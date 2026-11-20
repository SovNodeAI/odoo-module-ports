# Notes

Two kinds of note: behaviour that changed in a published port because Odoo removed something, and things we found in Odoo 18, 19 and 20 that affect any port. Every statement about Odoo below was checked in the Odoo source code; the file is named so you can check it too.

## Corrections to this page

### 20 November 2026, night: a second review of the Odoo 20 list has begun, and its first three results are bad

After the older-version ports, the second reviewer read the complete code change (19.0 to 20.0) of three of the larger modules on the Odoo 20 list. All three have faults that none of their tests touches.

- `mis_builder`. Two findings checked by us in the source. In `models/aep.py` the 19.0 code combined the date conditions of the accounting modes with OR; the port combines them with AND, so a KPI that mixes modes drills down to nothing. In `models/mis_report.py` the port still calls `read_group(domain, fields, [])`; in Odoo 20 the second argument of `read_group` is the list to group by (`odoo/orm/models.py`), so a query that sums stored fields does not get what it asked for. The only query the tests run sums a field that is not stored and takes another path.
- `account_financial_report`. One finding checked: the port relaxed a guard in `wizard/trial_balance_wizard.py` from exactly one unaffected-earnings account to at least one. The review lists more, about accounts without a code (Odoo 20's US chart has none), which we have not verified yet.
- `helpdesk_mgmt`. The review lists portal values still set inside a `t-call` body in a form our own check did not catch, arguments of `portal.portal_my_contact` that Odoo 20 renamed, and more. Not verified yet.

The three are off the list, with the modules that depend on them. What this means for the rest: until 20 November nobody had read the complete code change of any module on this list. Tests, a review of every changed test, and our static checks were the whole proof. For small modules that may be enough. For large ones it was not. [MODULES.md](MODULES.md) now has a column that says whether a module's second review is done, and the README says plainly what the list does and does not claim.

### 20 November 2026, later: ports from older versions withdrawn for a second review

Until today this page carried ports made from the 15.0, 16.0 and 17.0 versions of well-known modules to 19.0 and 20.0. Each had passed every one of its own tests. The second reviewer then read three of them against the maintainers' own 19.0 version of the same module.

The first was `helpdesk_mgmt` from 17.0 to 19.0. We checked three of its findings in the Odoo 19 source ourselves, and all three hold:

- The kanban views still had a `kanban-box` template. Odoo 19 reads the card from a template named `card` and stops with `Missing 'card' template.` otherwise (`addons/web/static/src/views/kanban/kanban_arch_parser.js`). The ticket board, the dashboard and the team form would not open.
- The method that lists the stages when tickets are grouped by stage still took a third argument, `order`. Odoo 19 calls a `group_expand` method with the records and the domain only (`odoo/orm/fields.py`, `determine_group_expand`), so grouping by stage would raise an error.
- The override of `_message_get_suggested_recipients` kept the old signature and called `_message_add_suggested_recipient`, which no longer exists (`addons/mail/models/models.py`).

None of the module's tests opens a kanban view, groups by stage or loads the recipients of a ticket, so all of them passed. The reviews of `purchase_request` (16.0 to 19.0) and `auditlog` (15.0 to 19.0) list further faults, which we are checking one by one.

A port from an old version crosses several releases at once. Tests written for the old version prove less across that distance than we said they did. All ports from older versions are off the page. Each returns only after it has been read against the maintainers' version for the target, every finding has been fixed or ruled out, and its tests pass again.

### 20 November 2026: icons that Odoo 20 no longer draws

A second reviewer read one of our ports in full and pointed at something none of our checks looked for. Odoo 20 does not load Font Awesome. `web.icons_fonts` in `addons/web/__manifest__.py` is Material Symbols plus Odoo's own icon font, and no bundle includes `font-awesome.css` any more (19.0 loaded it in three). A view button is drawn as `<i class="o_button_icon oi" data-icon="...">` with the `icon` attribute exactly as written (`addons/web/static/src/views/view_button/view_button.js`, `iconFromString`). So `<button icon="fa-bars"/>` shows the letters "fa-bars" where the icon was, and `<i class="fa fa-trash-o"/>` shows nothing: a control that is only an icon cannot be seen.

Nothing fails. No Python test looks at an icon. A browser test that clicks an icon fails only if the test tool checks that the icon can be seen; ours did, in one module, and that port's test had been changed to click it anyway. We accepted the explanation given for that change and should not have.

81 of our ports still named icons the Font Awesome way, 71 of them listed here. Those 71 are off the page, and so are 43 modules that depend on one of them: 114 in all. They return as their icons are converted with Odoo's own script (`odoo/upgrade_code/19.5-00-material-symbols-icons.py`) and their tests pass again. See "Since 20.0: Font Awesome is gone" below.

The same review found a search method that one port had rewritten for a call Odoo no longer makes (see "Since 19.0: a field's search method is called with `in`" below). That module, `stock_weighing`, is off the page for both reasons. One older-version port, `base_tier_validation` from 17.0 to 19.0, is held back for the same check until its search methods have been read.

### 18 November 2026, evening: a module is not listed while what it depends on has a defect

Until now each module was judged alone: its own tests, its own code. But a module shows the screens and prints the templates of the modules it depends on. `sale_tier_validation` was listed here while `base_tier_validation`, whose review widget it puts on the sale order, still had JavaScript that Odoo 20 cannot load. Its tests passed because none of them opens that form in a browser.

The rule now: a module is listed only while every community module it depends on, at any depth, is free of defects we know of. 23 modules came off the page for that reason. They return when the module they depend on is corrected:

- on `account_payment_batch_oca`: `account_payment_mandate`, `account_payment_sepa_base`, `account_payment_sepa_direct_debit`
- on `account_reconcile_oca`: `account_in_payment`
- on `base_tier_validation`: `account_move_tier_validation`, `base_tier_validation_formula`, `base_tier_validation_forward`, `purchase_tier_validation`, `sale_tier_validation`
- on `ddmrp`: `ddmrp_cron_actions_as_job`
- on `dms_field`: `dms_field_auto_classification`
- on `helpdesk_mgmt`: `helpdesk_mgmt_activity`, `helpdesk_mgmt_crm`, `helpdesk_mgmt_merge`, `helpdesk_mgmt_portal_follower`, `helpdesk_mgmt_sla`, `helpdesk_ticket_partner_response`
- on `l10n_br_account`: `l10n_br_contract`
- on `l10n_br_account`, `l10n_br_purchase`: `l10n_br_purchase_blanket_order`
- on `mgmtsystem_nonconformity`: `mgmtsystem_review`
- on `mis_builder`: `l10n_es_mis_report`, `mis_template_financial_report`
- on `product_configurator`: `product_configurator_sale`

[MODULES.md](MODULES.md) now ends with a table of every dependency that is not in this repository, and why.

Also this evening: `mail_gateway` and `barcode_stock` came back from their web-code correction with all tests passing, including new ones. `mail_gateway` is listed again, with two visible changes written up under "Behaviour changes". `barcode_stock` waits for `barcode_scanner`, which it depends on.

<!-- state --> State at 2:56 am on 20 November: 427 modules listed. Back on the page since the evening correction of 18 November, because they were corrected or the module they depend on was: `account_analytic_distribution_manual`, `account_billing`, `account_in_payment`, `account_move_tier_validation`, `account_payment_mandate`, `account_payment_sepa_base`, `account_payment_sepa_direct_debit`, `account_reconcile_oca`, `automation_oca`, `barcode_scanner`, `barcode_stock`, `base_tier_validation`, `base_tier_validation_formula`, `base_tier_validation_forward`, `connector_importer`, `ddmrp`, `ddmrp_cron_actions_as_job`, `delivery_sendcloud_oca`, `dms_field`, `dms_field_auto_classification`, `document_url`, `l10n_br_contract`, `l10n_br_fiscal_dfe`, `l10n_br_purchase`, `l10n_br_purchase_blanket_order`, `l10n_br_sale`, `l10n_br_sale_blanket_order`, `mgmtsystem_nonconformity`, `mgmtsystem_review`, `partner_statement`, `purchase_tier_validation`, `rma_sale`, `sale_tier_validation`, `stay`, `web_widget_open_tab`. 24 of the modules listed on the morning of 18 November are still off.

### 18 November 2026, late afternoon: values that no longer reach a called template

While correcting `contract` we found that its report and portal templates handed values to Odoo's layout templates in a way Odoo 20 no longer honours (see "a value set inside a `t-call` no longer reaches the called template" below). Nothing had failed: no install error, no failing test.

What we did:

- Wrote a check that runs Odoo's own rewrite script over every server template of every port, in memory, and reports each value that would be lost.
- It found the pattern in 9 more modules. Counting `contract`, that is 10.
- 2 are corrected, each with a new test that opens the page: `contract` and `business_requirement_deliverable`. The portal page of the second failed with an error as soon as a customer opened it.
- 5 that were listed here are off the page until corrected: `account_billing`, `connector_importer`, `l10n_it_delivery_note`, `partner_statement`, `resource_booking`. What a user would have seen: a billing document or a partner statement printed without the address block, a delivery note without its title, a portal page of delivery notes or bookings that fails or loses its breadcrumbs.
- 3 were not listed for other reasons and wait for the same correction: `account_invoice_overdue_reminder`, `account_payment_batch_oca`, `rma_sale`.
- The check now runs on every port before it is listed.

State of the earlier correction at 4:30 pm: 4 of the 35 modules taken off in the afternoon are back, with their web code ported to Owl 3 and their browser tests passing (`contract`, `business_requirement_deliverable`, `web_widget_x2many_2d_matrix`, `web_widget_dropdown_dynamic`). With the 5 above, 36 of the morning's modules are off the page.

### 18 November 2026, afternoon: browser tests had not been running

Until 1:25 pm on 18 November our test machine lacked one Python package, `websocket-client`. Without it Odoo skips every test that needs a browser: a module's tours and its JavaScript unit tests. Our counter recorded a test that skipped itself as run. So for modules with web code, "every test ran and passed" was not true of their browser tests, and nothing had exercised their JavaScript on Odoo 20. This page said otherwise from 17 November until the correction.

What we did:

- Installed the package. Changed the counter: a test that skips itself now counts as not run.
- Ran again every module that carries web code (JavaScript or templates) and every module with a browser test of its own. A module with web code is listed here only after a passing run in which the browser tests really ran.
- 35 modules that were listed here in the morning are off the page. 22 have web code that is not yet ported to Owl 3 (see "the web client runs on Owl 3" below). 6 fail a browser test for another reason, mostly a tour whose steps no longer match Odoo 20's screens. 4 have tests that skip themselves. 3 extend a method Odoo 20 removed. They come back as they pass.
- One caveat on the browser failures: the browser on our test machine is Chrome 122, which is older than Odoo 20 expects. A missing import or an Owl 3 error does not depend on the browser. For a tour that stops at a step, we have not yet ruled out the browser's age as the cause, and we will run those again on a current Chrome.
- 10 of the 38 ports from older versions are off the page as well. The five ports of `contract` fail their tour now that it runs. Five ports of `helpdesk_mgmt` and `base_tier_validation` still contain JavaScript of the old version that the target version cannot load; no test of theirs opens those screens, so they had passed. The JavaScript import check now runs on these ports too, against the source of their target version.

The same afternoon we made the dead-method check look at each model separately (a same-named method on another model had hidden some cases) and added three checks. They found, in modules that passed all their tests:

| What | Modules | State now |
|---|---|---|
| A column added to an analysis report the old way: on Odoo 20 the invoice analysis failed on it, the sales analysis showed it empty | 12 | 9 corrected, each with a new test that reads the column through the report; 3 Brazilian localisation modules are off the page until done |
| A user preference that an ordinary user could no longer change on their own record | 5 | corrected, each with a new test |
| A call to a method Odoo 20 removed (`get_param`, `set_param`, `get_formview_action`), in code the tests did not reach | 10 | corrected; 2 with a new test |
| `pytz` imported without being declared, a package Odoo 20 no longer installs | 19 | declared in the manifest |
| A portal card and an access check written the pre-20 way, in the port of `contract` from 16.0 | 1 | corrected, waiting for its browser run |

Each kind is described under "Things in Odoo 18, 19 and 20 that affect any port". All of these checks now run on every port before it is listed.

## Behaviour changes in the published ports

These ports were in `from-older-versions/` and are withdrawn for a second review since 20 November 2026 (see "Corrections to this page"); the rows stay here as a record of what each change was. In a customer delivery, this is what the change summary would tell you.

| Module | Route | What changed | Why |
|---|---|---|---|
| `helpdesk_mgmt` | 16.0 to 20.0 and 16.0 to 19.0 | A new ticket without an assignee goes to the team leader. In 16.0 it went to the "Assign to" user of the team's email alias. | `mail.alias` no longer has `alias_user_id` (it is gone in both 19.0 and 20.0). The upstream module later dropped the automatic assignment altogether; our port keeps it and uses the nearest field that still exists. |
| `helpdesk_mgmt` | 16.0 to 20.0 and 17.0 to 20.0 | The ticket no longer keeps a CC list (`email_cc`). | Odoo 20 has no `mail.thread.cc` model. Odoo 19 still has it, so the ports to 19.0 keep the CC list. |
| `helpdesk_mgmt` | 15.0 to 19.0 | The alias owner field is gone from the team form and data. | Same removal of `alias_user_id`. |
| `purchase_request` | 15.0 to 19.0 | The allocations are no longer shown inside the transfer form's inline move form. They still show on the move form and on the detailed operations form. | Odoo 19's transfer form has no inline move form (`addons/stock/views/stock_picking_views.xml`). Upstream dropped the same view by 17.0. |
| `account_payment_partner` | 16.0 to 20.0 | Three tests set the company option "keep bank account without payment mode" explicitly instead of relying on its default. | See "A default that never reaches existing records" below. The upstream 19.0 tests do the same. |
| `contract` | 15.0 to 19.0 | Two tests were renamed (`..._fields_view_get` to `..._get_view`), with the same assertions. | `fields_view_get` was replaced by `get_view` in Odoo 16; upstream renamed them the same way. |
| `purchase_request` | 16.0 and 17.0, to 19.0 and 20.0 | One test no longer configures a "fixed procurement group" on a stock rule; it passes the reference on the move instead. | See "Procurement groups are gone" below. The test still checks that a request is reused, or not reused, according to the reference. |

Some ports in [`20.0/`](20.0) have a visible change as well:

| Module | Route | What changed | Why |
|---|---|---|---|
| `project_task_code_portal` | 19.0 to 20.0 | The task code is shown in a column of its own in the portal task list. In 19.0 it replaced the task number Odoo showed there. Two tests reach the portal pages another way. | Odoo 20's portal task list has no number column to replace. For the tests, see "The portal reaches a project only through a collaborator" below. |
| `l10n_it_delivery_note` | 18.0 to 20.0 | The root of the virtual locations is no longer found by itself. It has to be chosen once in the warehouse settings; until then the module says so in an error message. | Odoo removed the "Virtual Locations" parent location the module looked up (`stock.stock_location_locations_virtual` is in 18.0's `addons/stock/data/stock_data.xml` and not in 19.0 or 20.0). |
| `mail_gateway` | 19.0 to 20.0 | Gateway conversations are listed in a "Gateway" tab of the messaging menu. In 19.0 they were a category of the Discuss sidebar. | Odoo 20's Discuss has no sidebar categories. Odoo's own live chat moved to a tab the same way (`addons/im_livechat/static/src/core/public_web/messaging_menu_model_patch.js`). |
| `mail_gateway` | 19.0 to 20.0 | The delivery status of a gateway message shows Odoo's standard status symbols, green when sent and red when it failed. In 19.0 it showed the gateway's brand icon. | Odoo 20 draws a status icon by its name in Odoo's own icon font (`addons/mail/static/src/core/common/message_notification_popover.xml`); an icon class of the old font is not drawn there. |
| `mis_builder` | 19.0 to 20.0 | The report widget takes the id of the report from the record the form shows, and from the action that opened the form only when the form has no record (a dashboard). The 19.0 code could only use the second way. | The 19.0 line read `props.value`, which Odoo has not passed to field widgets since 17.0. The widget sits on the `id` field, so the record's id is the value that line meant. |
| `account_reconcile_oca` | 19.0 to 20.0 | In the reconcile form, a second click on the selected reconcile model clears the selection. | The module's `selection_badge_uncheck` widget is now Odoo 20's own many2one badges widget (`addons/web/static/src/views/fields/badges_many2one/badges_many2one_field.js`), which clears a field that is not required. The badge widget the module extended is gone in 20.0, and its own code for clearing compared the click with `props.value`, empty since 17.0, so as written it could not clear anything. The module's test now checks the second click. |
| `delivery_sendcloud_oca` | 19.0 to 20.0 | Choosing or clearing a service point goes through the form's record (`record.update`), so the change is saved with the record, and the Clear button shows whenever a service point is set. | The 19.0 code assigned the value into `record.data`, which the form does not track, and showed the button on `props.value`, empty since 17.0. jQuery is no longer loaded for the widget (`@web/core/ensure_jquery` is gone in 20.0); the one call that used it is plain JavaScript. |
| `dms_field` | 19.0 to 20.0 | The module carries its own copy of jQuery 3.6.3 (`static/lib/jquery/`, MIT licence beside it) and loads it before its tree library. | Odoo 20 ships no jQuery: `addons/web/static/lib/jquery` and the `web._assets_jquery` bundle the 19.0 module loaded are gone, and the tree library (jsTree) needs it. The file is the one Odoo 19.0 ships, byte for byte. |
| `mgmtsystem_nonconformity` | 19.0 to 20.0 | On a record that has not been saved yet, the Non-conformities button of the chatter saves the record first and then opens the list. | That is what Odoo 20's own chatter buttons do (`saveRecord` in `addons/mail/static/src/chatter/web/chatter_patch.js`). The 19.0 code tested `isTemporary` and called `doSaveRecord`, names Odoo no longer has, so that step never ran. |
| `account_payment_partner` | 18.0 to 20.0 | The module no longer adds the payment mode column to the invoice analysis itself. | Since 19.0 the module it depends on, `account_payment_mode`, carries the same field and adds the column; adding it twice makes the column ambiguous. |

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

One more trap for a module that changes another module's permissions: `project_todo`, which is installed automatically with `project`, ships its own copy of project's task permissions under its own names (`addons/project_todo/security/ir.access.csv`). A module that takes a task permission away from a group has to take away both copies, or the group keeps it.

The same script re-writes the XML files it touches through a parser, which drops the XML declaration and the copyright comment at the top of the file. That had happened in 13 files across 11 of our ports; they are restored, and it is checked on every port.

### In every new version: a method a module extends can be gone, and nothing fails

A module usually adds behaviour by extending a method of the model it inherits: it defines the method again and calls `super()`. When a new Odoo version renames or removes that method, the module still installs and its tests still pass, because nothing calls the old name any more. The feature is just gone. There is no error and no warning.

Some of the renames we met:

| Before | Odoo 20 | File in 20.0 |
|---|---|---|
| `mail.thread._track_template(changes)` | `_track_template_parameters(tracked_fields)` | `addons/mail/models/mail_thread.py` |
| `mail.thread._track_subtype(init_values)` | `_track_log_get_default_subtype(track_init_values)` | `addons/mail/models/mail_thread.py` |
| `toggle_active()` on any model | removed; `action_archive()` and `action_unarchive()` remain | `odoo/orm/models.py` |
| `_prepare_home_portal_values(counters)` in portal controllers | `_prepare_portal_counter_values(counter)` | `addons/portal/controllers/portal.py` |
| `mail.thread._thread_to_store(...)` | `_store_thread_fields(...)` | `addons/mail/models/mail_thread.py` |
| `sale.order.line._is_not_sellable_line()` (18.0) | `_sellable_lines_domain()` | `addons/sale/models/sale_order_line.py` |

We found it in our own ports on 18 November 2026: 9 of 480 ported modules had lost a feature this way, and five of them were on this page, along with the port of `helpdesk_mgmt` made from 17.0.

- `helpdesk_mgmt`: the email template of a stage was no longer sent when a ticket reached that stage.
- `hr_timesheet_sheet`: confirming or approving a timesheet no longer used the module's "confirmed" and "approved" message subtypes, so their followers were not notified.
- `l10n_it_account`: activating Italian from the language list no longer re-applied the Italian name of the accounting menu.
- `mgmtsystem_nonconformity`: the chatter no longer received the number of non-conformities linked to a record, so its button did not show.
- `delivery_fee`: fee lines were no longer left out of the order lines Odoo treats as sellable (the ones it offers for linking to projects, tasks and timesheets).

All five are corrected here and pass their tests again. Three other modules (`account_financial_report`, `base_location`, `l10n_br_coa`) call a parent method that already did not exist in their 19.0 original, so the port neither added nor lost anything there, and they are unchanged.

Every port is now checked for this: each method that calls `super()` has to exist in the source of the target version, and a method that Odoo no longer calls may not be kept alive by the module's tests alone.

### Since 20.0: the portal reaches a project only through a collaborator

In 19.0 a portal user could read a project they followed. In 20.0 the portal permission on `project.project` asks for a collaborator record (`project_project_rule_portal` in `addons/project/security/ir.access.csv`), and every access mode of the share wizard, including "View", creates one. A collaborator who opens `/my/projects/<id>` is sent on to the project sharing view (`portal_my_project` in `addons/project/controllers/portal.py`). So the plain portal task list of a project is now only reached with the project's access token.

The share wizard's email changed too: `project.share.wizard.action_send_mail` sends a sign-up link and no longer a link carrying `access_token`, `pid` and `hash`. Tests that picked those out of the email have nothing to pick.

### Since 20.0: the cards on the portal home page are records

Up to 19.0 a module put its card on `/my` by inheriting the `portal.portal_my_home` template and calling `portal.portal_docs_entry` with a title, a link and a counter name. In 20.0 the cards are `portal.entry` records loaded from a data file (`addons/portal/models/portal_entry.py`; `addons/project/data/portal_entry_data.xml` is an example), and the number on a card comes from `_prepare_portal_counter_values`.

A module that still does it the old way installs without an error, and the page still opens. Its card is just not there, so portal users have no way to reach the module's pages from their home page. A test that opens `/my` and looks for the card's link catches it.

### Since 20.0: a value set inside a `t-call` no longer reaches the called template

Up to 19.0 a template could hand values to the template it calls by setting them inside the call:

```xml
<t t-call="web.external_layout">
    <t t-set="address">...</t>
    <div class="page">...</div>
</t>
```

Odoo 19 already treated this as the old form, and still passed the values on (`ir_qweb.py`, `_compile_directive_call`, the branch named `is_deprecated_version`). Odoo 20 removed that branch. The body of a `t-call` is now rendered later and in its own scope. The called template receives the caller's values as they are at the call, plus the attributes of the `t-call`, and nothing that the body sets. Odoo's own modules were rewritten with `odoo/upgrade_code/19.1-00-t-call.py`:

```xml
<t t-set="address">...</t>
<t t-call="web.external_layout" address="address">
    <div class="page">...</div>
</t>
```

Nothing fails at install, and no test fails unless it renders the template and looks for the value. What a user sees instead: a report without its address block or its document title; a portal list with a plain title where the breadcrumbs were; a portal page that calls `portal.message_thread` and fails with `KeyError: 'object'` when a customer opens it.

Two details:

- An attribute given to an outer `t-call` is not seen by a `t-call` inside its body. Odoo's own portal pages pass `breadcrumbs_searchbar="True"` to `portal.portal_layout` and again to `portal.portal_searchbar`.
- Odoo's script is a good detector. Applied to a file as it is, it dropped the comment above the root element in our runs, which in community modules is the copyright notice. We use it to find the places and write the change by hand.
- Browser templates follow the same rule, and Odoo's script does not look at them (it skips everything under `static/`). In Owl 3 the body of a `t-call` is compiled as a block of its own that the called template may or may not render (`addons/web/static/lib/owl/owl.js`, `compileTCall`), so a `t-set` in that body does not reach the called template either. We found one such template in a port, an onboarding panel that hands each step's title and button text to a sub-template, and check for it in every port now: a `t-set` inside a `t-call` whose value the body itself does not use.

### Since 20.0: Font Awesome is gone

Up to 19.0 every backend, website and report bundle loaded Font Awesome (`web/static/src/libs/fontawesome/css/font-awesome.css` in `addons/web/__manifest__.py`). Odoo 20's bundles include `web.icons_fonts` instead: Material Symbols and Odoo's own icon font. An icon is now an element with the class `oi` and the icon's name in `data-icon`; the stylesheet prints that attribute in the icon font (`addons/web/static/src/webclient/icons.scss`).

What a module written for 19.0 shows on 20.0:

- `<button icon="fa-bars" .../>` in a view: the button's icon is the text of the attribute, so the letters "fa-bars" appear.
- `<i class="fa fa-trash-o" .../>` in a view, a report or a web template: an empty element. If the icon was the whole control (a fold arrow, a delete cross), the control is invisible and cannot be clicked.
- An icon name in a Python dictionary or a JavaScript string (`"icon": "fa-users"`): the same, wherever it ends up.

Odoo converted its own modules with `odoo/upgrade_code/19.5-00-material-symbols-icons.py`; its mapping table is `material_symbols_icons_mapping.py` beside it. Odoo 20's own views have no `icon="fa-..."` left (19.0 has them in 295 view files). The script is a text rewrite and says of itself that it is best effort: class names built at run time and icons stored in data need a look by hand.

No test fails because of this. We now run the script's transforms in memory on every port and treat any file it would change as a defect.

### Since 19.0: a field's search method is called with `in`

Before a field's `search=` method is called, the condition has been normalised: `('f', '=', v)` arrives as `('f', 'in', {v})` and `('f', '!=', v)` as `('f', 'not in', {v})` (`odoo/orm/domains.py`, `_operator_equal_as_in`). If the method raises `NotImplementedError` or a `UserError`, or returns `NotImplemented`, Odoo tries the opposite operator and then calls the method once per value with `=` or `!=` (`_optimize_field_search_method` in the same file). So a method that refuses what it does not know keeps working.

A method that answers anyway does not. This one, written during a port, returns the opposite of what was asked for, because it never sees `=`:

```python
def _search_has_weight(self, operator, value):
    return domain if (operator == "=") == bool(value) else ~domain
```

`bool({True})` and `bool({False})` are both true, so a search for records with the flag set returns the ones without it. No test of that module searches on the field. We found it by reading, and now flag every search method a port wrote or changed that compares the operator with `=` and never mentions `in`. A method left exactly as the 19.0 author wrote it is not flagged: it behaves on 20.0 as it did on 19.0, right or wrong.

### Since 20.0: the web client runs on Owl 3

Odoo 20 ships Owl 3 (`addons/web/static/lib/owl/owl.js`) with a compatibility layer for older component code (`addons/web/static/src/owl2/owl3_compatibility_layer.js`). Three things in it break a module's JavaScript, and no Python test notices:

- A component that declares `static props` or `static defaultProps` throws when it is created. The layer's `Component` constructor raises the error itself. Properties are declared in the instance, `props = useProps({ name: t.string().optional() })`, as in `addons/web/static/src/core/checkbox/checkbox.js`.
- Owl no longer exports `useState`, `useRef`, `reactive`, `onRendered` or `useExternalListener`. Odoo 20's own code does not import them anywhere; it uses `signal`, `proxy` and `signal.ref()`. A component written with the old hooks has to be rewritten with these.
- Old template directives and hooks have to be renamed for the layer: `t-portal` to `t-custom-portal`, `t-model` to `t-custom-model`, `useEffect` to `useLayoutEffect` (the header of the layer file lists them).

Files moved as well. These import paths exist in 19.0 and not in 20.0: `@web/core/orm_service`, `@web/core/ui/ui_service`, `@web/webclient/actions/action_service`, `@web/legacy/js/public/public_widget`, `@web/core/ensure_jquery`, `@web/views/kanban/kanban_compiler`, `@web/views/fields/badge_selection/badge_selection_field` (the badge widgets are now under `badges_selection` and `badges_many2one`), `@mail/chatter/web_portal/chatter`, and `@mail/core/common/record` (now `@mail/model/record`). With such an import the browser reports "The following modules are needed by other modules but have not been defined", and the code that depends on it does not load.

Only a test that opens a browser sees any of this: a tour or a JavaScript unit test of the module. A module without one can install and pass every test with web code that does not load. See "Corrections to this page" for what that meant for us.

### Since 20.0: the analysis reports are built from lists of columns

`account.invoice.report` and `purchase.report` are built by `_table_sql()` from `_select_list(table)` and, for purchases, `_groupby_list(table)`. `sale.report` is built from `_select_dict(table)` and `_groupby_list(table)`. The methods modules used to extend, `_select`, `_from`, `_where`, `_group_by`, `_select_additional_fields` and `_group_by_sale`, are gone (`addons/account/report/account_invoice_report.py`, `addons/purchase/report/purchase_report.py`, `addons/sale/report/sale_report.py`).

A module that still extends the old methods installs, and its tests pass. On the invoice analysis, reading the module's field fails with "column does not exist". On the sales analysis the field is simply empty, because a field the dictionary does not contain is filled with NULL. Odoo's own modules show the new way: `addons/l10n_latam_invoice_document/report/invoice_report.py`, `addons/project_purchase/report/purchase_report.py`, `addons/sale_stock/report/sale_report.py`.

One trap on top: a same-named method that survives on another model hides the problem from a check by name. `_select_additional_fields` is gone from `sale.report` and still exists on `event.sale.report`.

### Since 20.0: a field users may change on their own record is marked on the field

`res.users` has no `SELF_READABLE_FIELDS` and `SELF_WRITEABLE_FIELDS`. A field that a user may change on their own user record is declared with `user_writeable=True` (`_has_field_access` in `odoo/addons/base/models/res_users.py`). A module that still extends the two lists installs, and an ordinary user who changes that preference gets an access error. Tests that run as the administrator do not see it.

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
- A tour started by a test no longer goes to the tour's own `url`. In 19.0 the tour service redirected to the `url` the tour was registered with (`addons/web_tour/static/src/js/tour_service.js`). In 20.0 it redirects only to a `url` given in the start options (`addons/web_tour/static/src/tour_plugin.js`), and `start_tour` in `odoo/tests/common.py` gives none. A test that opened `/` and let the tour find its page now waits on the wrong page until it times out; it has to open the tour's page itself.
- `ir.config_parameter` has no `get_param` and `set_param` in 20.0. Use the typed pairs: `get_str`/`set_str`, `get_int`/`set_int`, `get_bool`/`set_bool`, `get_float`/`set_float` (`odoo/addons/base/models/ir_config_parameter.py`). A call left in a controller, a wizard or a button method only fails when a user gets there.
- No model has `get_formview_action()` in 20.0; `_get_records_action()` returns the same kind of action (`odoo/addons/base/models/ir_ui_view.py`). `check_access_rights()` and `check_access_rule()` are gone too; `has_access(operation)` and `check_access(operation)` remain (`odoo/orm/models.py`).
- Odoo 20 no longer installs `pytz` and `xlwt` (they are in 19.0's `requirements.txt` and not in 20.0's; Odoo itself moved to `zoneinfo`). A module that imports `pytz` works on a machine that happens to have it and fails to load on a clean Odoo 20, unless its manifest declares it under `external_dependencies`.
- In 20.0, tests built on `BaseCommon` run as a test user who has only the internal user group, unless the class sets `_test_user_groups` (`odoo/addons/base/tests/common.py`). A test that passed as the superuser can fail on access for that reason alone.
- The published `odoo-test-helper` package does not load fake models on 20.0, because the registry internals it uses changed (`MetaModel.module_to_models` is now `_module_to_models__`, and `Registry.load` no longer takes a cursor). The four ports that need it carry an adapted copy of its loader in their `tests/` folder, with the original copyright and licence lines.
