# Copyright 2019-TODAY Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

import logging
import sys
from collections import OrderedDict, defaultdict
from importlib import import_module
from inspect import getmembers, isclass

from contextlib import nullcontext

from odoo import SUPERUSER_ID, _, api, models
from odoo.models import is_model_definition
from odoo.orm import model_classes
from odoo.tools import mute_logger

from .ir_model import disambiguate_spec_labels
from .spec_compat import install_spec_model_hooks
from . import spec_compat

SPEC_MIXIN_MAPPINGS = defaultdict(dict)  # by db

_logger = logging.getLogger(__name__)


class SelectionMuteLogger(mute_logger):
    """
    The following fields.Selection warnings seem both very hard to
    avoid and benign in the spec_driven_model framework context.
    All in all, muting these 2 warnings seems like the best option.
    """

    def filter(self, record):
        msg = record.getMessage()
        if (
            "selection attribute will be ignored" in msg
            or "overrides existing selection" in msg
        ):
            return 0
        return super().filter(record)


class SpecModel(models.Model):
    """When you inherit this Model, then your model becomes concrete just like
    models.Model and it can use _inherit to inherit from several xsd generated
    spec mixins.
    All your model relational fields will be automatically mutated according to
    which concrete models the spec mixins where injected in.
    Because of this field mutation logic in _build_model, SpecModel should be
    inherited the Python way YourModel(spec_models.SpecModel)
    and not through _inherit.
    """

    _inherit = ["spec.mixin"]
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry
    _abstract = False
    _transient = False

    # TODO generic onchange method that check spec field simple type formats
    # xsd_required, according to the considered object context
    # and return warning or reformat things
    # ideally the list of onchange fields is set dynamically but if it is too
    # hard, we can just dump the list of fields when SpecModel is loaded

    # TODO a save python constraint that ensuire xsd_required fields for the
    # context are present

    @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    def _compute_display_name(self):
        "More user friendly when automatic _rec_name is bad"
        res = super()._compute_display_name()
        for rec in self:
            if rec.display_name == "False" or not rec.display_name:
                # a new record keeps the client "New" breadcrumb
                rec.display_name = _("Open...") if rec.id else False
        return res

    @classmethod
    def _spec_add_to_registry(cls, pool):
        """
        xsd generated spec mixins do not need to depend on this opinionated
        module. That's why the spec.mixin is dynamically injected as a parent
        class as long as the generated spec mixins inherit from some
        spec.mixin.<schema_name> mixin.
        """
        # In Odoo 18+, the test framework monitors model attribute modifications
        # and logs stack traces. We suppress these during dynamic model building.
        with mute_logger("odoo.tests.common"):
            if hasattr(cls, "_spec_schema"):  # when called via _register_hook
                schema = cls._spec_schema
            else:
                mod = import_module(".".join(cls.__module__.split(".")[:-1]))
                schema = mod.spec_schema

            if schema and not hasattr(cls, "_spec_schema"):
                spec_mixin = pool[f"spec.mixin.{schema}"]
                if spec_mixin._name not in getattr(spec_mixin, "_inherit_children", ()):
                    definition = next(
                        base
                        for base in spec_mixin._base_classes__
                        if is_model_definition(base) and base._name == spec_mixin._name
                    )
                    if "spec.mixin" not in definition._inherit__:
                        definition._inherit__ = [*definition._inherit__, "spec.mixin"]
                        spec_compat._original_add_to_registry(pool, definition)
                        for child_name in pool.descendants([definition._name], '_inherit'):
                            child = pool[child_name]
                            definition_cls = next(
                                b for b in child._base_classes__
                                if is_model_definition(b) and b._name == child_name
                            )
                            spec_compat._original_add_to_registry(pool, definition_cls)

            for parent in cls._inherit:
                cls._map_concrete(pool.db_name, parent, cls._name)
            return spec_compat._original_add_to_registry(pool, cls)

    def _spec_mute_selection_logger(self):
        if hasattr(type(self), "_is_spec_driven"):
            return SelectionMuteLogger("odoo.fields")
        return nullcontext()

    def _spec_setup(self, env):
        from . import spec_compat

        return spec_compat.setup_model_definition(type(self), env)

    def _prepare_spec_field_setup(self):
        """
        SpecModel models inherit their fields from XSD generated mixins.
        These mixins can either be made concrete, either be injected into
        existing concrete Odoo models. In that last case, the comodels of the
        relational fields pointing to such mixins should be remapped to the
        proper concrete models where these mixins are injected.
        """
        cls = type(self)
        stacked_parents = [getattr(x, "_name", None) for x in cls.mro()]
        for name, field in cls._fields.items():
            if hasattr(field, "comodel_name") and field.comodel_name:
                comodel_name = field.comodel_name
                comodel = self.env[comodel_name]
                concrete_class = SPEC_MIXIN_MAPPINGS[self.env.cr.dbname].get(
                    comodel._name
                )

                if (
                    field.type == "many2one"
                    and concrete_class is not None
                    and comodel_name not in stacked_parents
                ):
                    _logger.debug(
                        "    MUTATING m2o %s (%s) -> %s",
                        name,
                        comodel_name,
                        concrete_class,
                    )
                    field.original_comodel_name = comodel_name
                    field.comodel_name = concrete_class

                elif field.type == "one2many":
                    if concrete_class is not None:
                        _logger.debug(
                            "    MUTATING o2m %s (%s) -> %s",
                            name,
                            comodel_name,
                            concrete_class,
                        )
                        field.original_comodel_name = comodel_name
                        field.comodel_name = concrete_class
                    if not hasattr(field, "inverse_name"):
                        continue
                    inv_name = field.inverse_name
                    for n, f in comodel._fields.items():
                        if n == inv_name and f._args__ and f._args__.get("comodel_name"):
                            _logger.debug(
                                "    MUTATING m2o %s.%s (%s) -> %s",
                                comodel._name.split(".")[-1],
                                n,
                                f._args__["comodel_name"],
                                cls._name,
                            )
                            f._args__ = {
                                **f._args__,
                                "original_comodel_name": f._args__["comodel_name"],
                                "comodel_name": self._name,
                            }

        disambiguate_spec_labels(cls)

    @classmethod
    def _map_concrete(cls, dbname, key, target, quiet=False):
        if not quiet:
            _logger.debug(f"{key} ---> {target}")
        global SPEC_MIXIN_MAPPINGS
        SPEC_MIXIN_MAPPINGS[dbname][key] = target

    @classmethod
    def spec_module_classes(cls, spec_module):
        """
        Cache the list of spec_module classes to save calls to
        slow reflection API.
        """
        spec_module_attr = f"_spec_cache_{spec_module.replace('.', '_')}"
        if not hasattr(cls, spec_module_attr):
            # In Odoo 18+, the test framework monitors model attribute modifications
            # and logs stack traces. We suppress these during dynamic model building.
            with mute_logger("odoo.tests.common"):
                setattr(
                    cls, spec_module_attr, getmembers(sys.modules[spec_module], isclass)
                )
        return getattr(cls, spec_module_attr)

    @classmethod
    def _odoo_name_to_class(cls, odoo_name, spec_module):
        for _name, base_class in cls.spec_module_classes(spec_module):
            if base_class._name == odoo_name:
                return base_class
        return None


class StackedModel(SpecModel):
    """
    XML structures are typically deeply nested as this helps xsd
    validation. However, deeply nested objects in Odoo suck because that would
    mean crazy joins accross many tables and also an endless cascade of form
    popups.

    By inheriting from StackModel instead, your models.Model can
    instead inherit all the mixins that would correspond to the nested xsd
    nodes starting from the stacking_mixin. stacking_skip_paths allows you to avoid
    stacking specific nodes while stacking_force_paths will stack many2one
    entities even if they are not required.

    In Brazil it allows us to have mostly the fiscal
    document objects and the fiscal document line object with many details
    stacked in a denormalized way inside these two tables only.
    Because StackedModel has its _build_method overriden to do some magic
    during module loading it should be inherited the Python way
    with MyModel(spec_models.StackedModel).
    """

    _register = False  # forces you to inherit StackeModel properly

    @classmethod
    def _spec_add_to_registry(cls, pool):
        # In Odoo 18+, the test framework monitors model attribute modifications
        # and logs stack traces. We suppress these during dynamic model building.
        with mute_logger("odoo.tests.common"):
            if hasattr(cls, "_spec_schema"):  # when called via _register_hook
                schema = cls._spec_schema
                version = cls._spec_version.replace(".", "")[:2]
            else:
                mod = import_module(".".join(cls.__module__.split(".")[:-1]))
                schema = mod.spec_schema
                version = mod.spec_version.replace(".", "")[:2]
            spec_prefix = f"{schema}{version}"
            setattr(cls, f"_{spec_prefix}_stacking_points", {})
        stacking_settings = {
            "odoo_module": getattr(cls, f"_{spec_prefix}_odoo_module"),  # TODO inherit?
            "stacking_mixin": getattr(cls, f"_{spec_prefix}_stacking_mixin"),
            "stacking_points": getattr(cls, f"_{spec_prefix}_stacking_points"),
            "stacking_skip_paths": getattr(
                cls, f"_{spec_prefix}_stacking_skip_paths", []
            ),
            "stacking_force_paths": getattr(
                cls, f"_{spec_prefix}_stacking_force_paths", []
            ),
        }
        # inject all stacked m2o as inherited classes
        _logger.info(f"building StackedModel {cls._name} {cls}")
        node = cls._odoo_name_to_class(
            stacking_settings["stacking_mixin"], stacking_settings["odoo_module"]
        )
        cr = pool.cursor()
        env = api.Environment(cr, SUPERUSER_ID, {})
        for kind, klass, _path, _field_path, _child_concrete in cls._visit_stack(
            env, node, stacking_settings
        ):
            if kind == "stacked" and klass not in cls.__bases__:
                cls._inherit.append(klass._name)
        return super()._spec_add_to_registry(pool)

    @classmethod
    def _spec_skip_stacking_field(cls, name, field):
        """Avoid adding many2one fields that are in fact stacking points."""
        if field.type != "many2one":
            return False
        for klass in cls.mro():
            if issubclass(klass, StackedModel):
                for attr in dir(klass):
                    if attr != "_get_stacking_points" and attr.endswith(
                        "_stacking_points"
                    ) and name in getattr(klass, attr):
                        # The original _add_field override also skipped these fields.
                        return True
        return False

    @classmethod
    def _visit_stack(cls, env, node, stacking_settings, path=None):
        """Pre-order traversal of the stacked models tree.
        1. This method is used to dynamically inherit all the spec models
        stacked together from an XML hierarchy.
        2. It is also useful to generate an automatic view of the spec fields.
        3. Finally it is used when exporting as XML.
        """
        if path is None:
            path = stacking_settings["stacking_mixin"].split(".")[-1]
        cls._map_concrete(env.cr.dbname, node._name, cls._name, quiet=True)
        yield "stacked", node, path, None, None

        fields = OrderedDict()
        # this is required when you don't start odoo with -i (update)
        # otherwise the model spec will not have its fields loaded yet.
        # TODO we may pass this env further instead of re-creating it.
        # TODO move setup_base just before the _visit_stack next call
        if node._name != cls._name or not env[node._name]._fields:
            model = env[node._name]
            model_classes._prepare_setup(type(model))
            model_classes._setup(type(model), env)

        field_items = [(k, f) for k, f in env[node._name]._fields.items()]
        for i in field_items:
            fields[i[0]] = {
                "type": i[1].type,
                # TODO get with a function (lambda?)
                "comodel_name": getattr(i[1], "comodel_name", None),
                "xsd_required": hasattr(i[1], "xsd_required") and i[1].xsd_required,
                "xsd_choice_required": hasattr(i[1], "xsd_choice_required")
                and i[1].xsd_choice_required,
            }
        for name, f in fields.items():
            if f["type"] not in [
                "many2one",
                "one2many",
            ] or name in stacking_settings.get("stacking_skip_paths", ""):
                # TODO change for view or export
                continue
            child = cls._odoo_name_to_class(
                f["comodel_name"], stacking_settings["odoo_module"]
            )
            if child is None:  # Not a spec field
                continue
            child_concrete = SPEC_MIXIN_MAPPINGS[env.cr.dbname].get(child._name)
            field_path = name.split("_")[1]  # remove schema prefix

            if f["type"] == "one2many":
                yield "one2many", node, path, field_path, child_concrete
                continue

            force_stacked = any(
                stack_path in path + "." + field_path
                for stack_path in stacking_settings.get("stacking_force_paths", [])
            )

            # many2one
            if (child_concrete is None or child_concrete == cls._name) and (
                f["xsd_required"] or f["xsd_choice_required"] or force_stacked
            ):
                # then we will STACK the child in the current class
                # In Odoo 18+, the test framework monitors model attribute modifications
                # and logs stack traces. We suppress these during dynamic model building
                with mute_logger("odoo.tests.common"):
                    child._stack_path = path
                child_path = f"{path}.{field_path}"
                stacking_settings["stacking_points"][name] = env[
                    node._name
                ]._fields.get(name)
                yield from cls._visit_stack(env, child, stacking_settings, child_path)
            else:
                yield "many2one", node, path, field_path, child_concrete
