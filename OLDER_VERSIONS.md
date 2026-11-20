# Ports from Odoo 15.0, 16.0 and 17.0

The same modules exist upstream for newer versions. These ports are made from the OLD version's code on purpose, to show the jump a private module would have to make.

On 20 November 2026 all ports listed here were withdrawn for a second review: each had passed every one of its own tests, and the first three that were then read against the maintainers' own version for the target had faults no test of the module touches. A port is listed again only after that review, with every finding fixed or ruled out and the tests passing again. See "Corrections to this page" in [NOTES.md](NOTES.md).

3 ports listed now.

| From | To | Module | Source repository | Commit | License | Test runs (all pass) | Note |
|---|---|---|---|---|---|---|---|
| 17.0 | 18.0 | [partner_firstname](from-older-versions/17.0-to-18.0/partner_firstname) | OCA/partner-contact | `7a5ddbd` | AGPL-3 | 66 | second review passed after 2 reads |
| 15.0 | 19.0 | [auditlog](from-older-versions/15.0-to-19.0/auditlog) | OCA/server-tools | `85b4112` | AGPL-3 | 40 | second review passed after 2 reads; one point is the original's own behaviour, see NOTES.md |
| 16.0 | 19.0 | [purchase_request](from-older-versions/16.0-to-19.0/purchase_request) | OCA/purchase-workflow | `e41f927` | LGPL-3 | 39 | second review passed after 3 reads; two behaviour changes, see NOTES.md |
