# What passes every test and still breaks: a porting checklist for Odoo 18, 19 and 20

A module can install on a new Odoo version, pass every test it has, and still be broken for the people who use it. Each line below is a case we met in a real port, where nothing failed and nothing warned. Every statement was checked in the Odoo source, and the whole list was then checked a second time, row by row, by a reviewer who had not written it (that pass removed three rows and corrected six); the file is named so you can check it too. We have no 17.0 source on our bench, so the two rows marked "18.0 at the latest" are checked in 18.0 only. [NOTES.md](NOTES.md) has the longer story for most of them, including the ones we got wrong ourselves first.

How to read it: "Since" is the first version where the old form stops working. "Look for" is a text search that finds candidates in a module; a hit is a place to read, not a verdict.

## Arriving at 17.0 or 18.0

| Since | What still installs and passes | What the user gets | Look for |
|---|---|---|---|
| 18.0 at the latest | `states={...}` on a field in Python is deleted during the port and nothing replaces it | The field is editable (or no longer required) in every state. The rule has to move into each view: `readonly="state == 'done'"` | `states=` in the old version's `models/` |
| 18.0 at the latest | An override of `name_get()` | It is never called; records show the default name. The name comes from `_compute_display_name` | `def name_get` |
| 18.0 | Test classes that inherit their test methods from a common parent | The inherited tests no longer run, and the run is still green. `odoo/tests/loader.py` runs only methods written in the class body unless `allow_inherited_tests_method = True` | compare the count of tests that ran before and after |
| 18.0 at the latest | `get_view()` that picks a view by a key of the action's context | The default view, always. The web client sends only `lang` and keys ending in `_view_ref` when it loads a view (`addons/web/static/src/views/view_service.js`, `filteredContext`). A test that passes the context to `get_view` itself still passes | `context.get(` inside `get_view` / `_get_view` |
| 18.0 | `view_type == "tree"` in Python, `"view_mode": "tree,form"` in an action built in code | The comparison never matches: the list view's type is `list` | `"tree"` in `.py` files |
| 18.0 | `copy()` overridden with `self.ensure_one()` | Works from the form. In the list view, select two rows and choose Duplicate: "Expected singleton". `BaseModel.copy` is multi-record; per-record defaults belong in `copy_data()` (`odoo/models.py`; `dynamic_list.js`, `_duplicateRecords`) | `def copy(` with `ensure_one` |
| 18.0 at the latest | `<field name="x" invisible="1"/>` as a column of a list | The column stays, with its title and empty cells. A column leaves the list only for `column_invisible` (`addons/web/static/src/views/list/list_renderer.js`, `getActiveColumns`) | a constant `invisible` on a direct child of `<list>` or `<tree>` |
| 18.0 | `<div class="oe_chatter">` with the three mail widgets | The form shows raw fields and no chatter. The tag is `<chatter/>` | `oe_chatter` |
| 18.0 | A `group_expand` method that takes `(self, stages, domain, order)` | Grouping by that field raises. The method is called with the records and the domain only (18.0: `odoo/models.py`, where `group_expand(self, groups, domain)` is called; 19.0: `odoo/orm/fields.py`, `determine_group_expand`) | `group_expand=` and the method it names |
| 18.0 | `self.user_has_groups(...)` in a button, wizard or controller | `AttributeError` when a user gets there. Use `self.env.user.has_groups(...)` | `user_has_groups` |

## Arriving at 19.0

| Since | What still installs and passes | What the user gets | Look for |
|---|---|---|---|
| 19.0 | A kanban view with `t-name="kanban-box"` | The view cannot be opened: `Missing 'card' template.` (`addons/web/static/src/views/kanban/kanban_arch_parser.js`). 18.0 still accepts the old name | `kanban-box` |
| 19.0 | A field's `search=` method that tests `operator == "="` | It never sees `=`: the condition arrives as `in` with a set (`odoo/orm/domains.py`, `_operator_equal_as_in`). A method that answers anyway can return the opposite of what was asked | `def _search_` methods that never mention `in` |
| 19.0 | `digits="Product Unit of Measure"` or `precision_get("Product Unit of Measure")` | 2 decimals, whatever the database has configured. The precision is named `Product Unit` now (`addons/uom/data/uom_data.xml`), and an unknown name is not an error (`decimal_precision.py`, `precision_get`). 18.0 still uses the old name | `Product Unit of Measure` outside labels |
| 19.0 | An override of `_message_get_suggested_recipients(self)`, or a call to `_message_add_suggested_recipient` | An error as soon as the chatter loads the recipients of a record (`addons/mail/models/models.py`) | both names |
| 19.0 | Code that reads `stock.move.name` | The field is gone; the move is named by `reference` (`addons/stock/models/stock_move.py`) | `.name` on moves, `"name":` in move values |
| 19.0 | Anything built on `procurement.group` or `stock.rule.group_id` | The model and the fields are gone; `stock.reference` replaces them | `procurement.group`, `group_propagation_option` |

## Arriving at 20.0

| What still installs and passes | What the user gets | Look for |
|---|---|---|
| An access right without a domain on a model another module owns (a plain right on `mail.message`, `sale.order`, `account.move`), carried over from the old access file | The group gets that model without any limit. In Odoo 20 a right and its limit are one row, the rows of all a user's groups add up (`odoo/orm/models.py`, `Domain.OR(permissions)`), and the owner's limits are the domains of its own rows (`addons/mail/security/ir.access.csv`). We found a module whose users could read every message in the database | rows of `security/ir.access.csv` with a group, an empty domain and a model the module does not define |
| Two records of one module with the same XML id, in different files | The one loaded later replaces the first without a word; a whole view can vanish | the same `id=` twice among a module's data files |
| `<t t-name="kanban-menu">` in a kanban view; a card link with `type="edit"` | The card has no menu; the link does nothing. The template is named `menu` (`addons/web/static/src/views/kanban/kanban_record.js`) and the action is `type="open"` (`addons/web/static/src/views/card/card_compiler.js`) | `kanban-menu`, `type="edit"` |
| A value set with `t-set` inside the body of a `t-call` | The called template does not receive it: a report without its address block, a portal page without its sidebar, or `KeyError` when a customer opens the page. Values travel as attributes of the `t-call` (`ir_qweb.py`, `_compile_directive_call`) | Odoo's `upgrade_code/19.1-00-t-call.py` finds most; it skips any `t-call` that carries `id=`, `groups=` or another plain attribute, so check those by hand |
| The same in a browser template under `static/` | The same; Odoo's script does not look there (`owl.js`, `compileTCall`) | `t-set` inside `t-call` in `static/src/**/*.xml` |
| `icon="fa-..."` on buttons, `<i class="fa fa-...">` anywhere | The letters "fa-bars" where the icon was, or an invisible control. Font Awesome is not loaded (`addons/web/__manifest__.py`, `web.icons_fonts`) | Odoo's `upgrade_code/19.5-00-material-symbols-icons.py`; it adds `icon_class` to search filters, which the view schema refuses there |
| Record rules converted with Odoo's own script | A rule can vanish without a replacement: on a model another module owns, or when a wider group has the same permission without a rule. Users then read records they could not read before (`upgrade_code/19.4-00-ir-access.py`) | compare every rule of the old version with the `ir.access` rows of the new one |
| A component with `static props`, or code using `useState`, `useRef`, `reactive`, `onRendered` | The file loads. The component throws when it is created (`static props`), or the hook is `undefined` when it is called, because Owl 3 no longer exports it. Only a browser test shows it | those names in `static/src` |
| Imports from paths that moved or were removed (`@web/core/orm_service`, `@web/core/ensure_jquery`, `@web/views/fields/badge_selection/...`, `@mail/core/common/record`, ...) | "modules are needed by other modules but have not been defined", and nothing that depends on it runs | resolve every import against the 20.0 tree |
| Code that relies on jQuery being there | `addons/web/static/lib/jquery` and the `web._assets_jquery` bundle are gone | `$(`, `jQuery`, `ensure_jquery` |
| `widget="remaining_days"` | "Missing widget", plain date shown. It is `relative_date` now | the widget name |
| `read_group(domain, fields, groupby)` called from Python | In 20.0 the second argument is the list to group by and the result is a list of tuples: `read_group(domain, groupby=(), aggregates=(), ...)` (`odoo/orm/models.py`). An old call raises as soon as there is data, or, when its group-by list was empty, quietly groups by the fields it meant to sum. Either way only on a code path the tests may not reach | `.read_group(` |
| Extensions of `_select`, `_from`, `_where`, `_group_by` on the invoice or purchase analysis, or of `_select_sale`, `_select_additional_fields`, `_from_sale`, `_group_by_sale` on the sales analysis | Nothing calls them. "column does not exist" on the invoice analysis; an empty column on the sales analysis. The reports are built from `_select_list` / `_select_dict` and `_groupby_list` now | those method names in `report/` |
| A module that makes `product.product.weight` a computed field that is not stored | The Sales app does not load at all: its report now builds SQL from the field (`addons/sale/report/sale_report.py`, `_select_dict`), and the ORM refuses a field that is not stored. On 19.0 the report read the column directly and nobody noticed | `weight = fields.Float(compute=` without `store=True` |
| `SELF_WRITEABLE_FIELDS` extended on `res.users` | An ordinary user gets an access error on their own preference; the administrator in the tests does not. The field needs `user_writeable=True` | `SELF_WRITEABLE_FIELDS`, `SELF_READABLE_FIELDS` |
| `get_param` / `set_param` on `ir.config_parameter`; `get_formview_action()`; `check_access_rights()`; `toggle_active()` | `AttributeError` when a user reaches the line. Use `get_str`/`get_int`/`get_bool`/`get_float` and their `set_` twins, `get_record_default_action()`, `has_access()`/`check_access()`, `action_archive()`/`action_unarchive()` | those names |
| `import pytz` or `import xlwt` without `external_dependencies` | Works where the package happens to be installed, fails to load on a clean Odoo 20 | the imports, then the manifest |
| `portal.portal_my_contact` called with `_contactAvatar`, `_contactName`, `_contactLink` | Empty avatar and name. The arguments are `_contact_avatar`, `_contact_name`, `_contact_link` | the camelCase names |
| Overrides of `_track_template`, `_track_subtype`, `_prepare_home_portal_values` and other renamed hooks | Nothing calls them; the feature is silently gone. For every method that calls `super()`, check the parent still has it in the target version | each `super().x(` against the 20.0 source |
| Money converted on the day a rate is entered | Another number than on 19.0: a rate applies from the day after its date (`res_currency.py`, `_get_rates`) | multi-currency tests that change result |
| A partner created with `is_company=True` and no tax ID | It is created as a person: the field is computed in 20.0 from the tax ID and the commercial entity (`res_partner.py`, `_compute_is_company`). A later plain write of `True` holds only until the tax ID or the parent changes | `is_company` in `create()` values and in data files |

Not on this list, because they fail loudly at install: a module that extends a model Odoo 20 no longer has (`stock.return.picking`, `mail.thread.cc`, `res.bank`, `account.group`), and a portal template that hooks onto the card blocks of the 19.0 home page (`portal_client_category` and its siblings), which are gone now that the cards are `portal.entry` records.

## What this list is for

Tests answer the question the old version's author asked. A new Odoo version asks new ones, and the old tests do not know them. Every row here got past a full test run at least once, most of them past ours. We now check each port for all of them mechanically, and since 20 November 2026 a second reviewer also reads the complete code change of a port against the Odoo source before we call it reviewed; [NOTES.md](NOTES.md), "Corrections to this page", says how we came to that.

If a row is wrong or out of date, open an issue and we will correct it.
