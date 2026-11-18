from . import spec_export
from . import spec_import
from . import spec_mixin
from . import ir_model

# from . import spec_view
from . import spec_models
from .spec_models import install_spec_model_hooks

# Odoo 20 moved model construction to odoo.orm.model_classes.
install_spec_model_hooks()
