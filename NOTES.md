# Notes

Two kinds of note: behaviour that changed in a published port because Odoo removed something, and things we found in Odoo 18, 19 and 20 that affect any port. Every statement about Odoo below was checked in the Odoo source code; the file is named so you can check it too.

## Behaviour changes in the published ports

These are in [`from-older-versions/`](from-older-versions). In a customer delivery, this is what the change summary would tell you.

| Module | Route | What changed | Why |
|---|---|---|---|
| `helpdesk_mgmt` | 16.0 to 20.0 and 16.0 to 19.0 | A new ticket without an assignee goes to the team leader. In 16.0 it went to the "Assign to" user of the team's email alias. | `mail.alias` no longer has `alias_user_id` (it is gone in both 19.0 and 20.0). The upstream module later dropped the automatic assignment altogether; our port keeps it and uses the nearest field that still exists. |
| `helpdesk_mgmt` | 16.0 to 20.0 and 17.0 to 20.0 | The ticket no longer keeps a CC list (`email_cc`). | Odoo 20 has no `mail.thread.cc` model. Odoo 19 still has it, so the ports to 19.0 keep the CC list. |
| `helpdesk_mgmt` | 15.0 to 19.0 | The alias owner field is gone from the team form and data. | Same removal of `alias_user_id`. |
| `purchase_request` | 15.0 to 19.0 | The allocations are no longer shown inside the transfer form's inline move form. They still show on the move form and on the detailed operations form. | Odoo 19's transfer form has no inline move form (`addons/stock/views/stock_picking_views.xml`). Upstream dropped the same view by 17.0. |
| `account_payment_partner` | 16.0 to 20.0 | Three tests set the company option "keep bank account without payment mode" explicitly instead of relying on its default. | See "A default that never reaches existing records" below. The upstream 19.0 tests do the same. |
| `contract` | 15.0 to 19.0 | Two tests were renamed (`..._fields_view_get` to `..._get_view`), with the same assertions. | `fields_view_get` was replaced by `get_view` in Odoo 16; upstream renamed them the same way. |
| `purchase_request` | 16.0 and 17.0, to 19.0 and 20.0 | One test no longer configures a "fixed procurement group" on a stock rule; it passes the reference on the move instead. | See "Procurement groups are gone" below. The test still checks that a request is reused, or not reused, according to the reference. |

## Things in Odoo 18, 19 and 20 that affect any port

### Since 18.0: inherited test methods silently stop running

`odoo/tests/loader.py` (`get_module_test_cases`) runs only the test methods written in a class's own body. A test method inherited from a parent class runs only if the class, or a parent, sets `allow_inherited_tests_method = True`. Odoo 16 and 17 ran inherited tests.

A module ported from 16 or 17 can therefore pass on 18, 19 or 20 with a large share of its tests no longer running, and nothing reports it. In `partner_firstname`, 26 of 61 test runs disappeared this way until we switched them back on.

### Since 20.0: one access model, and Odoo's upgrade script can drop record rules

Odoo 20 replaces `ir.model.access` and `ir.rule` with one model, `ir.access` (`odoo/addons/base/models/ir_access.py`; the data is in `security/ir.access.csv`). A row with a group is a permission, and permissions add up. A row without a group is a restriction for everybody. The old two layers, "may this group touch the model at all" and "which records", no longer exist.

Odoo ships a script that converts a module's access files (`odoo/upgrade_code/19.4-00-ir-access.py`). It removes the module's record rules from the XML and writes `ir.access` rows. In two situations it removes a rule and writes nothing in its place:

- The rule is on a model that another module owns, for example a rule on `account.move` in a module that depends on `account`. The script keeps only the operations it can find a permission for, and it cannot see the other module's permissions.
- A group was limited by a rule while a wider group, often all internal users, had the same operation without a rule. The wider row covers the limited one, so the limit disappears.

Nothing fails when this happens. The module installs, and tests rarely cover record rules.

We found it in our own ports on 18 November 2026: 6 of the 106 ported modules that had record rules were affected, and five of them were on this page. In one, users who were allowed to read only their own credit notes could read every journal entry. In another, users who were limited to their own appraisals could read everyone's. Three are corrected here (`rma`, `mail_gateway`, `product_assortment`) and pass their tests again. The other two are no longer on this page. In one, the rule can only be put back by also limiting users the original did not limit. In the other, putting it back makes two of the module's own tests fail, so its access design needs a decision from whoever uses the module. Every port is now compared rule by rule with its original, and a port with an open difference is not published.

The same script re-writes the XML files it touches through a parser, which drops the XML declaration and the copyright comment at the top of the file. That had happened in 13 files across 11 of our ports; they are restored, and it is checked on every port.

### Since 20.0: a currency rate applies from the day after its date

`res.currency._get_rates` in `odoo/addons/base/models/res_currency.py` looks for the latest rate dated strictly before the given date. Odoo 19 and older included the date itself (`<=`).

So an amount converted on the same day a rate is entered comes out different on 20.0. A multi-currency test that suddenly returns another number is usually hitting this. The right adaptation is in the test data (date the rate one day earlier). Changing the module's arithmetic to get the old number back would be wrong.

### Since 20.0: "is a company" is computed

`res.partner.is_company` is a stored computed field in 20.0: a partner is a company when it is its own commercial entity and has a tax ID (`_compute_is_company` in `odoo/addons/base/models/res_partner.py`). In 19.0 it is a plain checkbox. Code that writes `is_company = True` without a tax ID no longer creates a company.

### Since 20.0: no return wizard

There is no `stock.return.picking` wizard in 20.0. A return is created directly by `stock.picking._create_return()` and then edited like any transfer. A module that added fields or checks to the wizard has to move them onto the return transfer itself. Odoo 19 still has the wizard.

### Since 19.0: procurement groups are gone

There is no `procurement.group` model, and `stock.rule` has no `group_id` or `group_propagation_option`. `stock.reference` (`addons/stock/models/stock_reference.py`) replaces them.

### Since 20.0: no `mail.thread.cc`

Models that inherited `mail.thread.cc` to keep the CC addresses of incoming email have to inherit `mail.thread`, and the `email_cc` field goes with it.

### A default that never reaches existing records

When a module adds a field with a default, Odoo writes that default to the records that already exist, but only if the column is new (`Field.update_db` in `odoo/orm/fields.py`). If a module you depend on already defines the same field with another default, the column exists by the time your module loads, and your default is not written to existing records.

We met this with `account_payment_partner` from 16.0 on top of the 20.0 version of `account_payment_mode`: the dependency now defines the same company option with the opposite default, so the existing company never gets the value the module expects. It is a reason to port a module together with the modules it depends on.

### Small ones

- A domain `('field', 'in', value)` with a single value is turned into a one-item list before any search method sees it (`odoo/orm/domains.py`), so code and tests that expected an error from it no longer get one.
- There is no `account.group` model in 20.0.
