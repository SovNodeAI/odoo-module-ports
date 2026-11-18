# Copyright (c) Odoo SA 2017
# @author Nicolas Seinlet
# Copyright (c) ACSONE SA 2022
# @author Stéphane Bidoul
import functools
import json
import logging
import os
import sys

import psycopg2

import odoo
from odoo.http import session

_logger = logging.getLogger(__name__)

lock = None
if odoo.evented:
    import gevent.lock

    lock = gevent.lock.RLock()
elif odoo.tools.config["workers"] == 0:
    import threading

    lock = threading.RLock()


def with_lock(func):
    def wrapper(*args, **kwargs):
        try:
            if lock is not None:
                lock.acquire()
            return func(*args, **kwargs)
        finally:
            if lock is not None:
                lock.release()

    return wrapper


def with_cursor(func):
    def wrapper(self, *args, **kwargs):
        tries = 0
        while True:
            tries += 1
            try:
                self._ensure_connection()
                return func(self, *args, **kwargs)
            except (psycopg2.InterfaceError, psycopg2.OperationalError):
                self._close_connection()
                if tries > 4:
                    _logger.warning(
                        "session_db operation try %s/5 failed, aborting", tries
                    )
                    raise
                _logger.info("session_db operation try %s/5 failed, retrying", tries)

    return wrapper


class PGSessionStore(session.SessionStore):
    def __init__(self, uri, session_class=None):
        super().__init__(session_cls=session_class or session.Session)
        self._uri = uri
        self._cursor = None
        self._open_connection()
        self._setup_db()

    def __del__(self):
        self._close_connection()

    @with_lock
    def _ensure_connection(self):
        if self._cursor is None:
            self._open_connection()

    @with_lock
    def _open_connection(self):
        self._close_connection()
        cnx = odoo.sql_db.db_connect(self._uri, allow_uri=True)
        self._cursor = cnx.cursor()
        self._cursor._cnx.autocommit = True

    @with_lock
    def _close_connection(self):
        """Return cursor to the pool."""
        if self._cursor is not None:
            try:
                self._cursor.close()
            except Exception:  # pylint: disable=except-pass
                pass
            self._cursor = None

    @with_lock
    @with_cursor
    def _setup_db(self):
        self._cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS http_sessions (
                    sid varchar PRIMARY KEY,
                    write_date timestamp without time zone NOT NULL,
                    payload text NOT NULL
                )
            """
        )

    @with_lock
    @with_cursor
    def save(self, session):
        payload = json.dumps(dict(session))
        self._cursor.execute(
            """
                INSERT INTO http_sessions(sid, write_date, payload)
                    VALUES (%(sid)s, now() at time zone 'UTC', %(payload)s)
                ON CONFLICT (sid)
                DO UPDATE SET payload = %(payload)s,
                              write_date = now() at time zone 'UTC'
            """,
            dict(sid=session.sid, payload=payload),
        )

    @with_lock
    @with_cursor
    def delete(self, session):
        self._cursor.execute("DELETE FROM http_sessions WHERE sid=%s", (session.sid,))

    @with_lock
    @with_cursor
    def get(self, sid, *, keep_sid=False):
        self._cursor.execute("SELECT payload FROM http_sessions WHERE sid=%s", (sid,))
        try:
            data = json.loads(self._cursor.fetchone()[0])
        except Exception:
            if keep_sid:
                return self.session_cls({}, sid, new=False)
            return self.new()

        return self.session_cls(data, sid, new=False)

    # Odoo's SessionStore has a few additional methods that are independent
    # of the actual storage backend. We reuse them here.
    rotate = session.SessionStore.rotate
    generate_key = session.SessionStore.generate_key
    is_valid_session_id = session.SessionStore.is_valid_session_id
    delete_old_sessions = session.SessionStore.delete_old_sessions

    @with_lock
    @with_cursor
    def vacuum(self, max_lifetime=session.SESSION_LIFETIME):
        self._cursor.execute(
            "DELETE FROM http_sessions "
            "WHERE now() at time zone 'UTC' - write_date > %s",
            (f"{max_lifetime} seconds",),
        )

    @with_lock
    @with_cursor
    def get_missing_session_identifiers(self, identifiers: list[str]) -> set[str]:
        """
        :param identifiers: session identifiers whose file existence must be checked
                            identifiers are a part session sid (first 42 chars)
        :type identifiers: iterable
        :return: the identifiers which are not present on the filesystem
        :rtype: set

        Note 1:
        Working with identifiers 42 characters long means that
        we don't have to work with the entire sid session,
        while maintaining sufficient entropy to avoid collisions.
        See details in ``generate_key``.

        Note 2:
        Scans the session store for inactive (GC'd) sessions.
        Performance is acceptable for an infrequent background job.
        """
        missing_identifiers = set()
        for identifier in identifiers:
            self._cursor.execute(
                "SELECT sid FROM http_sessions WHERE sid LIKE %s||'%%' LIMIT 1",
                (identifier,),
            )
            if self._cursor.rowcount == 0:
                missing_identifiers.add(identifier)
        return missing_identifiers

    @with_lock
    @with_cursor
    def delete_from_identifiers(self, identifiers: list[str]) -> None:
        for identifier in identifiers:
            if not session._session_identifier_re.match(identifier):
                raise ValueError(
                    "Identifier format incorrect, "
                    "did you pass in a string instead of a list?"
                )
            self._cursor.execute(
                "DELETE FROM http_sessions WHERE sid LIKE %s||'%%'", (identifier,)
            )


_original_session_store = session.session_store


@functools.cache
def session_store():
    session_db_uri = os.environ.get("SESSION_DB_URI")
    if session_db_uri:
        _logger.debug("HTTP sessions stored in: db")
        return PGSessionStore(session_db_uri, session_class=session.Session)
    return _original_session_store()


# Monkey patch of standard methods
_logger.debug("Monkey patching session store")
session.session_store = session_store
# Odoo 20 imports ``session_store`` by name in several modules, so the
# already imported references must be patched as well.
for _module in list(sys.modules.values()):
    try:
        if getattr(_module, "session_store", None) is _original_session_store:
            _module.session_store = session_store
    except Exception:  # pylint: disable=except-pass
        pass
del _module
