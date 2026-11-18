# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tools import convert_file

# Demo data is no longer installed by default in Odoo 20 test databases,
# so the tests that rely on it load it explicitly when missing.
DEMO_FILES = [
    "demo/resolver_demo.xml",
    "demo/export_demo.xml",
    "demo/ir.exports.line.csv",
]


def load_demo_data(env):
    if env.ref("jsonifier.ir_exp_partner", raise_if_not_found=False):
        return
    for fname in DEMO_FILES:
        convert_file(env, "jsonifier", fname, {}, mode="init", noupdate=True)
