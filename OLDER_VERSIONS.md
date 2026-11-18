# Ports from Odoo 15.0, 16.0 and 17.0

The same modules exist upstream for newer versions. These ports were made from the OLD version's code on purpose, to show the jump a private module would have to make. 23 ports, each with every one of its own tests running and passing on a clean database of the target version.

| From | To | Module | Source repository | Commit | License | Test runs (all pass) | Note |
|---|---|---|---|---|---|---|---|
| 15.0 | 19.0 | [auditlog](from-older-versions/15.0-to-19.0/auditlog) | OCA/server-tools | `85b4112` | AGPL-3 | 38 |  |
| 15.0 | 19.0 | [partner_firstname](from-older-versions/15.0-to-19.0/partner_firstname) | OCA/partner-contact | `52c4359` | AGPL-3 | 57 |  |
| 15.0 | 19.0 | [purchase_request](from-older-versions/15.0-to-19.0/purchase_request) | OCA/purchase-workflow | `733d378` | LGPL-3 | 26 | one view customisation dropped with the form Odoo removed, see NOTES.md |
| 16.0 | 19.0 | [auditlog](from-older-versions/16.0-to-19.0/auditlog) | OCA/server-tools | `6141f1f` | AGPL-3 | 48 |  |
| 16.0 | 19.0 | [partner_firstname](from-older-versions/16.0-to-19.0/partner_firstname) | OCA/partner-contact | `8a58599` | AGPL-3 | 62 |  |
| 16.0 | 19.0 | [purchase_request](from-older-versions/16.0-to-19.0/purchase_request) | OCA/purchase-workflow | `e41f927` | LGPL-3 | 30 | one test adapted: procurement groups are gone, see NOTES.md |
| 16.0 | 19.0 | [sale_automatic_workflow](from-older-versions/16.0-to-19.0/sale_automatic_workflow) | OCA/sale-workflow | `866d018` | AGPL-3 | 13 |  |
| 17.0 | 19.0 | [auditlog](from-older-versions/17.0-to-19.0/auditlog) | OCA/server-tools | `ecb2422` | AGPL-3 | 41 |  |
| 17.0 | 19.0 | [partner_firstname](from-older-versions/17.0-to-19.0/partner_firstname) | OCA/partner-contact | `7a5ddbd` | AGPL-3 | 61 |  |
| 17.0 | 19.0 | [purchase_request](from-older-versions/17.0-to-19.0/purchase_request) | OCA/purchase-workflow | `e1103fb` | LGPL-3 | 30 | one test adapted: procurement groups are gone, see NOTES.md |
| 17.0 | 19.0 | [sale_automatic_workflow](from-older-versions/17.0-to-19.0/sale_automatic_workflow) | OCA/sale-workflow | `f579f65` | AGPL-3 | 11 |  |
| 15.0 | 20.0 | [auditlog](from-older-versions/15.0-to-20.0/auditlog) | OCA/server-tools | `85b4112` | AGPL-3 | 38 |  |
| 15.0 | 20.0 | [partner_firstname](from-older-versions/15.0-to-20.0/partner_firstname) | OCA/partner-contact | `52c4359` | AGPL-3 | 57 |  |
| 16.0 | 20.0 | [account_payment_partner](from-older-versions/16.0-to-20.0/account_payment_partner) | OCA/bank-payment | `47fa61d` | AGPL-3 | 20 | three tests set a company option explicitly, see NOTES.md |
| 16.0 | 20.0 | [auditlog](from-older-versions/16.0-to-20.0/auditlog) | OCA/server-tools | `6141f1f` | AGPL-3 | 48 |  |
| 16.0 | 20.0 | [partner_firstname](from-older-versions/16.0-to-20.0/partner_firstname) | OCA/partner-contact | `8a58599` | AGPL-3 | 62 |  |
| 16.0 | 20.0 | [purchase_request](from-older-versions/16.0-to-20.0/purchase_request) | OCA/purchase-workflow | `e41f927` | LGPL-3 | 30 | one test adapted: procurement groups are gone, see NOTES.md |
| 17.0 | 20.0 | [account_payment_partner](from-older-versions/17.0-to-20.0/account_payment_partner) | OCA/bank-payment | `cea05f5` | AGPL-3 | 20 |  |
| 17.0 | 20.0 | [auditlog](from-older-versions/17.0-to-20.0/auditlog) | OCA/server-tools | `ecb2422` | AGPL-3 | 41 |  |
| 17.0 | 20.0 | [partner_firstname](from-older-versions/17.0-to-20.0/partner_firstname) | OCA/partner-contact | `7a5ddbd` | AGPL-3 | 61 |  |
| 17.0 | 20.0 | [purchase_request](from-older-versions/17.0-to-20.0/purchase_request) | OCA/purchase-workflow | `e1103fb` | LGPL-3 | 30 |  |
| 17.0 | 20.0 | [sale_automatic_workflow](from-older-versions/17.0-to-20.0/sale_automatic_workflow) | OCA/sale-workflow | `f579f65` | AGPL-3 | 11 |  |
| 17.0 | 20.0 | [web_company_color](from-older-versions/17.0-to-20.0/web_company_color) | OCA/web | `fca94d5` | AGPL-3 | 4 |  |
