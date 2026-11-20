# Notes

Two kinds of note: behaviour that changed in a published port because Odoo removed something, and things we found in Odoo 18, 19 and 20 that affect any port. Every statement about Odoo below was checked in the Odoo source code; the file is named so you can check it too.

## Corrections to this page

### 20 November 2026, 10:35 am: a row of our own checklist that we had not applied to the Odoo 20 list

The checklist says: since 18.0, Duplicate in a list view copies every selected record in one call, so a
`copy()` that begins with `ensure_one()` works from the form and raises "Expected singleton" from the list.
We check every port from an older version for it. We had not run that check over the Odoo 20 list, where the
same code simply comes along from the 19.0 original. It was in seven places in six modules we work on, among
them two that carry a passed second review, `mis_builder` and `helpdesk_mgmt`.

Corrected in all six: the override now copies the records one by one through the same method, so what it
does for one record is unchanged, and each record gets its own copy of the defaults (the helpdesk override
writes the new ticket number into them). For the two reviewed modules there are tests that select two
records and duplicate them; they failed with "Expected singleton" before the change. `mis_builder` 102 test
runs, `helpdesk_mgmt` 39. The check now runs on every module for Odoo 20 and holds a module back.

While reading findings one by one before telling anyone about them, we also found a false alarm in our
check for `group_expand` methods: it counted an argument that has a default value (`order=None`) as
required. Such a method works when Odoo passes two arguments. The check is corrected; nothing on this page
was affected.

### 20 November 2026, 10 am: on Odoo 20, reports printed the wrong company's letterhead

This one is about Odoo 20 itself, and it concerns every report that was written for 19.0.

The standard page layouts (`web.external_layout`, `web.internal_layout`) put the company's logo, address and
VAT number around a document. They choose the company themselves when the report does not name one: the
document's own company first, the user's company last. That choice only runs when no `company` value exists.
Odoo 20 gives every template a `company` value from the start, the company the user is currently working in.
So the choice never runs, and a report that simply calls the layout prints the letterhead of whoever prints it.
In a database with one company nobody notices. In a database with several, an order of company B printed from
a session in company A goes out under A's name.

We did not take this from reading alone. One report, one contact that belongs to a second company, printed
through the report engine on both versions: Odoo 19 put the second company in the header, Odoo 20 the first.
With the company passed in the call, Odoo 20 prints the second again. Odoo's own invoice and sale order do
pass it; most of its other reports do not.

23 of our Odoo 20 modules call a layout this way (some of them are still held for other reasons).
Each call now names the company: one the report chose itself, else the document's, else the user's, which is
what 19.0 did. Each module's tests were run again and pass. 3 modules have such a call in a template where we could not tell mechanically
which record is the document; they are held until someone has read them. The second reviewer found this in
`account_credit_control`; the check and the experiment came from that one finding.

`account_reconcile_oca` is back on the Odoo 20 list: its second read found four of the five faults of the
first fixed, and what is left concerns its tests only (a browser test class that also runs under other
modules' test tags, and two new browser tests that assert less than their names say).

The class-name check of 8:45 am was too narrow, as a re-read showed: it missed names inside a computed
class (`t-att-class="'font-weight-bold' if ..."`) and the responsive forms (`pl-sm-0`, `text-md-right`).
Widened; seven more modules for Odoo 20 and the `contract` and `helpdesk_mgmt` ports to 19.0 were corrected
and tested again. `contract`'s portal stylesheet also used a colour function Bootstrap 5 does not have
(`gray("800")`) and a breakpoint that means something narrower in Bootstrap 5; both corrected, in the
Odoo 20 module and in the port to 19.0.

Two more ports from older versions are listed as of this note: `sale_automatic_workflow` 17.0 to 19.0, where
the third full read found nothing left to change, and `partner_firstname` 17.0 to 19.0, with one point that is
the 17.0 original's own behaviour: a company created from a "Create and edit" dialog keeps the name the dialog
was opened with, even if the user changes it there. The original's own test pins that behaviour, so the port
keeps it; the maintainers changed both in their 19.0.

### 20 November 2026, 8:45 am: a batch of new checks, and what they found in ports already on this page

The second reviewer read four more older-version ports this morning (`contract` 16.0 to 19.0, `auditlog` 15.0 to
18.0, `base_tier_validation` 16.0 to 19.0, `partner_firstname` 17.0 to 19.0). None of the four is on this page;
one was rejected outright. As before, every finding that a program can look for became a check, and the checks
ran over everything that is on the page. This is what they found here and what we changed.

**A gap in our own pipeline.** For ports to 18.0 and 19.0 no check ever looked at the JavaScript; that check ran
for Odoo 20 targets only. The rejected port had kept nine script files on the 16.0 mail framework: nothing
loaded in the browser, every Python test passed, and our pipeline said PASS. The check now runs for every
target. The five older-version ports on this page come out clean under it.

**Older-version ports on this page.**

- Bootstrap 4 class names (`text-right`, `ml-auto`, `font-weight-bold` and so on) were still in the report of
  `purchase_request` 16.0 to 19.0 (4), in the report, portal pages and wizards of `contract` 17.0 to 19.0 (36)
  and in the portal pages of `helpdesk_mgmt` 17.0 to 19.0 (14). Odoo has defined none of them since Bootstrap 5:
  right-aligned amounts were left-aligned. Renamed; the tests pass as before (40, 119, 38).
- `auditlog` 15.0 to 19.0, two corrections. With a rule that logs reads, every change of a field in a form wrote
  an empty "read" entry, because the web client reads the form's unsaved copy through `read()` since 17.0. And
  deleting a rule that had never been subscribed removed another module's patch of the same method (automation
  rules patch `create`, `write` and `unlink` too) and then raised an error; that one is as old as the 15.0
  original. Both are shown by tests that failed before the correction. 42 test runs pass. Not changed, and the
  same in the maintainers' own version: `search_read()` no longer goes through `read()`, so a read made through
  that method is not logged.
- `partner_firstname` 17.0 to 18.0: after "Recalculate names" in the settings, the contact list kept showing
  the old order, because the stored complete name was not told that the name had changed. The 17.0 original has
  the same gap. One line, and a test that failed before it. 67 test runs pass.

**The Odoo 20 list.**

- The same Bootstrap 4 names are in the maintainers' own 19.0 code of 48 of the 392 modules we checked. We
  renamed them in 46 modules here and ran each module's tests again. Modules still held for other
  reasons get the same when they return.
- Three modules posted chatter messages built as plain HTML strings, which Odoo has shown with their tags since
  17.0: `contract_sale_generation`, `hr_course`, `l10n_it_edi_doi_extension`. They build markup now, with
  every value escaped. The 19.0 originals do the same as before.
- `contract`: the portal's fallback avatar pointed at a file that moved (`/web/static/img/...`).
- `partner_firstname`: on the user form, the first-name and last-name fields were hidden for every user whose
  login is their e-mail address, while the name itself is read-only. The module adds them "after the email
  field", and Odoo 20 put that field into a container with a condition of its own. They now follow the heading
  that holds the name. A test reads the form and fails on the old placement. The settings action described
  above is corrected here too. 43 test runs pass.
- `purchase_exception`: the "Ignore Exceptions" checkbox, meant for confirmed orders, was inside a container
  that Odoo 20 hides on confirmed orders, so nobody ever saw it. It now sits in the group that holds the order
  date, with a test.
- The check that found the last two compares, for every view extension, where its anchor sits in Odoo 19's
  form and in Odoo 20's. It reported nine modules whose additions now sit under a new condition. Two are the
  ones above. Seven were read and left as they are, because the new condition suits what the module adds
  (`ddmrp`, `stock_move_common_dest`, `hr_timesheet_time_control`, `l10n_es_verifactu_oca`,
  `partner_contact_job_position`, `product_simple_seasonality`, `stay`).
- Open, not yet corrected: the same check shows nine modules whose added fields used to sit in a group, where
  a field gets its label, and no longer do in Odoo 20's rebuilt forms: `delivery_sendcloud_oca`,
  `fieldservice_project`, `l10n_br_account`, `l10n_br_base`, `l10n_es_partner`, `mail_activity_board`,
  `mail_activity_team`, `project_forecast_line`, `sale_stock_picking_invoicing`. The fields are there and work;
  some may show without a label. We are going through them.
- Fourteen modules build their settings screen from the old `<div class="o_setting_box">` blocks, as their
  19.0 originals do. The options show and work; the search box of the Settings screen does not find them.
  Not changed yet.

### 20 November 2026, 7:20 am: `contract` for Odoo 20 is back

Rejected at 5:15 am (below), fixed, read again. All five faults of the first read are dealt with: the pricelist dropdown gets a valid domain in every case, and the test checks what the screen receives; section and note rows on contract lines show and can be edited, written the way Odoo 20's own invoice lines are; each access right exists once; the portal card is no longer overwritten on update; and the module's tests run as an accounting user instead of the superuser, which is what found the next two points in the modules that build on it.

The second read left four points, and all four were things the fix had added or changed beyond the brief: a product had become mandatory on every line (19.0 does not require one); the description column could be switched off, which would have emptied every section row; an XML id that the maintainers ask other modules to rely on had been dropped; and an upgrade script had been added that looks up a model Odoo 20 does not have. We corrected the four by hand. 77 test runs pass.

Modules that build on `contract` should know two things. Its line list now holds product and description in one column named `product_and_description`, so a view that hooked onto `.../list/field[@name='product_id']` has to hook onto the column or look for the field at any depth; `l10n_br_contract` here needed that. And its test classes now run as a user with accounting rights, so a dependant's test that needs more (a company setting, a group of its own) has to say so; `contract_termination` and `contract_line_successor` here needed that. All nine dependants were tested against the corrected module before any of them returned. `contract_sale` stays off the page for its access rows (6:30 am, below).

### 20 November 2026, 6:30 am: nine more modules read in full; six rejected, and a class of access fault

The second reviewer read the complete 19.0 to 20.0 change of nine more of the larger modules on this list. One came back without a finding (`account_asset_management`, now marked `passed`). Two were accepted with changes (`fieldservice`, `ddmrp`). Six were rejected: `rma`, `account_reconcile_oca`, `automation_oca`, `payroll`, `account_credit_control`, `edi_core_oca`. All eight with findings are off the page, with the modules that depend on them, until the findings are fixed and the module has been read again. What we have checked ourselves so far:

- **`account_credit_control`: access to every message.** The 19.0 module gives its three groups plain rights on `mail.message`. On 19.0 that was harmless, because what a user may read there was decided elsewhere. In Odoo 20 a right and its limit are one row, the rows of all a user's groups add up, and Odoo's own rows on `mail.message` all carry a domain (`addons/mail/security/ir.access.csv`). The converted rows carry none. A credit control user could have read every message in the database. This is the conversion doing what Odoo's script does; our comparison of record rules did not look at rows on models of other modules.
- **`rma`: one view silently replaced another.** Two views of the module carry the same XML id, so the one loaded later overwrote the first, and the fields that start an RMA from a return were gone from the transfer form. Its report also sets the address inside a condition inside the `t-call` body, a nesting Odoo's conversion script and therefore our check both skip, so the report printed no address.
- **`account_reconcile_oca`:** its controllers call `this.render(true)`, which an Owl 3 component does not have, and its JavaScript calls the server method `get_formview_action`, which Odoo 20 renamed. Both sit on paths the module's browser tests do not walk.
- **`fieldservice`, `automation_oca`, `rma` and four small modules: dead card menus.** In a kanban view, Odoo 20 reads the card's menu from a template named `menu` (`addons/web/static/src/views/kanban/kanban_record.js`), and a link with `type="edit"` is no longer an action (`addons/web/static/src/views/card/card_compiler.js`); it is `type="open"`. The old names install and do nothing.

**The access fault as a class.** We wrote a check for it and ran it on every port: an access row that gives a group a right without a domain on another module's model, where Odoo 20's own rows limit that model by domain. Twelve of our ports have such rows, on models like `sale.order`, `account.move`, `crm.lead`, `product.template` and `mail.message`. For most of them the effect is narrower than for messages: a user who holds the module's group and also a limited group of the owning app sees more than on 19.0. All twelve are off the page until each row has been read against the 19.0 rights.

**Dead card links corrected in three small modules** (`base_kanban_stage`, `iot_oca`, `mgmtsystem_action`), which stay listed; their tests pass.

Where this leaves the list: every module on it still installs and passes its own tests, and of the fifteen larger ones that have now been read in full, fourteen had at least one fault the tests do not show. The second-review column in [MODULES.md](MODULES.md) is the one to go by.

### 20 November 2026, 6 am: `contract` 17.0 to 19.0 is listed (not to be confused with the Odoo 20 one)

Two ports of `contract` are in play and they stand differently. The port from 19.0 to 20.0 was rejected an hour ago and is off the page (5:15 am, below). The port from 17.0 to 19.0 has now been read twice and is listed under older versions.

Its first read accepted it with six changes: choosing a product on a contract line could raise an error or keep a unit the line does not allow; the supplier line list was never selected because the code still asked for a view of type `tree`; searches through the contract no longer skipped the contract's record rules as the 17.0 module made them do; a fallback picture pointed at a file Odoo moved; and three calls were deprecated. All six are fixed and the second read confirmed five outright.

What the second read added, and what we did with it:

- The supplier line list hid one column with `invisible`, which since 17.0 leaves an empty column. Corrected to `column_invisible`.
- A new test of ours ran at the wrong moment of the installation. Corrected.
- Not changed, and listed below as an inherited limitation: the module picks a special form and list for supplier contract lines by looking at a value in the action's context. The web client sends only the language and view references when it loads a view, so that value never arrives and the special views are not used from the screen. The 17.0 module has the same mechanism and so has the maintainers' 19.0 version. Making it work would mean designing it anew, which is not a port.

119 test runs pass.

### 20 November 2026, 5:30 am: `purchase_request` is off the Odoo 20 list; two icon forms our check did not see

**`purchase_request`, 19.0 to 20.0, rejected by the second reviewer.** Two of its findings we have checked in the source, and both hold.

- When a request is turned into a purchase order, the wizard looks for an existing purchase line it can add the quantity to, and it finds that line by its text: the product's name, plus the purchase description. In Odoo 20 the line's `name` holds the purchase description only; the product's name moved to a new field, `label` (`addons/purchase/models/purchase_order_line.py`). So nothing matches any more, and every request line becomes a new purchase line instead of joining the one that is there. No test of the module counts the purchase lines.
- The module overrides `_prepare_stock_moves(self, picking)`. Odoo 20 made that argument optional (`addons/purchase_stock/models/purchase_order_line.py`) and has callers that leave it out; with the module installed those calls fail.

Three more findings are not verified yet (a checkbox on the product form that Odoo 20's layout hides, wider read access for users who hold two of the module's groups, a test that leaves the table changed). One finding we do not count as a fault: the port declares `pytz` as a Python dependency where the review would have replaced it by `zoneinfo`. A module that needs `pytz` says so in its manifest on this page; see "Small ones" below.

`purchase_request` and the modules that depend on it are off the list. Note the difference to the port of the same module from 16.0 to 19.0, which is listed under older versions and has been read three times: that is another port to another Odoo version.

**Two icon forms our check did not look at.** The review of `base_tier_validation` accepted the module with three changes, and two of them were icons, in forms that Odoo's conversion script does not handle and that our check, which runs that script, therefore never saw: an icon name stored in a data record (`<field name="icon">fa-bell</field>` on an activity type; `mail.activity.type.icon` is a Material Symbols name in Odoo 20), and a style rule that prints a glyph from the Font Awesome font (`font-family: FontAwesome; content: "\f0d7"`), which shows as an empty box because Odoo 20 does not load that font. Both forms are now reported. Across all ports we found them in six modules and corrected them: five activity-type icons and two style rules. One of the style rules was our own doing: Odoo's script had renamed a selector from `.fa` to `.oi` in `l10n_it_delivery_note` and left the rule's body, which then forced a text font onto icon elements. In `base_tier_validation` we also switched off the bottom sheet on the systray menu, as Odoo 20's own systray menus do. With the three points corrected and its 72 test runs passing, the module is marked `passed` in [MODULES.md](MODULES.md); the corrections were made after the read.

### 20 November 2026, 5:15 am: `contract` is off the Odoo 20 list

The second reviewer read the complete change of `contract` from 19.0 to 20.0 and rejected it. We checked its first finding in the Odoo source and it holds.

The contract form limits the pricelists a user can pick to the journal's currency, through a computed field that holds the domain. The port changed that field's type to `Json`. A `Json` field stores an empty list as nothing and gives back `False` (`odoo/orm/fields_misc.py`, `convert_to_cache`). The domain is empty whenever the journal has no currency of its own, which is the normal case. The view hands that `False` to the web client as the field's domain, and the web client cannot build a domain from it (`addons/web/static/src/views/fields/field.js`, where the field's domain is evaluated; `core/domain.js`, `toAST`). So opening the pricelist dropdown on an ordinary contract fails. The module's test for this had expected an empty list on 19.0; in the port it expected `False`. That change went through our review of changed tests, and should not have: the value the test checks is the value the screen uses.

The review lists four more points we have not verified yet: section and note rows of the contract lines that show nothing, because Odoo 20's list for such rows wants a column the views do not have; two access rights written twice; a portal card whose settings are overwritten on every update; and tests that opt out of Odoo 20's ordinary test user.

`contract` and the modules that depend on it are off the page until these are fixed and the module has been read again.

### 20 November 2026, 5 am: `helpdesk_mgmt` for Odoo 20 is back, with the modules that build on it

The first read had rejected it with nine faults, most of them on the customer portal: the ticket page had lost its whole sidebar (the case our template check could not see, described under 3:30 am below), the assignee and customer cards were empty because Odoo 20 renamed three arguments of `portal.portal_my_contact`, the ticket list had lost its breadcrumbs, the page printed its "Communication history" heading twice, and a customer with no ticket yet no longer saw the Tickets card and so had no way to create the first one. In the backend, two list columns used a date widget Odoo 20 renamed (`remaining_days` is `relative_date` now), a dashboard tile lost its filled icon, and the dashboard did not follow the window size because its resize listener was not bound to the component.

All nine are fixed, and the portal ones are now covered by tests that open the pages as a portal user. The second read confirmed eight and left two small points, which we corrected: an empty element the fix had left in the page, and a tag on the browser-test class. One thing we took back from the fix: it had mapped a screen size that no longer exists (`VSM`) onto the next one, which changed the dashboard to three columns on small tablets. On 19.0 that case never matched, because Odoo 19 has no such size either, and the dashboard showed four columns. It shows four.

One thing an inheriting module should know: on 19.0 the call to the sidebar template carried `id="helpdesk_ticket_portal_sidebar"` as a hook. On Odoo 20 an attribute of a `t-call` is a value handed to the called template, so the id is gone; hook onto the `t-call` itself.

38 test runs pass. The eight modules that depend on `helpdesk_mgmt` were tested again against the corrected version; the six of them that have tests of their own are listed again.

### 20 November 2026, 4:30 am: `mis_builder` is the first module on the Odoo 20 list with a passed second review

The first read of `mis_builder` had rejected it with four faults (see "a second review of the Odoo 20 list has begun" below). All four are fixed and each has a test:

- A query that sums stored fields asks Odoo 20 for the sums the way Odoo 20 wants to be asked. We kept the rest of that code exactly as 19.0 had it: only sums are done in SQL, each field with its own aggregator, and a field that cannot be summed is reported and left empty. The first fix had moved minimum, maximum and average into SQL as well, which 19.0 never did; we took that back.
- An expression that mixes accounting modes (an initial balance plus a period balance) drills down to the move lines of both again.
- The wide-display button has an icon, and the browser test checks it before and after a click.
- The access file Odoo 20 no longer loads is gone, after each of its 23 rights and the company rule was found in the new file.

The second read confirmed the four and found nothing else. 100 test runs pass. `mis_builder` and two of the three modules that depend on it are listed again, and [MODULES.md](MODULES.md) shows `passed` in its second-review column for `mis_builder`, the only module there so far.

### 20 November 2026, 4:15 am: `helpdesk_mgmt` 17.0 to 19.0 is back

This is the port whose first review made us withdraw all the others (see "ports from older versions withdrawn" below): its kanban views would not open on Odoo 19, grouping tickets by stage raised an error, and loading a ticket's suggested recipients raised another. It has now been read three times.

- All six faults of the first read are fixed, and the second read confirmed each one: the three kanban views use the `card` template, the stage method takes the two arguments Odoo 19 passes, the old recipients override is gone (Odoo 19 handles the customer and a bare email address itself), the forms use `<chatter/>`, several tickets can be duplicated at once and each copy gets its own number, and three deprecated calls are replaced.
- The second read also found a fault that is in the 17.0 module itself: a ticket created from an incoming email got the email's subject as its number, because the number is the record's name field and Odoo's mail gateway fills that with the subject. The port now leaves the number to the sequence. It is listed below as a behaviour change.
- The third read found that one of the new tests read a view through the wrong model. Corrected.
- Two points we did not act on. Mass mailings sent from the composer do not use the team's alias as reply-to; Odoo 19's own project, CRM and recruitment apps override the same method in the same way (`_notify_get_reply_to`, while the composer calls `_notify_get_reply_to_batch`), so this is how Odoo 19 behaves, not something the port lost. And the team form shows the alias domain read-only, as the 17.0 module does.

38 test runs pass.

### 20 November 2026, 4 am: two more older-version ports back, and a mistake of ours the review caught

**`purchase_request`, 16.0 to 19.0, read three times.** The first read listed nine faults, among them the old chatter block on both forms, a crash in procurement when a move has no destination moves, icon names of Odoo 20 that Odoo 19 shows as broken images, and a date comparison that duplicated purchase lines for users outside UTC. Two rounds of fixes dealt with those and each fix has a test. The third read left two points, and both are worth telling.

- *The vendor's minimum quantity.* In 16.0 a vendor price had no unit of its own; its minimum was in the product's purchase unit, which was also the unit of the purchase line, so the module compared the two numbers as they stood. In 19.0 a vendor price has its own unit (`product_uom_id` on `product.supplierinfo`, `addons/product/models/product_supplierinfo.py`) and the minimum is expressed in it. After the first read we told the engineer to "do no conversion the original did not do". That was wrong: the original did not need one, Odoo 19 does. With a vendor minimum of 5 dozen the port ordered 5 units, and a test asserted it. The third read said so. The port now converts the minimum to the purchase line's unit (60 units), and the test checks that.
- *Grouping request lines by analytic distribution.* The 16.0 search view offers it. Odoo 19's analytic mixin supports that grouping for four of its own models and with the record count only (`addons/analytic/models/analytic_mixin.py`, `_get_count_id` and `_read_group_select`); a list view also asks for sums, and the mixin refuses. Two attempts to make it work for request lines each came back half working. We removed them and the group-by option with them. That is a loss against 16.0 and it is listed below under behaviour changes.

Also changed: duplicating several requests at once from the list now works (see "Since 18.0: `copy()` is called with several records"). 39 test runs pass. The last corrections were made by us after the third read.

**`partner_firstname`, 17.0 to 18.0, read twice.** This is our first port to 18.0. The first read found that duplicating several contacts or several users at once raised an error, that a company created through the "Related Company" field had its name split into first and last name, and that the module's error message was translated without a language. All fixed, with tests; the second read confirmed three and found the fourth half done (the values for a copied company were only right when they went through `copy()`), which we finished. 66 test runs pass. One thing the second read pointed at is unchanged because the 17.0 module does the same: when a contact is duplicated with an explicit first or last name, the module overwrites one of them with "(copy)".

**A renamed setting, in 11 listed modules.** The review of another port (17.0 to 19.0) pointed at the precision name for quantities, which Odoo renamed in 19.0. 15 of our Odoo 20 ports still asked for the old name, in 44 places, all carried over unchanged from their 19.0 originals; 11 of the 15 are listed here. The old name silently means two decimals. We renamed it in all 15 and their tests pass again; see "Since 19.0: the precision for quantities has a new name" below.

**This page's own statements were checked too.** [CHECKLIST.md](CHECKLIST.md) is new: one page of the cases where nothing fails and the module is still broken. Before publishing it we had every row checked against the 18.0, 19.0 and 20.0 source by a reviewer who had not written it. Three rows were wrong and are gone (two described failures that are loud, not silent; one named the wrong version), and six were reworded. The same check corrected three statements in these notes: what replaces `get_formview_action()`, when `is_company` is really overwritten, and what a portal card written for 19.0 does on 20.0.

### 20 November 2026, 3:30 am: a blind spot in our template check, and the first older-version port back

**The blind spot.** The second review of `helpdesk_mgmt` said the portal ticket page still set values inside a `t-call` body, and our check had called the module clean. Both were true. Our check is built on Odoo's own conversion script, and that script leaves alone any `t-call` that carries an attribute not starting with `t-` (`odoo/upgrade_code/19.1-00-t-call.py`, the first test in `change`): in Odoo 20 such an attribute is a value for the called template, so the script takes the call for converted. A 19.0 template could carry an ordinary attribute there, an `id` for inheriting views or a `groups` rule, and then nobody looked at its body. Our check now judges those calls like any other.

Run over every port, it found two modules: `helpdesk_mgmt`, already off the page, and `sale_elaboration`, which was listed. Its delivery slip and picking report called the module's notes template with `groups=...` on the call and the record set in the body, three times; on Odoo 20 the template did not receive the record. The three calls now pass it as an attribute and the module's tests pass again. None of its tests prints those reports, so the tests could not have told us.

**The first older-version port back: `auditlog`, 15.0 to 19.0.** It was read twice.

- First read, three findings to act on. The 15.0 fields of a rule were read-only once the rule was subscribed, through `states=` on each field; that parameter is gone and the port had not moved the rule to the form view, so a subscribed rule could be edited. Fixed, with a test on the view. Creating several subscribed rules in one call hooked only the first, because `any()` stops a generator at the first true value. Fixed, with a test that creates two rules together and checks that both models are logged.
- The third finding was that the module reads the logged values through `sudo()` into the cache every other user's code shares. The fix that came back wrapped those reads in a helper that swaps the transaction's cache dictionaries for the duration, modelled on what the maintainers' 19.0 version does. The second read called that helper unsafe on Odoo 19. We checked two of its reasons and both hold: environments keep their own cached references to two of those dictionaries (`odoo/orm/environments.py`, `_field_dirty` and `_protected` are cached properties), and one of the dictionaries is a `StackMap` (`odoo/tools/misc.py`), where emptying a shallow copy empties the original too; we ran that one. We took the helper out. The port reads the values exactly as the 15.0 module does. The shared cache the finding describes is therefore the original's own behaviour on 15.0 as well, carried over and not changed by us.
- Six tests that had come with the helper tested its internals. They are replaced by the two behaviour tests named above.

40 test runs pass. It is one port, and the only one on this page that has been through a second review.

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

<!-- state --> State at 10:36 am on 20 November: 406 modules listed. Back on the page since the evening correction of 18 November, because they were corrected or the module they depend on was: `account_analytic_distribution_manual`, `account_billing`, `account_in_payment`, `account_move_tier_validation`, `account_payment_mandate`, `account_payment_sepa_base`, `account_payment_sepa_direct_debit`, `account_reconcile_oca`, `barcode_scanner`, `barcode_stock`, `base_tier_validation`, `base_tier_validation_formula`, `base_tier_validation_forward`, `connector_importer`, `delivery_sendcloud_oca`, `dms_field`, `dms_field_auto_classification`, `document_url`, `helpdesk_mgmt`, `helpdesk_mgmt_activity`, `helpdesk_mgmt_crm`, `helpdesk_mgmt_merge`, `helpdesk_mgmt_portal_follower`, `helpdesk_mgmt_sla`, `helpdesk_ticket_partner_response`, `l10n_br_contract`, `l10n_br_fiscal_dfe`, `l10n_br_purchase`, `l10n_br_purchase_blanket_order`, `l10n_br_sale`, `l10n_br_sale_blanket_order`, `l10n_es_mis_report`, `mgmtsystem_nonconformity`, `mgmtsystem_review`, `mis_builder`, `mis_template_financial_report`, `partner_statement`, `purchase_tier_validation`, `resource_booking`, `sale_tier_validation`, `stay`, `web_widget_open_tab`. 45 of the modules listed on the morning of 18 November are still off.

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

These ports were in `from-older-versions/` and were withdrawn for a second review on 20 November 2026 (see "Corrections to this page"); the rows stay here as a record of what each change was. [OLDER_VERSIONS.md](OLDER_VERSIONS.md) lists the ones that have returned. In a customer delivery, this is what the change summary would tell you.

| Module | Route | What changed | Why |
|---|---|---|---|
| `helpdesk_mgmt` | 17.0 to 19.0 | A ticket created from an incoming email gets its number from the sequence, like any other ticket. In 17.0 it got the email's subject as its number. | `number` is the model's name field, and the mail gateway fills the name field with the subject unless the module says otherwise (`addons/mail/models/mail_thread.py`, `message_new`). The module now does. |
| `contract` | 17.0 to 19.0 | Not changed, and worth knowing: the special form and list for supplier contract lines are not used when the lines are opened from the screen. | The module chooses them in `get_view` by the context key `default_contract_type`. The web client sends only `lang` and keys ending in `_view_ref` when it loads a view (`addons/web/static/src/views/view_service.js`), so the key never arrives. The 17.0 original works the same way. |
| `contract` | 17.0 to 19.0 | Choosing another product on a contract line always sets the line's unit to that product's unit. In 17.0 the unit was kept when both units were of the same category. | Odoo 19 has no unit categories; its own invoice lines take the product's unit (`addons/account/models/account_move_line.py`). Keeping the old unit could leave one the line does not allow. |
| `purchase_request` | 16.0 to 19.0 | Names in the module's chatter messages (request, order, transfer, location, requestor, unit, product) are shown as text. In 16.0 they went into the message as HTML. | Since 17.0 a plain string posted to the chatter is escaped as a whole, so the port builds these messages as markup; every value that goes into them is escaped first. |
| `purchase_request` | 16.0 to 19.0 | Request lines can no longer be grouped by analytic distribution; the option is gone from the search view. Filtering and showing the distribution are unchanged. | Odoo 19's analytic mixin offers that grouping for four of its own models and with the record count only (`addons/analytic/models/analytic_mixin.py`). A list of request lines also asks for sums, which the mixin refuses. |
| `purchase_request` | 16.0 to 19.0 | A vendor's minimum quantity is converted from the vendor price's unit to the unit of the purchase line before the two are compared. | In 16.0 both were always in the product's purchase unit. In 19.0 a vendor price has a unit of its own (`product_uom_id` on `product.supplierinfo`) and there is no purchase unit on the product. |
| `auditlog` | 15.0 to 19.0 | A subscribed rule is read-only through the form view (`readonly="state == 'subscribed'"` on each field). In 15.0 the same rule sat on the fields in Python. Code that writes to a subscribed rule directly is no longer stopped by the field definition; in 15.0 it was not stopped either, `states` only ever acted in the form. | `states=` on a field no longer exists (checked in 18.0 and 19.0). |
| `auditlog` | 15.0 to 19.0 | Not changed, and worth knowing: the module reads the values it logs as superuser into the cache that the rest of the request shares, as it did on 15.0. | The maintainers' 19.0 version isolates those reads with a helper that replaces the transaction's cache dictionaries. We are not confident that approach is safe on Odoo 19 (see "Corrections to this page", 3:30 am) and kept the original's way; whoever needs the isolation should have it tested under their own load. |
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
| `sale_blanket_order` | 19.0 to 20.0 | The printed blanket order shows the subtotal of each section. On 19.0 it printed 0 there. | The 19.0 template added up the lines under two groups, `account.group_show_line_subtotals_tax_excluded` and `..._tax_included`, which Odoo no longer has, so nothing was added. The port adds the line's amount without or with tax according to the company's price setting, the rule Odoo 20's own sales order report uses (`price_field` in `addons/sale/report/ir_actions_report_templates.xml`). A new test prints the report and checks the subtotal. |
| `account_payment_partner` | 18.0 to 20.0 | The module no longer adds the payment mode column to the invoice analysis itself. | Since 19.0 the module it depends on, `account_payment_mode`, carries the same field and adds the column; adding it twice makes the column ambiguous. |

## Things in Odoo 18, 19 and 20 that affect any port

### Since 18.0: inherited test methods silently stop running

`odoo/tests/loader.py` (`get_module_test_cases`) runs only the test methods written in a class's own body. A test method inherited from a parent class runs only if the class, or a parent, sets `allow_inherited_tests_method = True`. Odoo 16 and 17 ran inherited tests.

A module ported from 16 or 17 can therefore pass on 18, 19 or 20 with a large share of its tests no longer running, and nothing reports it. In `partner_firstname`, 26 of 61 test runs disappeared this way until we switched them back on.

### Since 18.0: `copy()` is called with several records

Up to 17.0 `copy()` duplicated one record, and modules overrode it with `self.ensure_one()` at the top. Since 18.0 `BaseModel.copy` works on a whole recordset: it asks `copy_data()` for one dictionary per record and creates them together (`odoo/models.py` in 18.0, `odoo/orm/models.py` in 19.0). The list view's Duplicate action sends every selected id in one call (`addons/web/static/src/model/relational_model/dynamic_list.js`, `_duplicateRecords`).

An override kept from 17.0 still works from the form, where one record is duplicated, so the module's tests pass. Select two rows in the list and choose Duplicate, and it raises "Expected singleton". The per-record defaults belong in `copy_data()`, as Odoo's own `res.partner` has them. We found this in a port of `partner_firstname` to 18.0 and then in ten more of our older-version ports; the maintainers' own versions of two of those modules still have it.

### A list column hidden with `invisible="1"` is an empty column now

In a list view, a column leaves the table only when its `column_invisible` is true (`addons/web/static/src/views/list/list_renderer.js`, `getActiveColumns`; the same in 18.0, 19.0 and 20.0). `invisible` is looked at per row and only empties the cell (`list_renderer.xml`, `isInvisible`). Old modules hid technical columns with `invisible="1"`, which worked while a constant there hid the whole column. Carried over as it is, the list shows the column's title above a column of blanks. Nothing fails.

A second reviewer pointed at it in a module from 17.0. We then found it in older-version ports of ours (up to 50 columns in one of them) and in 24 of our Odoo 20 ports, 17 of them listed here, where it comes unchanged from the 19.0 originals. A constant `invisible` on a list column is now reported for every port, and corrected to `column_invisible`.

### A view chosen by a value in the context is never chosen

Old modules pick a different form or list in `fields_view_get` (later `get_view`) by looking at a key of the action's context, for example a default type. When the web client loads a view it sends only the language and the keys that end in `_view_ref` (`addons/web/static/src/views/view_service.js`, `filteredContext`; the same in 18.0, 19.0 and 20.0). Every other key stays in the browser. The override still runs and never sees its key, so the user always gets the default view. A test that calls `get_view` with the context itself passes, which is how such code survives a port. Where the old version already behaved like this we leave it and say so; a working version needs a view reference in the action or separate actions.

### `states=` on a field is gone, and the rule goes with it

Until 16.0 a field could be made read-only or required per state in Python: `states={"done": [("readonly", True)]}`. The parameter no longer exists (checked in 18.0 and later; views stopped accepting `states` in 17.0, `odoo/addons/base/models/ir_ui_view.py`). A port that only deletes it installs and passes its tests, and the field is now editable in every state. The rule has to be written into each view that shows the field (`readonly="state == 'done'"`). Tests that write through the ORM never see the difference; a user does.

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

A 19.0 module hooks its card onto one of the category blocks of the home page (`portal_client_category` and its siblings). Those blocks are gone in 20.0, so that module does not install: this one is loud. The quiet version comes from fixing the install error the short way, by hooking onto something that still exists. `portal.portal_docs_entry` now expects an `entry` record, so what a customer gets depends on where the hook landed: no card, or an error on `/my`. Either way a test that opens `/my` as a portal user and looks for the card's link catches it. (An earlier version of this paragraph said the old way installs without an error. A second check of this page against the source on 20 November 2026 showed that is only true after such a short fix.)

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
- Odoo's script skips a `t-call` that already has an attribute not starting with `t-`. On 19.0 that could be an `id` or a `groups` rule (`groups` is itself a QWeb directive, an alias of `t-groups`), with the values still set in the body. A check built on the script has to look at those calls separately; ours did not until 20 November 2026.
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

### Since 19.0: the precision for quantities has a new name

Every quantity field takes its number of decimals from a named setting. Up to 18.0 the name is "Product Unit of Measure" (`addons/product/data/product_data.xml`). In 19.0 and 20.0 it is "Product Unit" (`addons/uom/data/uom_data.xml`). A precision is looked up by name, and a name that does not exist is not an error: `precision_get` returns 2 (`odoo/addons/base/models/decimal_precision.py`).

So `fields.Float(digits="Product Unit of Measure")` and `precision_get("Product Unit of Measure")` quietly mean "2 decimals" on 19.0 and 20.0. A company that works with 3 or 4 decimals on quantities gets them rounded to 2 in that one module, on a blanket order line or a manual stock assignment, while the rest of Odoo keeps its setting. No test notices, because a test database keeps the default of 2.

A second reviewer found it in a port from 17.0 to 19.0. We then looked at our Odoo 20 ports: 15 of them asked for the old name, in 44 places, all carried over unchanged from their 19.0 originals, where it was already wrong (11 of the 15 are listed on this page). We renamed it in all of them. The same words used as a field label, or printed in a report, are not a precision name and stay as they are.

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

`res.partner.is_company` is a stored computed field in 20.0: a partner is a company when it is its own commercial entity and has a tax ID (`_compute_is_company` in `odoo/addons/base/models/res_partner.py`). In 19.0 it is a plain checkbox. A partner created with `is_company=True` and no tax ID comes out as a person. A plain write of `True` on an existing partner holds only until its tax ID or its parent changes and the field is computed again.

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
- No model has `get_formview_action()` in 20.0. It was renamed to `get_record_default_action()` (`odoo/addons/base/models/ir_ui_view.py`); `_get_records_action()`, which opens one record or a list of several, exists in 19.0 and 20.0 alike. `check_access_rights()` and `check_access_rule()` are gone too; `has_access(operation)` and `check_access(operation)` remain (`odoo/orm/models.py`).
- Odoo 20 no longer installs `pytz` and `xlwt` (they are in 19.0's `requirements.txt` and not in 20.0's; Odoo itself moved to `zoneinfo`). A module that imports `pytz` works on a machine that happens to have it and fails to load on a clean Odoo 20, unless its manifest declares it under `external_dependencies`.
- In 20.0, tests built on `BaseCommon` run as a test user who has only the internal user group, unless the class sets `_test_user_groups` (`odoo/addons/base/tests/common.py`). A test that passed as the superuser can fail on access for that reason alone.
- The published `odoo-test-helper` package does not load fake models on 20.0, because the registry internals it uses changed (`MetaModel.module_to_models` is now `_module_to_models__`, and `Registry.load` no longer takes a cursor). The four ports that need it carry an adapted copy of its loader in their `tests/` folder, with the original copyright and licence lines.
