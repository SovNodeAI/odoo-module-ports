# Copyright 2026 Akretion
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

"""Adapters for the functional model-construction API introduced in Odoo 20.

Odoo 18 dispatched model registration and field setup through overridable model
methods. Odoo 20 uses functions in ``odoo.orm.model_classes``. These wrappers
retain the original extension points used by spec models while delegating all
ordinary work to the core implementations.
"""

from types import MappingProxyType

from odoo.orm import model_classes
from odoo.orm.model_classes import is_model_definition
from odoo.tools import LastOrderedSet
from odoo.tools.safe_eval import safe_checker

_original_add_to_registry = model_classes.add_to_registry
_original_setup = model_classes._setup
_original_setup_fields = model_classes._setup_fields
_original_add_field = model_classes.add_field
_direct_setup_models = set()


def _is_spec_model(model_cls):
    return any(getattr(base, "_is_spec_driven", False) for base in model_cls.mro())


def _add_synthetic_schema_model(registry, model_def):
    """Replace an abstract schema registry class with its concrete SpecModel."""
    old_cls = registry[model_def._name]
    # Build the new registry wrapper, not the extension wrapper returned by
    # ordinary self-inheritance. These synthetic classes already carry the
    # ordinary schema definitions as Python bases.
    model_cls = type(
        model_def._name,
        (model_def,),
        {
            **{
                name: old_cls.__dict__[name]
                for name in (
                    "_inherit_module",
                    "_inherit_children",
                    "_inherits_children",
                )
            },
            "pool": registry,
            "_name": model_def._name,
            "_register": False,
            "_original_module": model_def._module,
            "_fields__": {},
            "_fields_update_order__": {},
            "_table_objects": {},
            "_setup_done__": False,
            "_setup_fields_done__": False,
        },
    )
    bases = LastOrderedSet([model_def])
    # Keep every genuine definition class of the model (the schema class and
    # the downstream _inherit extensions), but never a previous synthetic
    # definition nor a registry class: those would either duplicate the model
    # or break the C3 linearization on the next rebuild. The synthetic
    # definition carries them as its own Python bases, which is the only place
    # they survive once the previous registry class replaced them.
    for base in model_def.__bases__:
        if (
            is_model_definition(base)
            and base._name == model_def._name
            and not base.__dict__.get("_spec_synthetic", False)
        ):
            bases.add(base)
    model_cls._fields = MappingProxyType(model_cls._fields__)
    for parent_name in model_def._inherit:
        if parent_name != model_def._name:
            bases.add(registry[parent_name])
            registry[parent_name]._inherit_children.add(model_def._name)
    bases.add(registry["base"])
    model_cls._base_classes__ = tuple(bases)
    model_classes._init_model_class_attributes(model_cls)
    # This model is made concrete on purpose: Odoo 18 built it directly as a
    # SpecModel subclass, so ordinary extension checks do not apply.
    model_cls._abstract = False
    registry[model_def._name] = model_cls
    for model_name in registry.descendants(
        [model_def._name], "_inherit", "_inherits"
    ):
        registry[model_name]._setup_done__ = False
    safe_checker.add_hook(model_cls, None)
    return model_cls


def add_to_registry(registry, model_def):
    if getattr(model_def, "_spec_synthetic", False):
        return _add_synthetic_schema_model(registry, model_def)
    if hasattr(model_def, "_spec_add_to_registry"):
        return model_def._spec_add_to_registry(registry)
    return _original_add_to_registry(registry, model_def)


def setup(model_cls, env):
    if not hasattr(model_cls, "_spec_mute_selection_logger"):
        return _original_setup(model_cls, env)
    with model_cls(env, (), ())._spec_mute_selection_logger():
        return _original_setup(model_cls, env)


def setup_fields(model_cls, env):
    if model_cls not in _direct_setup_models and hasattr(model_cls, "_prepare_spec_field_setup"):
        model_cls(env, (), ())._prepare_spec_field_setup()
    return _original_setup_fields(model_cls, env)


def add_field(model_cls, name, field, shareable=False):
    if hasattr(model_cls, "_spec_skip_stacking_field") and model_cls._spec_skip_stacking_field(name, field):
        return
    return _original_add_field(model_cls, name, field, shareable)


def install_spec_model_hooks():
    """Install the adapter before the registry definitions are built."""
    model_classes.add_to_registry = add_to_registry
    model_classes._setup = setup
    model_classes._setup_fields = setup_fields
    model_classes.add_field = add_field


def setup_model_definition(model_cls, env):
    """Direct setup equivalent for models added after the regular setup loop."""
    rec_name = model_cls._rec_name
    # The registry class may already have been set up by the regular loop (it
    # existed before this hook replaced it). Force a fresh setup, otherwise
    # _setup() returns early and leaves the class without any field.
    model_cls._setup_done__ = False
    model_classes._prepare_setup(model_cls)
    _direct_setup_models.add(model_cls)
    try:
        _original_setup(model_cls, env)
        if rec_name:
            model_cls._rec_name = rec_name
        model = model_cls(env, (), ())
        if hasattr(model, "_prepare_spec_field_setup"):
            model._prepare_spec_field_setup()
        model_cls._fields_update_order__ = {
            field: (field.write_sequence, i)
            for i, field in enumerate(model_cls._fields.values())
        }
        model_classes._setup_fields(model_cls, env)
        model_cls._setup_done__ = True
        model_cls._setup_fields_done__ = True
        if rec_name not in model_cls._fields:
            schema = getattr(model_cls, "_spec_schema", "")
            version = getattr(model_cls, "_spec_version", "").replace(".", "")[:2]
            field_prefix = f"{schema}{version}_" if schema else "x_"
            rec_name = next(
                (
                    name for name in model_cls._fields
                    if name.startswith(field_prefix) and "_choice" not in name
                ),
                False,
            )
        if rec_name:
            model_cls._rec_name = rec_name
        model_cls(env, (), ())._post_model_setup__()
        return model_cls(env, (), ())
    finally:
        _direct_setup_models.discard(model_cls)
