# GreenLoop Collect Ltd

GreenLoop is a fictional small business collecting separated food waste and coffee grounds in the fictional city of Northbridge.
Its customer Copper Kettle operates workplace dining rooms and cafes through Juniper Table Services Ltd.
The account file includes an earlier service provider, later GreenLoop billing, receiving-facility records and management working papers.

This English dossier is synthetic benchmark data. Names, addresses, identifiers, commercial values and prose were authored for this exercise.
Contacts use `.example` domains; record and payment identifiers are explicitly non-operational test strings.
The tax convention belongs to the fictional account and does not describe an actual tax regime.

The documents exercise reconstruction of an ordinary business file: contracts, monthly invoices, weekly collection records, an annual review with a four-month update, account summaries and proposed future work.
Treat statements as belonging to their documents. Working papers and exports may describe different periods and levels of detail.
No reference annotations or expected answers are included in this directory.

There are **28 document files representing 27 logical sources**. The manifest uses one source entry with two representations for the repeated register.
The six invoice documents include five collection invoices and one treatment invoice.
Two CSV sheets retain monthly aggregates and individual visits. Blank fields remain blank.
The customer review contains sixteen explicit pages. Multipage Markdown uses `--- page N ---` markers.
An unpaginated sheet has one logical page; CSV citations can add a row number, with the header at row 1.

The two weigh tickets and the corrected certificate are supplied in the permitted Markdown fallback because Pandoc and WeasyPrint were unavailable in the authoring environment.
The manifest hashes the supplied representations. File copies do not create another independent source.

## Provenance of the form

The form of these documents is deliberately modelled on a real private dossier from a small business in the same line of work. All substance is synthetic. The versioned leakage checker at `../../scripts/leak_check.py` tests every document and root file, including the manifest, against a private source-derived blocklist; its recorded zero-leak result supports this separation of form and substance.

## Inventory

| Source | Document | Pages | Nature |
| --- | --- | --- | --- |
| gl-01 | [01-contract-summary.md](documents/01-contract-summary.md) | 1 | internal contract summary |
| gl-02 | [02-signed-service-agreement.md](documents/02-signed-service-agreement.md) | 4 | signed service agreement |
| gl-03 | [03-receivables-summary.md](documents/03-receivables-summary.md) | 1 | internal financial summary |
| gl-04 | [04-receivables-worksheet.md](documents/04-receivables-worksheet.md) | 1 | receivables spreadsheet representation |
| gl-05 | [05-contract-notice-diary.md](documents/05-contract-notice-diary.md) | 1 | internal contract and notice summary |
| gl-06 | [06-expansion-offer-card.md](documents/06-expansion-offer-card.md) | 1 | reconstructed commercial proposal and costing |
| gl-07 | [07-revised-site-rates.md](documents/07-revised-site-rates.md) | 1 | internal tariff revision |
| gl-08 | [08-certification-preparation.md](documents/08-certification-preparation.md) | 1 | internal certificate preparation and revision note |
| gl-09 | [09-january-scale-export.md](documents/09-january-scale-export.md) | 1 | monthly weighing spreadsheet export |
| gl-10 | [10-billing-index.md](documents/10-billing-index.md) | 1 | internal invoice index |
| gl-11 | [11-invoice-mw-c-jan-h8k.md](documents/11-invoice-mw-c-jan-h8k.md) | 2 | customer collection invoice |
| gl-12 | [12-invoice-mw-c-nov-l6v.md](documents/12-invoice-mw-c-nov-l6v.md) | 2 | customer collection invoice |
| gl-13 | [13-invoice-gl-t-feb-b7z.md](documents/13-invoice-gl-t-feb-b7z.md) | 1 | customer treatment invoice |
| gl-14 | [14-invoice-gl-c-feb-n9d.md](documents/14-invoice-gl-c-feb-n9d.md) | 2 | customer collection invoice |
| gl-15 | [15-invoice-mw-c-dec-r7p.md](documents/15-invoice-mw-c-dec-r7p.md) | 2 | customer collection invoice |
| gl-16 | [16-invoice-gl-c-sep-u6w.md](documents/16-invoice-gl-c-sep-u6w.md) | 2 | customer collection invoice |
| gl-17 | [17-collection-register.md](documents/17-collection-register.md) | 1 | reconstructed collection register |
| gl-18 | [18-weigh-ticket-index.md](documents/18-weigh-ticket-index.md) | 1 | reconstructed weigh ticket index |
| gl-19 | [19-transfer-scenario.md](documents/19-transfer-scenario.md) | 1 | internal business transfer scenario |
| gl-20 | [20-internal-service-review.md](documents/20-internal-service-review.md) | 1 | reconstructed internal service report |
| gl-21 | [21-monthly-collections.csv](documents/21-monthly-collections.csv) | 1 | monthly collection and mass aggregates |
| gl-22 | [22-recorded-visits.csv](documents/22-recorded-visits.csv) | 1 | per-visit weighing table |
| gl-23 | [23-treatment-certificate-corrected.md](documents/23-treatment-certificate-corrected.md) | 1 | customer treatment certification |
| gl-24 | [24-customer-review.md](documents/24-customer-review.md) | 16 | sixteen-page customer collection and treatment report |
| gl-25 | [25-weigh-ticket-station-house.md](documents/25-weigh-ticket-station-house.md) | 1 | final weigh ticket and handover form |
| gl-26 | [26-weigh-ticket-quarry-tower-provisional.md](documents/26-weigh-ticket-quarry-tower-provisional.md) | 1 | provisional weigh ticket |
| gl-27 | [27-june-invoice-preparation.md](documents/27-june-invoice-preparation.md) | 1 | internal invoice preparation draft |
| gl-17 (file copy) | [28-collection-register-file-copy.md](documents/28-collection-register-file-copy.md) | 1 | second file representation of the collection register |

## Manifest and use

`manifest.json` uses `dossier-manifest/1.0.0` and a `sources` array. Each source records its file hash, pagination, date precision and documentary roles.
An unknown date is null; a month-only date has no fabricated day. Recipient and signatory lists are empty where the document does not identify them.
Data licensing follows [the benchmark data licence](../../DATA-LICENSE.md).
