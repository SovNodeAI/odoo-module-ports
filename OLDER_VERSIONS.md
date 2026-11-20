# Ports from Odoo 15.0, 16.0 and 17.0

The same modules exist upstream for newer versions. These ports are made from the OLD version's code on purpose, to show the jump a private module would have to make.

On 20 November 2026 all ports listed here were withdrawn for a second review: each had passed every one of its own tests, and the first three that were then read against the maintainers' own version for the target had faults no test of the module touches. A port is listed again only after that review, with every finding fixed or ruled out and the tests passing again. See "Corrections to this page" in [NOTES.md](NOTES.md).

1 port listed now.

| From | To | Module | Source repository | Commit | License | Test runs (all pass) | Note |
|---|---|---|---|---|---|---|---|
| 15.0 | 19.0 | [auditlog](from-older-versions/15.0-to-19.0/auditlog) | OCA/server-tools | `85b4112` | AGPL-3 | 40 | second review passed after 2 reads; one point is the original's own behaviour, see NOTES.md |
