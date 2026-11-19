# Modules ported to Odoo 20.0

414 modules. In every one of them each test the module defines ran and passed on a clean Odoo 20.0 database: 5214 test runs in all.

- **Source**: the OCA repository, branch and commit the port started from.
- **Test methods**: test methods the module defines. **Test runs**: how many times they ran (a method can run more than once when test classes inherit from each other). All passed.
- **Test changes**: `none` = the module's tests are byte-for-byte the original's apart from whitespace; `reviewed` = the tests had to change for Odoo 20 and an independent review of every change found nothing weakened; `reviewed, accepted` = the review questioned a change and it was checked against the Odoo 20 source and kept.

| Module | Source repository | From | Commit | License | Test methods | Test runs | Test changes |
|---|---|---|---|---|---|---|---|
| [account_analytic_parent](20.0/account_analytic_parent) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 7 | 7 | none |
| [account_analytic_sequence](20.0/account_analytic_sequence) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 1 | 1 | reviewed |
| [account_analytic_tag](20.0/account_analytic_tag) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 6 | 6 | reviewed |
| [account_asset_low_value](20.0/account_asset_low_value) | OCA/account-financial-tools | 18.0 | `a7d84ff` | AGPL-3 | 1 | 1 | none |
| [account_asset_management](20.0/account_asset_management) | OCA/account-financial-tools | 19.0 | `4a1c887` | AGPL-3 | 27 | 27 | none |
| [account_asset_transfer](20.0/account_asset_transfer) | OCA/account-financial-tools | 18.0 | `a7d84ff` | AGPL-3 | 1 | 1 | none |
| [account_avatax_oca](20.0/account_avatax_oca) | OCA/account-fiscal-rule | 18.0 | `3fd03ff` | AGPL-3 | 12 | 12 | reviewed |
| [account_banking_mandate](20.0/account_banking_mandate) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 21 | 21 | reviewed |
| [account_banking_pain_base](20.0/account_banking_pain_base) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 17 | 17 | reviewed |
| [account_banking_sepa_credit_transfer](20.0/account_banking_sepa_credit_transfer) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 8 | 8 | reviewed |
| [account_commission_oca](20.0/account_commission_oca) | OCA/commission | 19.0 | `3649f32` | AGPL-3 | 17 | 17 | none |
| [account_credit_control](20.0/account_credit_control) | OCA/credit-control | 19.0 | `ade8df1` | AGPL-3 | 28 | 28 | reviewed |
| [account_due_list](20.0/account_due_list) | OCA/account-payment | 19.0 | `376d018` | AGPL-3 | 1 | 1 | none |
| [account_einvoice_generate](20.0/account_einvoice_generate) | OCA/edi | 18.0 | `f62d700` | AGPL-3 | 1 | 1 | none |
| [account_financial_report](20.0/account_financial_report) | OCA/account-financial-reporting | 19.0 | `94ad458` | AGPL-3 | 32 | 34 | reviewed |
| [account_fiscal_year](20.0/account_fiscal_year) | OCA/account-financial-tools | 19.0 | `4a1c887` | AGPL-3 | 4 | 4 | none |
| [account_global_discount](20.0/account_global_discount) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 10 | 10 | none |
| [account_in_payment](20.0/account_in_payment) | OCA/account-reconcile | 19.0 | `fa7be05` | AGPL-3 | 2 | 2 | none |
| [account_invoice_ar_ap_by_journal](20.0/account_invoice_ar_ap_by_journal) | OCA/account-invoicing | 18.0 | `4a901e9` | AGPL-3 | 1 | 1 | reviewed |
| [account_invoice_export](20.0/account_invoice_export) | OCA/edi | 19.0 | `9dc91ef` | AGPL-3 | 6 | 6 | none |
| [account_invoice_fixed_discount](20.0/account_invoice_fixed_discount) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 5 | 5 | reviewed |
| [account_invoice_import](20.0/account_invoice_import) | OCA/edi | 19.0 | `9dc91ef` | AGPL-3 | 9 | 9 | reviewed |
| [account_invoice_inter_company](20.0/account_invoice_inter_company) | OCA/multi-company | 19.0 | `2992d5a` | AGPL-3 | 14 | 14 | reviewed |
| [account_invoice_merge](20.0/account_invoice_merge) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 10 | 10 | none |
| [account_invoice_overdue_warn](20.0/account_invoice_overdue_warn) | OCA/credit-control | 19.0 | `ade8df1` | AGPL-3 | 1 | 1 | none |
| [account_invoice_pricelist](20.0/account_invoice_pricelist) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 14 | 14 | reviewed |
| [account_invoice_refund_link](20.0/account_invoice_refund_link) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 4 | 6 | reviewed |
| [account_invoice_report_grouped_by_picking](20.0/account_invoice_report_grouped_by_picking) | OCA/account-invoice-reporting | 19.0 | `79bd733` | AGPL-3 | 7 | 7 | reviewed |
| [account_invoice_report_payment_info](20.0/account_invoice_report_payment_info) | OCA/account-invoice-reporting | 19.0 | `79bd733` | AGPL-3 | 1 | 1 | reviewed |
| [account_invoice_start_end_dates](20.0/account_invoice_start_end_dates) | OCA/account-closing | 19.0 | `4f06e76` | LGPL-3 | 5 | 5 | reviewed, accepted |
| [account_invoice_tax_required](20.0/account_invoice_tax_required) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 4 | 4 | none |
| [account_invoice_transmit_method](20.0/account_invoice_transmit_method) | OCA/account-invoicing | 19.0 | `5b5f7d5` | AGPL-3 | 3 | 3 | none |
| [account_loan](20.0/account_loan) | OCA/account-financial-tools | 18.0 | `a7d84ff` | AGPL-3 | 17 | 17 | reviewed |
| [account_lock_date_update](20.0/account_lock_date_update) | OCA/account-financial-tools | 19.0 | `4a1c887` | AGPL-3 | 1 | 1 | none |
| [account_manual_currency](20.0/account_manual_currency) | OCA/account-invoicing | 18.0 | `4a901e9` | AGPL-3 | 2 | 2 | reviewed |
| [account_move_name_sequence](20.0/account_move_name_sequence) | OCA/account-financial-tools | 19.0 | `4a1c887` | AGPL-3 | 25 | 25 | reviewed |
| [account_multicompany_easy_creation](20.0/account_multicompany_easy_creation) | OCA/multi-company | 18.0 | `cf22d0e` | AGPL-3 | 2 | 2 | reviewed |
| [account_netting](20.0/account_netting) | OCA/account-financial-tools | 19.0 | `4a1c887` | AGPL-3 | 1 | 1 | none |
| [account_operating_unit](20.0/account_operating_unit) | OCA/operating-unit | 19.0 | `df56d49` | LGPL-3 | 15 | 15 | reviewed |
| [account_partner_company_group](20.0/account_partner_company_group) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | reviewed, accepted |
| [account_payment_base_oca_sale](20.0/account_payment_base_oca_sale) | OCA/bank-payment-alternative | 19.0 | `5893a02` | AGPL-3 | 4 | 4 | reviewed |
| [account_payment_mode](20.0/account_payment_mode) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 23 | 23 | reviewed, accepted |
| [account_payment_order](20.0/account_payment_order) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 24 | 26 | reviewed |
| [account_payment_order_notification](20.0/account_payment_order_notification) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 1 | 1 | reviewed |
| [account_payment_partner](20.0/account_payment_partner) | OCA/bank-payment | 18.0 | `24ba240` | AGPL-3 | 23 | 23 | reviewed, accepted |
| [account_payment_purchase](20.0/account_payment_purchase) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 5 | 5 | reviewed |
| [account_payment_purchase_stock](20.0/account_payment_purchase_stock) | OCA/bank-payment | 19.0 | `b5d4fbf` | AGPL-3 | 4 | 4 | none |
| [account_payment_term_extension](20.0/account_payment_term_extension) | OCA/account-payment | 19.0 | `376d018` | AGPL-3 | 22 | 22 | reviewed |
| [account_reconcile_model_oca](20.0/account_reconcile_model_oca) | OCA/account-reconcile | 18.0 | `db252b0` | LGPL-3 | 36 | 36 | reviewed, accepted |
| [account_reconcile_oca](20.0/account_reconcile_oca) | OCA/account-reconcile | 19.0 | `fa7be05` | AGPL-3 | 48 | 48 | reviewed, accepted |
| [account_statement_base](20.0/account_statement_base) | OCA/account-reconcile | 19.0 | `fa7be05` | LGPL-3 | 1 | 1 | none |
| [account_statement_import_camt](20.0/account_statement_import_camt) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 6 | 6 | reviewed |
| [account_statement_import_file](20.0/account_statement_import_file) | OCA/bank-statement-import | 19.0 | `058a9a8` | LGPL-3 | 3 | 3 | reviewed |
| [account_statement_import_generate_unique_id](20.0/account_statement_import_generate_unique_id) | OCA/bank-statement-import | 18.0 | `64d0022` | LGPL-3 | 4 | 4 | none |
| [account_statement_import_online](20.0/account_statement_import_online) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 29 | 29 | none |
| [account_statement_import_online_gocardless](20.0/account_statement_import_online_gocardless) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 2 | 2 | reviewed |
| [account_statement_import_online_paypal](20.0/account_statement_import_online_paypal) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 17 | 17 | reviewed |
| [account_statement_import_online_stripe](20.0/account_statement_import_online_stripe) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 1 | 1 | reviewed |
| [account_statement_import_sheet_file](20.0/account_statement_import_sheet_file) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 15 | 15 | reviewed |
| [account_statement_import_sheet_file_xlsx](20.0/account_statement_import_sheet_file_xlsx) | OCA/bank-statement-import | 19.0 | `058a9a8` | AGPL-3 | 5 | 5 | none |
| [account_tax_balance](20.0/account_tax_balance) | OCA/account-financial-reporting | 19.0 | `94ad458` | AGPL-3 | 4 | 4 | none |
| [account_tax_unece](20.0/account_tax_unece) | OCA/community-data-files | 19.0 | `be3b367` | LGPL-3 | 1 | 1 | none |
| [agreement](20.0/agreement) | OCA/agreement | 19.0 | `1a330f2` | AGPL-3 | 4 | 4 | none |
| [agreement_rebate](20.0/agreement_rebate) | OCA/agreement | 19.0 | `1a330f2` | AGPL-3 | 9 | 9 | reviewed |
| [attachment_preview](20.0/attachment_preview) | OCA/knowledge | 18.0 | `b19da27` | AGPL-3 | 1 | 1 | reviewed |
| [attachment_unindex_content](20.0/attachment_unindex_content) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 11 | 11 | reviewed |
| [attribute_set](20.0/attribute_set) | OCA/odoo-pim | 19.0 | `96c1abb` | AGPL-3 | 36 | 36 | none |
| [auditlog](20.0/auditlog) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 31 | 50 | reviewed |
| [auth_api_key](20.0/auth_api_key) | OCA/server-auth | 19.0 | `ae09869` | LGPL-3 | 13 | 13 | reviewed |
| [auth_api_key_group](20.0/auth_api_key_group) | OCA/server-auth | 19.0 | `ae09869` | LGPL-3 | 1 | 1 | none |
| [auth_oauth_multi_token](20.0/auth_oauth_multi_token) | OCA/server-auth | 19.0 | `ae09869` | AGPL-3 | 7 | 7 | none |
| [auth_oidc](20.0/auth_oidc) | OCA/server-auth | 19.0 | `ae09869` | AGPL-3 | 10 | 10 | none |
| [auth_oidc_environment](20.0/auth_oidc_environment) | OCA/server-auth | 18.0 | `23df47b` | AGPL-3 | 1 | 1 | none |
| [auth_session_timeout](20.0/auth_session_timeout) | OCA/server-auth | 19.0 | `ae09869` | AGPL-3 | 12 | 12 | reviewed |
| [auth_signup_verify_email](20.0/auth_signup_verify_email) | OCA/server-auth | 18.0 | `23df47b` | AGPL-3 | 3 | 3 | reviewed |
| [auth_user_case_insensitive](20.0/auth_user_case_insensitive) | OCA/server-auth | 19.0 | `ae09869` | AGPL-3 | 3 | 3 | none |
| [autovacuum_message_attachment](20.0/autovacuum_message_attachment) | OCA/server-tools | 18.0 | `55308ba` | LGPL-3 | 4 | 4 | reviewed |
| [base_business_document_import](20.0/base_business_document_import) | OCA/edi | 19.0 | `9dc91ef` | AGPL-3 | 16 | 16 | none |
| [base_cancel_confirm](20.0/base_cancel_confirm) | OCA/server-ux | 19.0 | `ecb65d1` | AGPL-3 | 3 | 3 | reviewed |
| [base_edi](20.0/base_edi) | OCA/edi | 19.0 | `9dc91ef` | LGPL-3 | 1 | 1 | none |
| [base_exception](20.0/base_exception) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 13 | 13 | none |
| [base_external_dbsource](20.0/base_external_dbsource) | OCA/server-backend | 19.0 | `d6b0897` | LGPL-3 | 26 | 26 | none |
| [base_global_discount](20.0/base_global_discount) | OCA/server-backend | 19.0 | `d6b0897` | AGPL-3 | 3 | 3 | none |
| [base_kanban_stage](20.0/base_kanban_stage) | OCA/server-tools | 19.0 | `71de4de` | LGPL-3 | 7 | 7 | reviewed |
| [base_location](20.0/base_location) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 18 | 18 | none |
| [base_location_geonames_import](20.0/base_location_geonames_import) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 7 | 7 | reviewed |
| [base_name_search_improved](20.0/base_name_search_improved) | OCA/server-tools | 18.0 | `55308ba` | AGPL-3 | 6 | 6 | reviewed |
| [base_partner_company_group](20.0/base_partner_company_group) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | reviewed |
| [base_partner_sequence](20.0/base_partner_sequence) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 5 | 5 | reviewed |
| [base_revision](20.0/base_revision) | OCA/server-ux | 19.0 | `ecb65d1` | AGPL-3 | 3 | 3 | none |
| [base_search_fuzzy](20.0/base_search_fuzzy) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 8 | 8 | reviewed |
| [base_sequence_option](20.0/base_sequence_option) | OCA/server-tools | 18.0 | `55308ba` | LGPL-3 | 1 | 1 | reviewed |
| [base_sequence_template](20.0/base_sequence_template) | OCA/server-tools | 18.0 | `55308ba` | AGPL-3 | 5 | 5 | none |
| [base_substate](20.0/base_substate) | OCA/server-ux | 19.0 | `ecb65d1` | AGPL-3 | 1 | 1 | reviewed |
| [base_technical_features](20.0/base_technical_features) | OCA/server-ux | 19.0 | `ecb65d1` | AGPL-3 | 9 | 9 | reviewed, accepted |
| [base_technical_user](20.0/base_technical_user) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 6 | 6 | none |
| [base_territory](20.0/base_territory) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 19 | 19 | none |
| [base_user_role_company](20.0/base_user_role_company) | OCA/server-backend | 19.0 | `d6b0897` | AGPL-3 | 7 | 7 | none |
| [base_user_role_history](20.0/base_user_role_history) | OCA/server-backend | 19.0 | `d6b0897` | AGPL-3 | 8 | 8 | reviewed |
| [bi_sql_editor](20.0/bi_sql_editor) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 5 | 5 | none |
| [brand](20.0/brand) | OCA/brand | 19.0 | `a89a1c2` | LGPL-3 | 2 | 2 | none |
| [business_requirement](20.0/business_requirement) | OCA/business-requirement | 18.0 | `7052fb3` | AGPL-3 | 12 | 12 | reviewed |
| [business_requirement_deliverable](20.0/business_requirement_deliverable) | OCA/business-requirement | 18.0 | `7052fb3` | AGPL-3 | 23 | 23 | reviewed, accepted |
| [calendar_public_holiday](20.0/calendar_public_holiday) | OCA/calendar | 19.0 | `1d6bd36` | AGPL-3 | 11 | 11 | reviewed |
| [commission_oca](20.0/commission_oca) | OCA/commission | 19.0 | `3649f32` | AGPL-3 | 3 | 3 | none |
| [component](20.0/component) | OCA/connector | 19.0 | `cce7654` | LGPL-3 | 45 | 45 | reviewed |
| [connector](20.0/connector) | OCA/connector | 19.0 | `cce7654` | LGPL-3 | 31 | 31 | none |
| [connector_mercadolibre](20.0/connector_mercadolibre) | OCA/connector-mercadolibre | 19.0 | `45e0f2e` | AGPL-3 | 49 | 49 | reviewed |
| [contract](20.0/contract) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 77 | 77 | reviewed, accepted |
| [contract_line_successor](20.0/contract_line_successor) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 45 | 45 | none |
| [contract_payment_mode](20.0/contract_payment_mode) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 2 | 2 | none |
| [contract_sale](20.0/contract_sale) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 4 | 4 | none |
| [contract_sale_generation](20.0/contract_sale_generation) | OCA/contract | 18.0 | `aa96753` | AGPL-3 | 13 | 13 | reviewed |
| [contract_termination](20.0/contract_termination) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 3 | 3 | none |
| [contract_variable_quantity](20.0/contract_variable_quantity) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 5 | 5 | reviewed |
| [crm_claim](20.0/crm_claim) | OCA/crm | 19.0 | `16ad7c9` | AGPL-3 | 3 | 3 | reviewed |
| [crm_lead_code](20.0/crm_lead_code) | OCA/crm | 19.0 | `16ad7c9` | AGPL-3 | 3 | 3 | none |
| [crm_phonecall](20.0/crm_phonecall) | OCA/crm | 19.0 | `16ad7c9` | AGPL-3 | 9 | 9 | none |
| [currency_rate_update](20.0/currency_rate_update) | OCA/currency | 19.0 | `ec7e095` | AGPL-3 | 11 | 11 | reviewed |
| [currency_rate_update_xe](20.0/currency_rate_update_xe) | OCA/currency | 18.0 | `e7d64f8` | AGPL-3 | 3 | 3 | none |
| [data_encryption](20.0/data_encryption) | OCA/server-env | 18.0 | `dc737ed` | AGPL-3 | 10 | 10 | reviewed |
| [database_cleanup](20.0/database_cleanup) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 11 | 11 | reviewed |
| [ddmrp](20.0/ddmrp) | OCA/ddmrp | 19.0 | `84ec100` | LGPL-3 | 63 | 63 | reviewed, accepted |
| [ddmrp_cron_actions_as_job](20.0/ddmrp_cron_actions_as_job) | OCA/ddmrp | 19.0 | `84ec100` | LGPL-3 | 3 | 3 | none |
| [delivery_carrier_partner](20.0/delivery_carrier_partner) | OCA/delivery-carrier | 19.0 | `b6258c7` | AGPL-3 | 1 | 1 | none |
| [delivery_dropoff_site](20.0/delivery_dropoff_site) | OCA/delivery-carrier | 18.0 | `95c525a` | AGPL-3 | 10 | 10 | reviewed |
| [delivery_fee](20.0/delivery_fee) | OCA/delivery-carrier | 18.0 | `95c525a` | LGPL-3 | 12 | 12 | reviewed |
| [delivery_sendcloud_oca](20.0/delivery_sendcloud_oca) | OCA/delivery-carrier | 18.0 | `95c525a` | LGPL-3 | 26 | 26 | reviewed, accepted |
| [dms_auto_classification](20.0/dms_auto_classification) | OCA/dms | 18.0 | `a083c5b` | AGPL-3 | 7 | 7 | reviewed |
| [document_page_access_group](20.0/document_page_access_group) | OCA/knowledge | 19.0 | `3ba8a78` | AGPL-3 | 3 | 3 | none |
| [document_page_reference](20.0/document_page_reference) | OCA/knowledge | 18.0 | `b19da27` | AGPL-3 | 8 | 8 | reviewed |
| [document_url](20.0/document_url) | OCA/knowledge | 19.0 | `3ba8a78` | AGPL-3 | 2 | 2 | reviewed, accepted |
| [edi_core_oca](20.0/edi_core_oca) | OCA/edi-framework | 19.0 | `73845cf` | LGPL-3 | 138 | 139 | reviewed |
| [edi_queue_oca](20.0/edi_queue_oca) | OCA/edi-framework | 19.0 | `73845cf` | LGPL-3 | 16 | 16 | reviewed |
| [edi_webservice_core_oca](20.0/edi_webservice_core_oca) | OCA/edi-framework | 18.0 | `8c263d9` | AGPL-3 | 8 | 8 | reviewed |
| [fieldservice](20.0/fieldservice) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 39 | 40 | reviewed |
| [fieldservice_account](20.0/fieldservice_account) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 1 | 1 | none |
| [fieldservice_activity](20.0/fieldservice_activity) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 4 | 4 | none |
| [fieldservice_crm](20.0/fieldservice_crm) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 2 | 2 | none |
| [fieldservice_project](20.0/fieldservice_project) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 5 | 6 | none |
| [fieldservice_recurring](20.0/fieldservice_recurring) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 5 | 5 | none |
| [fieldservice_sale](20.0/fieldservice_sale) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 27 | 27 | reviewed |
| [fieldservice_stage_validation](20.0/fieldservice_stage_validation) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 2 | 2 | none |
| [fieldservice_stock](20.0/fieldservice_stock) | OCA/field-service | 19.0 | `650561d` | AGPL-3 | 5 | 5 | none |
| [helpdesk_mgmt](20.0/helpdesk_mgmt) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 35 | 35 | reviewed, accepted |
| [helpdesk_mgmt_activity](20.0/helpdesk_mgmt_activity) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 6 | 6 | reviewed |
| [helpdesk_mgmt_crm](20.0/helpdesk_mgmt_crm) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 3 | 3 | reviewed |
| [helpdesk_mgmt_merge](20.0/helpdesk_mgmt_merge) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 2 | 2 | reviewed |
| [helpdesk_mgmt_portal_follower](20.0/helpdesk_mgmt_portal_follower) | OCA/helpdesk | 18.0 | `9fbf485` | AGPL-3 | 2 | 2 | reviewed |
| [helpdesk_mgmt_sla](20.0/helpdesk_mgmt_sla) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 19 | 19 | reviewed |
| [helpdesk_ticket_partner_response](20.0/helpdesk_ticket_partner_response) | OCA/helpdesk | 19.0 | `9bfcdef` | AGPL-3 | 20 | 20 | reviewed |
| [hotel](20.0/hotel) | OCA/vertical-hotel | 19.0 | `5094008` | LGPL-3 | 8 | 8 | none |
| [hotel_housekeeping](20.0/hotel_housekeeping) | OCA/vertical-hotel | 19.0 | `5094008` | AGPL-3 | 8 | 8 | none |
| [hotel_restaurant](20.0/hotel_restaurant) | OCA/vertical-hotel | 19.0 | `5094008` | AGPL-3 | 11 | 11 | none |
| [hr_course](20.0/hr_course) | OCA/hr | 19.0 | `1c718db` | AGPL-3 | 2 | 2 | reviewed |
| [hr_expense_advance_clearing](20.0/hr_expense_advance_clearing) | OCA/hr-expense | 18.0 | `8d41ea6` | AGPL-3 | 8 | 8 | reviewed, accepted |
| [hr_expense_analytic_tag](20.0/hr_expense_analytic_tag) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 5 | 10 | reviewed |
| [hr_holidays_public](20.0/hr_holidays_public) | OCA/hr-holidays | 19.0 | `46e293f` | AGPL-3 | 17 | 17 | reviewed |
| [hr_job_category](20.0/hr_job_category) | OCA/hr | 19.0 | `1c718db` | AGPL-3 | 4 | 4 | reviewed |
| [hr_shift](20.0/hr_shift) | OCA/shift-planning | 18.0 | `6c44585` | AGPL-3 | 8 | 8 | reviewed |
| [hr_timesheet_sheet](20.0/hr_timesheet_sheet) | OCA/timesheet | 19.0 | `daaa000` | AGPL-3 | 29 | 29 | reviewed |
| [hr_timesheet_time_control](20.0/hr_timesheet_time_control) | OCA/timesheet | 19.0 | `daaa000` | AGPL-3 | 20 | 20 | reviewed |
| [hr_timesheet_time_control_begin_end](20.0/hr_timesheet_time_control_begin_end) | OCA/timesheet | 19.0 | `daaa000` | AGPL-3 | 11 | 11 | reviewed |
| [iap_alternative_provider](20.0/iap_alternative_provider) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 3 | 3 | none |
| [iot_oca](20.0/iot_oca) | OCA/iot | 18.0 | `30f6d87` | AGPL-3 | 3 | 3 | none |
| [iot_output_oca](20.0/iot_output_oca) | OCA/iot | 18.0 | `30f6d87` | AGPL-3 | 5 | 5 | none |
| [jsonifier](20.0/jsonifier) | OCA/server-tools | 18.0 | `55308ba` | LGPL-3 | 18 | 18 | reviewed |
| [l10n_br_account_due_list](20.0/l10n_br_account_due_list) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 2 | 2 | none |
| [l10n_br_account_payment_order](20.0/l10n_br_account_payment_order) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 30 | 30 | reviewed |
| [l10n_br_base](20.0/l10n_br_base) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 83 | 83 | reviewed |
| [l10n_br_cnab_structure](20.0/l10n_br_cnab_structure) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 35 | 35 | reviewed |
| [l10n_br_coa_generic](20.0/l10n_br_coa_generic) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 1 | 1 | none |
| [l10n_br_coa_simple](20.0/l10n_br_coa_simple) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 1 | 1 | none |
| [l10n_br_contract](20.0/l10n_br_contract) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 3 | 3 | reviewed |
| [l10n_br_currency_rate_update](20.0/l10n_br_currency_rate_update) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 7 | 7 | none |
| [l10n_br_fiscal_certificate](20.0/l10n_br_fiscal_certificate) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 9 | 9 | reviewed |
| [l10n_br_fiscal_dfe](20.0/l10n_br_fiscal_dfe) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 11 | 11 | reviewed, accepted |
| [l10n_br_fiscal_edi](20.0/l10n_br_fiscal_edi) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 31 | 31 | none |
| [l10n_br_purchase](20.0/l10n_br_purchase) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 15 | 15 | reviewed, accepted |
| [l10n_br_purchase_blanket_order](20.0/l10n_br_purchase_blanket_order) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 10 | 10 | reviewed |
| [l10n_br_sale](20.0/l10n_br_sale) | OCA/l10n-brazil | 19.0 | `d6b9f0d` | AGPL-3 | 21 | 28 | reviewed, accepted |
| [l10n_br_sale_blanket_order](20.0/l10n_br_sale_blanket_order) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 13 | 13 | reviewed, accepted |
| [l10n_br_stock](20.0/l10n_br_stock) | OCA/l10n-brazil | 18.0 | `c50420c` | AGPL-3 | 6 | 6 | reviewed |
| [l10n_es_aeat](20.0/l10n_es_aeat) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 39 | 39 | reviewed, accepted |
| [l10n_es_aeat_mod190](20.0/l10n_es_aeat_mod190) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 4 | 4 | reviewed |
| [l10n_es_aeat_mod303](20.0/l10n_es_aeat_mod303) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 3 | 3 | reviewed |
| [l10n_es_aeat_mod349](20.0/l10n_es_aeat_mod349) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 5 | 5 | reviewed |
| [l10n_es_aeat_mod390](20.0/l10n_es_aeat_mod390) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 4 | 4 | reviewed |
| [l10n_es_aeat_sii_oca](20.0/l10n_es_aeat_sii_oca) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 33 | 33 | none |
| [l10n_es_mis_report](20.0/l10n_es_mis_report) | OCA/l10n-spain | 19.0 | `3349525` | AGPL-3 | 4 | 4 | none |
| [l10n_es_verifactu_oca](20.0/l10n_es_verifactu_oca) | OCA/l10n-spain | 18.0 | `d2fb55a` | AGPL-3 | 29 | 29 | reviewed |
| [l10n_eu_nace](20.0/l10n_eu_nace) | OCA/community-data-files | 18.0 | `7961dea` | AGPL-3 | 7 | 7 | none |
| [l10n_eu_product_adr](20.0/l10n_eu_product_adr) | OCA/community-data-files | 19.0 | `be3b367` | AGPL-3 | 6 | 6 | reviewed |
| [l10n_fi_sale_refund_payment_reference](20.0/l10n_fi_sale_refund_payment_reference) | OCA/l10n-finland | 19.0 | `662978a` | AGPL-3 | 2 | 2 | none |
| [l10n_fr_department](20.0/l10n_fr_department) | OCA/l10n-france | 19.0 | `5647885` | AGPL-3 | 3 | 3 | none |
| [l10n_fr_department_oversea](20.0/l10n_fr_department_oversea) | OCA/l10n-france | 19.0 | `5647885` | AGPL-3 | 1 | 1 | none |
| [l10n_fr_siret](20.0/l10n_fr_siret) | OCA/l10n-france | 19.0 | `5647885` | AGPL-3 | 7 | 7 | reviewed |
| [l10n_it_abicab](20.0/l10n_it_abicab) | OCA/l10n-italy | 19.0 | `bf1f300` | AGPL-3 | 1 | 1 | reviewed |
| [l10n_it_account](20.0/l10n_it_account) | OCA/l10n-italy | 19.0 | `bf1f300` | AGPL-3 | 3 | 3 | none |
| [l10n_it_edi_doi_extension](20.0/l10n_it_edi_doi_extension) | OCA/l10n-italy | 18.0 | `207b3f2` | AGPL-3 | 18 | 18 | reviewed |
| [l10n_it_edi_pec](20.0/l10n_it_edi_pec) | OCA/l10n-italy | 18.0 | `207b3f2` | AGPL-3 | 25 | 25 | reviewed |
| [l10n_it_edi_related_document](20.0/l10n_it_edi_related_document) | OCA/l10n-italy | 19.0 | `bf1f300` | AGPL-3 | 5 | 5 | reviewed |
| [l10n_it_riba_oca](20.0/l10n_it_riba_oca) | OCA/l10n-italy | 18.0 | `207b3f2` | AGPL-3 | 34 | 34 | reviewed |
| [l10n_nl_tax_statement](20.0/l10n_nl_tax_statement) | OCA/l10n-netherlands | 19.0 | `543c5d1` | AGPL-3 | 17 | 17 | reviewed |
| [l10n_th_base_sequence](20.0/l10n_th_base_sequence) | OCA/l10n-thailand | 19.0 | `a5cc1dc` | AGPL-3 | 4 | 4 | none |
| [mail_activity_done](20.0/mail_activity_done) | OCA/mail | 18.0 | `1a7341e` | LGPL-3 | 3 | 3 | reviewed |
| [mail_autosubscribe](20.0/mail_autosubscribe) | OCA/mail | 18.0 | `1a7341e` | AGPL-3 | 8 | 8 | reviewed |
| [mail_environment](20.0/mail_environment) | OCA/server-env | 19.0 | `7172600` | AGPL-3 | 11 | 11 | none |
| [mail_gateway](20.0/mail_gateway) | OCA/mail | 19.0 | `849f3ce` | AGPL-3 | 83 | 83 | reviewed, accepted |
| [mail_gateway_whatsapp](20.0/mail_gateway_whatsapp) | OCA/social | 18.0 | `75b2203` | AGPL-3 | 21 | 21 | reviewed |
| [mail_layout_force](20.0/mail_layout_force) | OCA/mail | 18.0 | `1a7341e` | AGPL-3 | 4 | 4 | none |
| [mail_message_search](20.0/mail_message_search) | OCA/mail | 19.0 | `849f3ce` | AGPL-3 | 3 | 3 | none |
| [mail_restrict_follower_selection](20.0/mail_restrict_follower_selection) | OCA/mail | 19.0 | `849f3ce` | AGPL-3 | 5 | 5 | reviewed |
| [mail_template_substitute](20.0/mail_template_substitute) | OCA/mail | 19.0 | `849f3ce` | AGPL-3 | 6 | 6 | reviewed |
| [maintenance_equipment_certification](20.0/maintenance_equipment_certification) | OCA/maintenance | 19.0 | `7fe288e` | AGPL-3 | 3 | 3 | reviewed |
| [maintenance_equipment_contract](20.0/maintenance_equipment_contract) | OCA/maintenance | 18.0 | `5321ea3` | AGPL-3 | 2 | 2 | none |
| [maintenance_equipment_status](20.0/maintenance_equipment_status) | OCA/maintenance | 19.0 | `7fe288e` | LGPL-3 | 1 | 1 | reviewed |
| [maintenance_equipment_tags](20.0/maintenance_equipment_tags) | OCA/maintenance | 19.0 | `7fe288e` | AGPL-3 | 2 | 2 | none |
| [maintenance_plan](20.0/maintenance_plan) | OCA/maintenance | 19.0 | `7fe288e` | AGPL-3 | 14 | 14 | reviewed |
| [maintenance_plan_activity](20.0/maintenance_plan_activity) | OCA/maintenance | 19.0 | `7fe288e` | AGPL-3 | 1 | 1 | reviewed, accepted |
| [maintenance_request_sequence](20.0/maintenance_request_sequence) | OCA/maintenance | 19.0 | `7fe288e` | AGPL-3 | 2 | 2 | none |
| [marketing_crm_partner](20.0/marketing_crm_partner) | OCA/crm | 19.0 | `16ad7c9` | AGPL-3 | 1 | 1 | reviewed |
| [mass_mailing_list_dynamic](20.0/mass_mailing_list_dynamic) | OCA/mass-mailing | 19.0 | `0dfef78` | AGPL-3 | 7 | 7 | reviewed |
| [mass_mailing_partner](20.0/mass_mailing_partner) | OCA/mass-mailing | 19.0 | `0dfef78` | AGPL-3 | 17 | 19 | none |
| [membership](20.0/membership) | OCA/vertical-association | 19.0 | `a36cce3` | LGPL-3 | 15 | 15 | reviewed |
| [membership_variable_period](20.0/membership_variable_period) | OCA/vertical-association | 19.0 | `a36cce3` | AGPL-3 | 11 | 11 | none |
| [mgmtsystem](20.0/mgmtsystem) | OCA/management-system | 19.0 | `d7d4fcf` | AGPL-3 | 1 | 1 | none |
| [mgmtsystem_action](20.0/mgmtsystem_action) | OCA/management-system | 19.0 | `d7d4fcf` | AGPL-3 | 7 | 7 | none |
| [mis_builder](20.0/mis_builder) | OCA/mis-builder | 19.0 | `adbe5c3` | AGPL-3 | 97 | 98 | reviewed, accepted |
| [mis_template_financial_report](20.0/mis_template_financial_report) | OCA/account-financial-reporting | 18.0 | `ae0fff3` | AGPL-3 | 1 | 1 | none |
| [module_auto_update](20.0/module_auto_update) | OCA/server-tools | 19.0 | `71de4de` | LGPL-3 | 13 | 13 | reviewed |
| [module_change_auto_install](20.0/module_change_auto_install) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 7 | 7 | none |
| [mrp_bom_component_mass_change](20.0/mrp_bom_component_mass_change) | OCA/manufacture | 19.0 | `c01ef60` | AGPL-3 | 14 | 14 | reviewed |
| [mrp_bom_structure_xlsx](20.0/mrp_bom_structure_xlsx) | OCA/manufacture-reporting | 19.0 | `ef6afd4` | AGPL-3 | 1 | 1 | reviewed |
| [mrp_bom_tracking](20.0/mrp_bom_tracking) | OCA/manufacture | 19.0 | `c01ef60` | LGPL-3 | 6 | 6 | reviewed |
| [mrp_lot_number_propagation](20.0/mrp_lot_number_propagation) | OCA/manufacture | 19.0 | `c01ef60` | AGPL-3 | 19 | 19 | reviewed |
| [mrp_stock_analytic](20.0/mrp_stock_analytic) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 11 | 11 | reviewed |
| [mrp_subcontracting_purchase_link](20.0/mrp_subcontracting_purchase_link) | OCA/manufacture | 19.0 | `c01ef60` | LGPL-3 | 3 | 3 | reviewed |
| [onchange_helper](20.0/onchange_helper) | OCA/server-tools | 19.0 | `71de4de` | LGPL-3 | 3 | 3 | reviewed |
| [openupgrade_framework](20.0/openupgrade_framework) | OCA/OpenUpgrade | 19.0 | `542cda3` | AGPL-3 | 2 | 2 | none |
| [operating_unit](20.0/operating_unit) | OCA/operating-unit | 19.0 | `df56d49` | LGPL-3 | 5 | 5 | reviewed |
| [partner_address_street3](20.0/partner_address_street3) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 6 | 6 | none |
| [partner_capital](20.0/partner_capital) | OCA/partner-contact | 18.0 | `de05f6d` | AGPL-3 | 2 | 2 | none |
| [partner_company_type](20.0/partner_company_type) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | reviewed |
| [partner_contact_address_default](20.0/partner_contact_address_default) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 3 | 3 | reviewed |
| [partner_contact_birthdate](20.0/partner_contact_birthdate) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | none |
| [partner_contact_gender](20.0/partner_contact_gender) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | none |
| [partner_deduplicate_acl](20.0/partner_deduplicate_acl) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 1 | 1 | reviewed |
| [partner_email_check](20.0/partner_email_check) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 16 | 16 | none |
| [partner_firstname](20.0/partner_firstname) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 36 | 40 | reviewed |
| [partner_identification](20.0/partner_identification) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 18 | 18 | none |
| [partner_industry_secondary](20.0/partner_industry_secondary) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 7 | 7 | reviewed |
| [partner_manual_rank](20.0/partner_manual_rank) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 2 | 2 | none |
| [partner_multi_relation](20.0/partner_multi_relation) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 48 | 49 | reviewed |
| [partner_ref_unique](20.0/partner_ref_unique) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 5 | 5 | reviewed |
| [partner_stage](20.0/partner_stage) | OCA/partner-contact | 19.0 | `26e80e9` | AGPL-3 | 6 | 6 | none |
| [password_security](20.0/password_security) | OCA/server-auth | 19.0 | `ae09869` | LGPL-3 | 40 | 40 | reviewed |
| [payroll](20.0/payroll) | OCA/payroll | 19.0 | `cbcaace` | LGPL-3 | 27 | 27 | reviewed |
| [payroll_account](20.0/payroll_account) | OCA/payroll | 18.0 | `d54bf91` | LGPL-3 | 3 | 3 | reviewed |
| [pdf_xml_attachment](20.0/pdf_xml_attachment) | OCA/reporting-engine | 19.0 | `ba46b0d` | LGPL-3 | 4 | 4 | reviewed |
| [portal_debranding](20.0/portal_debranding) | OCA/server-brand | 19.0 | `dacfe91` | LGPL-3 | 2 | 2 | none |
| [portal_odoo_debranding](20.0/portal_odoo_debranding) | OCA/server-brand | 18.0 | `4f378e5` | LGPL-3 | 1 | 1 | none |
| [product_abc_classification](20.0/product_abc_classification) | OCA/product-attribute | 18.0 | `aeb1f19` | AGPL-3 | 21 | 35 | reviewed |
| [product_assortment](20.0/product_assortment) | OCA/product-attribute | 18.0 | `aeb1f19` | AGPL-3 | 13 | 13 | reviewed |
| [product_brand](20.0/product_brand) | OCA/brand | 19.0 | `a89a1c2` | AGPL-3 | 3 | 3 | reviewed, accepted |
| [product_category_code](20.0/product_category_code) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 5 | 5 | reviewed |
| [product_code_unique](20.0/product_code_unique) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 2 | 2 | reviewed |
| [product_contract](20.0/product_contract) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 39 | 42 | none |
| [product_dimension](20.0/product_dimension) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 4 | 6 | none |
| [product_logistics_uom](20.0/product_logistics_uom) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 12 | 12 | reviewed, accepted |
| [product_lot_sequence](20.0/product_lot_sequence) | OCA/product-attribute | 18.0 | `aeb1f19` | AGPL-3 | 7 | 7 | reviewed |
| [product_net_weight](20.0/product_net_weight) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 3 | 3 | reviewed |
| [product_pack](20.0/product_pack) | OCA/product-pack | 19.0 | `3d3af23` | AGPL-3 | 12 | 12 | reviewed |
| [product_packaging_dimension](20.0/product_packaging_dimension) | OCA/product-attribute | 18.0 | `aeb1f19` | AGPL-3 | 3 | 3 | reviewed |
| [product_packaging_level](20.0/product_packaging_level) | OCA/product-attribute | 18.0 | `aeb1f19` | LGPL-3 | 11 | 11 | reviewed |
| [product_pricelist_direct_print](20.0/product_pricelist_direct_print) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 6 | 6 | reviewed |
| [product_secondary_unit](20.0/product_secondary_unit) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 10 | 10 | none |
| [product_sequence](20.0/product_sequence) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 16 | 16 | reviewed |
| [product_state](20.0/product_state) | OCA/product-attribute | 19.0 | `5545a68` | AGPL-3 | 5 | 5 | none |
| [product_variant_configurator](20.0/product_variant_configurator) | OCA/product-variant | 19.0 | `11d1c81` | AGPL-3 | 25 | 30 | reviewed |
| [project_forecast_line](20.0/project_forecast_line) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 73 | 73 | reviewed |
| [project_group](20.0/project_group) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 2 | 2 | reviewed |
| [project_hr](20.0/project_hr) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 6 | 6 | reviewed |
| [project_parent](20.0/project_parent) | OCA/project | 19.0 | `0e62631` | LGPL-3 | 2 | 2 | none |
| [project_sequence](20.0/project_sequence) | OCA/project | 19.0 | `0e62631` | LGPL-3 | 11 | 11 | reviewed |
| [project_stage_extra_info](20.0/project_stage_extra_info) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 1 | 1 | none |
| [project_sub_manager](20.0/project_sub_manager) | OCA/project | 18.0 | `36ab69b` | AGPL-3 | 4 | 4 | none |
| [project_tag_hierarchy](20.0/project_tag_hierarchy) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 3 | 3 | none |
| [project_task_code](20.0/project_task_code) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 12 | 12 | reviewed |
| [project_task_code_portal](20.0/project_task_code_portal) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 11 | 11 | reviewed, accepted |
| [project_task_default_user](20.0/project_task_default_user) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 8 | 8 | reviewed |
| [project_task_description_template](20.0/project_task_description_template) | OCA/project | 19.0 | `0e62631` | LGPL-3 | 2 | 2 | reviewed |
| [project_task_material](20.0/project_task_material) | OCA/project | 18.0 | `36ab69b` | AGPL-3 | 2 | 2 | reviewed |
| [project_task_name_with_id](20.0/project_task_name_with_id) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 2 | 2 | none |
| [project_task_parent_due_auto](20.0/project_task_parent_due_auto) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 7 | 7 | reviewed |
| [project_task_stage_state](20.0/project_task_stage_state) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 8 | 8 | reviewed |
| [project_template](20.0/project_template) | OCA/project | 18.0 | `36ab69b` | AGPL-3 | 4 | 4 | reviewed |
| [project_timeline](20.0/project_timeline) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 5 | 5 | reviewed |
| [project_type](20.0/project_type) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 2 | 2 | none |
| [project_version](20.0/project_version) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 2 | 2 | reviewed |
| [purchase_advance_payment](20.0/purchase_advance_payment) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 12 | 12 | reviewed |
| [purchase_allowed_product](20.0/purchase_allowed_product) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 2 | 2 | reviewed |
| [purchase_blanket_order](20.0/purchase_blanket_order) | OCA/purchase-workflow | 18.0 | `792b144` | AGPL-3 | 7 | 7 | reviewed |
| [purchase_delivery_split_date](20.0/purchase_delivery_split_date) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 16 | 16 | reviewed |
| [purchase_exception](20.0/purchase_exception) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 3 | 3 | reviewed |
| [purchase_force_invoiced](20.0/purchase_force_invoiced) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 2 | 2 | reviewed |
| [purchase_last_price_info](20.0/purchase_last_price_info) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 2 | 2 | reviewed |
| [purchase_order_approved](20.0/purchase_order_approved) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 7 | 7 | reviewed |
| [purchase_order_line_import_sheet_file](20.0/purchase_order_line_import_sheet_file) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 14 | 14 | reviewed |
| [purchase_order_line_sequence](20.0/purchase_order_line_sequence) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 3 | 3 | reviewed |
| [purchase_order_type](20.0/purchase_order_type) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 24 | 24 | reviewed |
| [purchase_reception_status](20.0/purchase_reception_status) | OCA/purchase-workflow | 19.0 | `f9031f1` | AGPL-3 | 3 | 3 | reviewed |
| [purchase_request](20.0/purchase_request) | OCA/purchase-workflow | 19.0 | `f9031f1` | LGPL-3 | 28 | 30 | reviewed |
| [purchase_requisition_line_description](20.0/purchase_requisition_line_description) | OCA/purchase-workflow | 18.0 | `792b144` | AGPL-3 | 1 | 1 | none |
| [purchase_sale_inter_company](20.0/purchase_sale_inter_company) | OCA/multi-company | 19.0 | `2992d5a` | AGPL-3 | 15 | 15 | none |
| [purchase_stock_analytic](20.0/purchase_stock_analytic) | OCA/account-analytic | 18.0 | `309045a` | AGPL-3 | 1 | 1 | reviewed |
| [purchase_stock_picking_invoice_link](20.0/purchase_stock_picking_invoice_link) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 7 | 7 | none |
| [report_py3o](20.0/report_py3o) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 14 | 14 | reviewed |
| [report_qweb_parameter](20.0/report_qweb_parameter) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 1 | 1 | reviewed |
| [report_wkhtmltopdf_param](20.0/report_wkhtmltopdf_param) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 2 | 2 | none |
| [report_xlsx_helper](20.0/report_xlsx_helper) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 1 | 1 | none |
| [report_xml](20.0/report_xml) | OCA/reporting-engine | 19.0 | `ba46b0d` | AGPL-3 | 3 | 3 | reviewed |
| [rma](20.0/rma) | OCA/rma | 19.0 | `4774c03` | AGPL-3 | 74 | 75 | reviewed |
| [rma_lot](20.0/rma_lot) | OCA/rma | 18.0 | `4e5260d` | AGPL-3 | 11 | 11 | reviewed |
| [rma_reason](20.0/rma_reason) | OCA/rma | 18.0 | `4e5260d` | AGPL-3 | 3 | 3 | reviewed |
| [rma_sale](20.0/rma_sale) | OCA/rma | 19.0 | `4774c03` | AGPL-3 | 38 | 38 | reviewed, accepted |
| [sale_advance_payment](20.0/sale_advance_payment) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 5 | 5 | reviewed |
| [sale_automatic_workflow](20.0/sale_automatic_workflow) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 18 | 18 | reviewed |
| [sale_blanket_order](20.0/sale_blanket_order) | OCA/sale-blanket | 19.0 | `c7243cd` | AGPL-3 | 25 | 25 | reviewed |
| [sale_cancel_reason](20.0/sale_cancel_reason) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 3 | 3 | none |
| [sale_commission_oca](20.0/sale_commission_oca) | OCA/commission | 19.0 | `3649f32` | AGPL-3 | 4 | 4 | none |
| [sale_delivery_state](20.0/sale_delivery_state) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 10 | 10 | none |
| [sale_elaboration](20.0/sale_elaboration) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 10 | 10 | reviewed |
| [sale_financial_risk](20.0/sale_financial_risk) | OCA/credit-control | 19.0 | `ade8df1` | AGPL-3 | 7 | 7 | reviewed |
| [sale_force_invoiced](20.0/sale_force_invoiced) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 1 | 1 | none |
| [sale_order_general_discount](20.0/sale_order_general_discount) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 11 | 11 | reviewed |
| [sale_order_general_discount_triple](20.0/sale_order_general_discount_triple) | OCA/sale-workflow | 18.0 | `2aff3053` | AGPL-3 | 12 | 12 | reviewed |
| [sale_order_line_input](20.0/sale_order_line_input) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 2 | 2 | reviewed |
| [sale_order_lot_selection](20.0/sale_order_lot_selection) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 6 | 6 | reviewed, accepted |
| [sale_order_revision](20.0/sale_order_revision) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 1 | 1 | none |
| [sale_order_secondary_unit](20.0/sale_order_secondary_unit) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 10 | 10 | reviewed |
| [sale_partner_incoterm](20.0/sale_partner_incoterm) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 1 | 1 | none |
| [sale_partner_sale_contact](20.0/sale_partner_sale_contact) | OCA/sale-workflow | 19.0 | `e62b0e15` | LGPL-3 | 16 | 16 | none |
| [sale_partner_selectable_option](20.0/sale_partner_selectable_option) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 1 | 1 | reviewed |
| [sale_payment_sheet](20.0/sale_payment_sheet) | OCA/sale-workflow | 18.0 | `2aff3053` | AGPL-3 | 9 | 9 | none |
| [sale_product_pack](20.0/sale_product_pack) | OCA/product-pack | 19.0 | `3d3af23` | AGPL-3 | 8 | 8 | reviewed |
| [sale_product_set](20.0/sale_product_set) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 13 | 13 | reviewed |
| [sale_project_task_recurrency](20.0/sale_project_task_recurrency) | OCA/project | 19.0 | `0e62631` | AGPL-3 | 18 | 18 | reviewed |
| [sale_stock_available_info_popup](20.0/sale_stock_available_info_popup) | OCA/stock-logistics-availability | 19.0 | `f6f0272` | AGPL-3 | 2 | 2 | none |
| [sale_stock_partner_warehouse](20.0/sale_stock_partner_warehouse) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 7 | 7 | reviewed |
| [sale_stock_picking_blocking](20.0/sale_stock_picking_blocking) | OCA/sale-workflow | 19.0 | `e62b0e1` | AGPL-3 | 8 | 8 | reviewed |
| [sale_stock_picking_invoice_link](20.0/sale_stock_picking_invoice_link) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 7 | 7 | reviewed |
| [sale_stock_picking_note](20.0/sale_stock_picking_note) | OCA/sale-workflow | 19.0 | `e62b0e15` | AGPL-3 | 3 | 3 | reviewed |
| [sale_stock_prebook](20.0/sale_stock_prebook) | OCA/sale-prebook | 19.0 | `b7aa629` | LGPL-3 | 7 | 7 | reviewed |
| [sale_timesheet_invoice_link](20.0/sale_timesheet_invoice_link) | OCA/timesheet | 19.0 | `daaa000` | LGPL-3 | 15 | 15 | reviewed |
| [sentry](20.0/sentry) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 26 | 26 | reviewed |
| [sequence_check_digit](20.0/sequence_check_digit) | OCA/server-ux | 18.0 | `c69ed17` | LGPL-3 | 13 | 13 | none |
| [sequence_reset_period](20.0/sequence_reset_period) | OCA/server-ux | 19.0 | `ecb65d1` | LGPL-3 | 9 | 9 | none |
| [server_action_mass_edit](20.0/server_action_mass_edit) | OCA/server-ux | 19.0 | `ecb65d1` | AGPL-3 | 13 | 13 | reviewed |
| [server_action_navigate](20.0/server_action_navigate) | OCA/server-backend | 19.0 | `d6b0897` | AGPL-3 | 5 | 5 | none |
| [server_environment](20.0/server_environment) | OCA/server-env | 19.0 | `7172600` | LGPL-3 | 17 | 17 | none |
| [server_environment_data_encryption](20.0/server_environment_data_encryption) | OCA/server-env | 18.0 | `dc737ed` | AGPL-3 | 2 | 2 | reviewed |
| [session_db](20.0/session_db) | OCA/server-tools | 19.0 | `71de4de` | LGPL-3 | 7 | 7 | reviewed |
| [shopify_connector_account](20.0/shopify_connector_account) | OCA/connector-shopify | 19.0 | `1a89d16` | AGPL-3 | 29 | 29 | none |
| [social_media_base](20.0/social_media_base) | OCA/social | 18.0 | `75b2203` | AGPL-3 | 328 | 329 | reviewed, accepted |
| [social_media_linkedin](20.0/social_media_linkedin) | OCA/social | 18.0 | `75b2203` | AGPL-3 | 235 | 235 | reviewed |
| [spec_driven_model](20.0/spec_driven_model) | OCA/l10n-brazil | 18.0 | `c50420c` | LGPL-3 | 13 | 13 | reviewed |
| [stock_analytic](20.0/stock_analytic) | OCA/account-analytic | 19.0 | `502ac4e` | AGPL-3 | 10 | 10 | reviewed |
| [stock_available](20.0/stock_available) | OCA/stock-logistics-availability | 19.0 | `f6f0272` | AGPL-3 | 2 | 2 | reviewed |
| [stock_cycle_count](20.0/stock_cycle_count) | OCA/stock-logistics-warehouse | 18.0 | `ee3167c` | AGPL-3 | 14 | 14 | reviewed |
| [stock_demand_estimate_matrix](20.0/stock_demand_estimate_matrix) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | AGPL-3 | 8 | 8 | none |
| [stock_inventory](20.0/stock_inventory) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | LGPL-3 | 18 | 18 | reviewed |
| [stock_inventory_discrepancy](20.0/stock_inventory_discrepancy) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | AGPL-3 | 4 | 4 | reviewed |
| [stock_inventory_preparation_filter](20.0/stock_inventory_preparation_filter) | OCA/stock-logistics-warehouse | 18.0 | `ee3167c` | AGPL-3 | 2 | 2 | reviewed |
| [stock_location_is_sublocation](20.0/stock_location_is_sublocation) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | LGPL-3 | 7 | 7 | none |
| [stock_move_common_dest](20.0/stock_move_common_dest) | OCA/stock-logistics-warehouse | 18.0 | `ee3167c` | AGPL-3 | 2 | 2 | reviewed |
| [stock_move_line_change_lot](20.0/stock_move_line_change_lot) | OCA/stock-logistics-workflow | 18.0 | `0d3301f` | AGPL-3 | 11 | 11 | reviewed |
| [stock_move_line_qty_picked](20.0/stock_move_line_qty_picked) | OCA/stock-logistics-workflow | 18.0 | `0d3301f` | AGPL-3 | 4 | 4 | reviewed |
| [stock_move_location](20.0/stock_move_location) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | AGPL-3 | 12 | 12 | reviewed |
| [stock_move_quantity_product_uom](20.0/stock_move_quantity_product_uom) | OCA/stock-logistics-warehouse | 19.0 | `2d54780` | LGPL-3 | 1 | 1 | reviewed |
| [stock_no_negative](20.0/stock_no_negative) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 5 | 5 | reviewed |
| [stock_owner_restriction](20.0/stock_owner_restriction) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 13 | 13 | reviewed |
| [stock_picking_back2draft](20.0/stock_picking_back2draft) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 1 | 1 | reviewed |
| [stock_picking_completion_info](20.0/stock_picking_completion_info) | OCA/stock-logistics-warehouse | 18.0 | `ee3167c` | AGPL-3 | 11 | 11 | reviewed |
| [stock_picking_delivery_link](20.0/stock_picking_delivery_link) | OCA/delivery-carrier | 18.0 | `95c525a` | AGPL-3 | 3 | 3 | reviewed |
| [stock_picking_delivery_package_type_domain](20.0/stock_picking_delivery_package_type_domain) | OCA/delivery-carrier | 18.0 | `95c525a` | AGPL-3 | 5 | 5 | reviewed |
| [stock_picking_line_sequence](20.0/stock_picking_line_sequence) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 4 | 4 | reviewed |
| [stock_picking_progress](20.0/stock_picking_progress) | OCA/stock-logistics-workflow | 18.0 | `0d3301f` | AGPL-3 | 5 | 5 | reviewed |
| [stock_picking_purchase_order_link](20.0/stock_picking_purchase_order_link) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 1 | 1 | reviewed |
| [stock_picking_report_valued](20.0/stock_picking_report_valued) | OCA/stock-logistics-reporting | 19.0 | `501706a` | AGPL-3 | 5 | 5 | none |
| [stock_picking_return_lot](20.0/stock_picking_return_lot) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 7 | 7 | reviewed |
| [stock_picking_return_restricted_qty](20.0/stock_picking_return_restricted_qty) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 4 | 4 | reviewed |
| [stock_picking_variable_qty](20.0/stock_picking_variable_qty) | OCA/stock-logistics-workflow | 18.0 | `0d3301f` | LGPL-3 | 22 | 22 | reviewed |
| [stock_quant_manual_assign](20.0/stock_quant_manual_assign) | OCA/stock-logistics-reservation | 19.0 | `4c6d209` | AGPL-3 | 5 | 5 | reviewed |
| [stock_quant_package_dimension](20.0/stock_quant_package_dimension) | OCA/stock-logistics-tracking | 18.0 | `0392600` | AGPL-3 | 3 | 3 | reviewed |
| [stock_quant_package_product_packaging](20.0/stock_quant_package_product_packaging) | OCA/stock-logistics-tracking | 18.0 | `0392600` | AGPL-3 | 10 | 11 | reviewed |
| [stock_split_picking](20.0/stock_split_picking) | OCA/stock-logistics-workflow | 19.0 | `3057a91` | AGPL-3 | 16 | 16 | reviewed |
| [subscription_oca](20.0/subscription_oca) | OCA/contract | 19.0 | `882afdf` | AGPL-3 | 62 | 62 | reviewed |
| [tracking_manager](20.0/tracking_manager) | OCA/server-tools | 19.0 | `71de4de` | AGPL-3 | 21 | 21 | reviewed |
| [uom_alias](20.0/uom_alias) | OCA/product-attribute | 19.0 | `5545a68` | LGPL-3 | 2 | 2 | none |
| [web_chatter_position](20.0/web_chatter_position) | OCA/web | 19.0 | `1f57640` | LGPL-3 | 1 | 1 | reviewed, accepted |
| [web_company_color](20.0/web_company_color) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 7 | 7 | reviewed |
| [web_dark_mode](20.0/web_dark_mode) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 10 | 10 | reviewed, accepted |
| [web_form_banner](20.0/web_form_banner) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 8 | 8 | none |
| [web_ir_actions_act_window_message](20.0/web_ir_actions_act_window_message) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 1 | 1 | reviewed |
| [web_m2x_options_manager](20.0/web_m2x_options_manager) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 7 | 7 | none |
| [web_notify](20.0/web_notify) | OCA/web | 19.0 | `1f57640` | LGPL-3 | 8 | 8 | none |
| [web_theme_classic](20.0/web_theme_classic) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 6 | 6 | reviewed, accepted |
| [web_widget_dropdown_dynamic](20.0/web_widget_dropdown_dynamic) | OCA/web | 19.0 | `1f57640` | LGPL-3 | 5 | 5 | none |
| [web_widget_x2many_2d_matrix](20.0/web_widget_x2many_2d_matrix) | OCA/web | 19.0 | `1f57640` | AGPL-3 | 1 | 1 | none |
| [webservice_core](20.0/webservice_core) | OCA/web-api | 18.0 | `50c4d89` | AGPL-3 | 54 | 55 | none |
| [website_require_login](20.0/website_require_login) | OCA/website | 19.0 | `d8318b7` | LGPL-3 | 2 | 2 | reviewed |
| [website_sale_checkout_skip_payment](20.0/website_sale_checkout_skip_payment) | OCA/e-commerce | 19.0 | `36f5b14` | LGPL-3 | 2 | 2 | reviewed |
| [website_sale_stock_provisioning_date](20.0/website_sale_stock_provisioning_date) | OCA/e-commerce | 19.0 | `36f5b14` | AGPL-3 | 2 | 2 | none |

## Dependencies that are not in this folder

Some listed modules depend on a community module that is not listed here. The tests above ran with that module installed. A module is never listed while a module it depends on has a defect we know of.

- **community 20.0**: the OCA already publishes the module for Odoo 20.0; use theirs.
- **no tests of its own**: we ported it, it installs and its dependents' tests pass with it; modules without tests are not in this repository.
- **not all of its tests run yet**: we ported it and it passes, but some of its own tests do not start on our test machine, so it does not meet the rule for this folder.

| Dependency | Why it is not listed | Needed by |
|---|---|---|
| `account_financial_risk` | community 20.0 | `sale_financial_risk` |
| `account_payment_base_oca` | no tests of its own | `account_payment_base_oca_sale` |
| `account_statement_import_base` | no tests of its own | `account_statement_import_file`, `account_statement_import_generate_unique_id`, `account_statement_import_online` |
| `analytic_operating_unit` | no tests of its own | `account_operating_unit` |
| `base_cron_exclusion` | community 20.0 | `ddmrp` |
| `base_maintenance` | no tests of its own | `maintenance_equipment_contract`, `maintenance_equipment_status`, `maintenance_plan` |
| `base_unece` | no tests of its own | `account_tax_unece` |
| `base_user_role` | not all of its tests run yet | `base_user_role_company`, `base_user_role_history` |
| `base_view_inheritance_extension` | community 20.0 | `account_invoice_transmit_method`, `account_operating_unit`, `purchase_allowed_product`, `purchase_blanket_order`, `stock_inventory_preparation_filter`, `web_m2x_options_manager` |
| `component_event` | not all of its tests run yet | `connector` |
| `date_range` | community 20.0 | `account_financial_report`, `account_tax_balance`, `l10n_it_account`, `mis_builder`, `stock_demand_estimate_matrix` |
| `dms` | community 20.0 | `dms_auto_classification` |
| `document_knowledge` | community 20.0 | `document_page_access_group` |
| `document_page` | community 20.0 | `document_page_access_group`, `document_page_reference` |
| `l10n_br_account` | not all of its tests run yet | `l10n_br_contract`, `l10n_br_purchase`, `l10n_br_sale` |
| `l10n_br_coa` | not all of its tests run yet | `l10n_br_coa_generic`, `l10n_br_coa_simple` |
| `l10n_br_fiscal` | not all of its tests run yet | `l10n_br_fiscal_certificate`, `l10n_br_fiscal_dfe`, `l10n_br_fiscal_edi` |
| `l10n_fr_state` | community 20.0 | `l10n_fr_department` |
| `l10n_it_edi_sdi` | no tests of its own | `l10n_it_edi_pec` |
| `mrp_multi_level` | community 20.0 | `ddmrp` |
| `partner_contact_personal_information_page` | community 20.0 | `partner_contact_birthdate`, `partner_contact_gender` |
| `product_set` | community 20.0 | `sale_product_set` |
| `queue_job` | community 20.0 | `connector`, `ddmrp_cron_actions_as_job`, `edi_queue_oca`, `l10n_br_fiscal_dfe` |
| `report_xlsx` | community 20.0 | `account_financial_report`, `l10n_nl_tax_statement`, `mis_builder`, `mrp_bom_structure_xlsx`, `report_xlsx_helper` |
| `sale_triple_discount` | not all of its tests run yet | `sale_order_general_discount_triple` |
| `shopify_connector` | not all of its tests run yet | `shopify_connector_account` |
| `sql_request_abstract` | no tests of its own | `bi_sql_editor` |
| `stock_demand_estimate` | community 20.0 | `ddmrp`, `stock_demand_estimate_matrix` |
| `stock_picking_invoice_link` | community 20.0 | `purchase_stock_picking_invoice_link`, `sale_stock_picking_invoice_link` |
| `stock_restrict_lot` | community 20.0 | `sale_order_lot_selection`, `stock_picking_return_lot` |
| `stock_warehouse_calendar` | community 20.0 | `ddmrp` |
| `uom_unece` | no tests of its own | `base_business_document_import` |
| `web_m2x_options` | community 20.0 | `web_m2x_options_manager` |
| `web_timeline` | community 20.0 | `project_timeline` |
| `web_widget_bokeh_chart` | community 20.0 | `ddmrp` |
