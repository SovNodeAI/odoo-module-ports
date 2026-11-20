# Odoo modules ported to Odoo 18, 19 and 20, with test evidence

SovNode ports Odoo modules to new Odoo versions. This repository is our public track record: community modules we have ported, each one installed on a clean database of the target version and passing its own test suite.

Figures as of 20 November 2026, 6:30 am (US Central). 55 of the 428 modules listed on the morning of 18 November are off this page until they are corrected and pass. Why, and every other correction we have had to make to this page (skipped browser tests, a template change in Odoo 20, icons Odoo 20 no longer draws, the ports from older versions), is in [NOTES.md](NOTES.md) under "Corrections to this page".

**What this list is, and what it is not (20 November 2026).** Every module in [`20.0/`](20.0) installs on Odoo 20, passes every test it defines and passes our static checks. That is all the list claims. On 20 November a second reviewer read the complete code change of three of the larger ports that were on it: `mis_builder`, `helpdesk_mgmt` and `account_financial_report`. It found faults in all three that none of their tests touches. We confirmed the ones we have checked so far in the Odoo source: in `mis_builder`, a date condition the port had changed and a call to `read_group` with arguments Odoo 20 no longer takes; in `account_financial_report`, a guard the port had relaxed. Those three are off the list until corrected. The other modules have not had that review yet, so expect faults of the same kind among the larger ones. We are working through the list, and [MODULES.md](MODULES.md) says for each module whether its second review is done.

## What is here

| Folder | What it holds | Table |
|---|---|---|
| [`20.0/`](20.0) | 396 community modules ported to Odoo 20.0. In every one, each test the module defines runs and passes, browser tests included: 4,715 test runs in all. | [MODULES.md](MODULES.md) |
| [`from-older-versions/`](from-older-versions) | Ports from Odoo 15.0, 16.0 and 17.0. All were withdrawn on 20 November 2026 for a second review; a port returns when it has passed one. See below. | [OLDER_VERSIONS.md](OLDER_VERSIONS.md) |
| [NOTES.md](NOTES.md) | Where a port had to change behaviour because Odoo removed something, and what we found in Odoo 18, 19 and 20 that affects any port. | |
| [CHECKLIST.md](CHECKLIST.md) | One page: what passes every test and still breaks when a module arrives on 18, 19 or 20, with a text search for each case. Use it on your own modules. | |

**Ports from older versions were withdrawn and are returning one by one.** Most databases that need upgrading today are on 15, 16 or 17, and the private modules in them have to make that whole jump at once. So until 20 November 2026 this page carried 28 ports made from the 15.0, 16.0 and 17.0 versions of well-known modules to 19.0 and 20.0, each passing every one of its own tests. A second reviewer then read three of them against the maintainers' own 19.0 versions. In the first, `helpdesk_mgmt` from 17.0 to 19.0, the kanban views still used the old card template, which Odoo 19 refuses, so those screens would not open; no test of the module opens them. The other two reviews listed faults as well. A port from an old version crosses several releases at once, and passing tests proved less there than this page said. Each of these ports comes back only after it has been read against the maintainers' version, every finding has been fixed or ruled out, and its tests pass again. [OLDER_VERSIONS.md](OLDER_VERSIONS.md) lists the ones that have; [NOTES.md](NOTES.md) says what the review found in each, under "Corrections to this page".

## How a port is checked

1. **Installed and tested on a real database.** The module is installed on a clean database of the target version with its dependencies, and its own tests are run.
2. **A pass only counts if every test actually ran.** We compare the tests the module defines with the tests that started. A test that skips itself counts as not run. Browser tests (a module's tours and its JavaScript unit tests) run in Chrome; a module that carries web code is listed only after a run in which they ran. Since Odoo 18 the test runner no longer runs test methods that a class inherits from a parent class, and nothing warns about it. A module ported from 16 or 17 can "pass" with a third of its tests silently gone. We check for that on every port and switch those tests back on.
3. **Changed tests are reviewed.** When a test has to change for the new version, it must still check what it checked before. Every changed test is read by a reviewer that did not make the port. A questioned change is either put back or justified from the Odoo source code.
4. **Nothing left behind, nothing lost.** Each port is scanned for leftover debugging lines and for files that are no longer loaded. Its record rules are compared with the original's, because Odoo's own upgrade script for 20.0 can drop a rule without replacing it (see [NOTES.md](NOTES.md)). Copyright comments are checked file by file. Every method that extends a parent method is checked against the source of the target version, model by model, because a method Odoo has renamed or removed is simply never called again and no test notices. The same goes for calls to methods Odoo removed, for JavaScript imports that point at files Odoo moved, and for Python packages Odoo no longer installs.
5. **License, authors and dependencies are untouched.**
6. **Nothing listed stands on a known defect.** A module is listed only while every community module it depends on, at any depth, is free of defects we know of. Dependencies that are not in this repository are named at the end of [MODULES.md](MODULES.md), each with the reason.

## What a pass does not prove

- Screens are not checked visually. Click through on a staging system. The one visual fault we check for statically is an icon still named the Font Awesome way, which Odoo 20 does not draw (see [NOTES.md](NOTES.md)).
- A report or a portal page is proven only where a test renders it. A template can install without an error and print without a value it used to receive. We check statically for the one cause of that we know in Odoo 20 (see "a value set inside a `t-call`" in [NOTES.md](NOTES.md)); print your documents on a staging system.
- A module's web code is proven only as far as a browser test of that module exercises it. Many modules have none. For those, the web code is only checked statically: every JavaScript import has to resolve to a file of the target version that exports the name, and no component may use something Owl 3 rejects. That is not proof that the screen works.
- These are code ports. Scripts that convert the data of an existing database are not included.
- Modules without tests of their own are not in this repository. We port those too, but "it installs cleanly" is weaker proof and we do not present it as more.
- These ports have not been reviewed by the OCA maintainers and are not the official OCA branches. Where the OCA publishes its own version of a module for your Odoo version, use that one.

## Your own modules

Odoo will not upgrade a database until every custom module in it has a version for the target release. That is the part we do.

- Fixed price per module, quoted before we start.
- 48-hour turnaround on standard modules.
- You receive the ported module, the full test log, a count of how many of the module's tests ran, and a change summary listing every file touched and why.
- If Odoo removed something your module was built on, the summary says so plainly, as [NOTES.md](NOTES.md) does here.
- 14-day fix window: if it fails on your staging system, we fix it at no charge.

To ask for a quote, reply to the email that brought you here, or open an issue in this repository.

## License and credit

Every module keeps its original license (AGPL-3 or LGPL-3, see each `__manifest__.py`) and its copyright headers. The modules were written by the Odoo Community Association (OCA) and the contributors named in each module. The tables give the OCA repository and the commit each port started from. What we changed is the port to the target Odoo version; nothing else.

SovNode is not affiliated with the OCA or with Odoo S.A.
