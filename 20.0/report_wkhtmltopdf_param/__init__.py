# Copyright 2017 Avoin.Systems
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os

os.environ["PATH"] = (
    os.path.join(os.path.dirname(__file__), "tools")
    + os.pathsep
    + os.environ.get("PATH", "")
)

from . import models
