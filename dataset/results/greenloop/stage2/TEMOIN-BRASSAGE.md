# Témoin de brassage

Date : 2026-09-27

Instrument resserré le 2026-09-24 sur revue indépendante (#129) ; les chiffres « avant » ci-dessous restent la référence publiée avant ce resserrement.
JSON régénérés le 25/09 avec l'instrument courant.

Appariement : rotation d'un cran sur les questions triées par identifiant (question *i* évaluée contre le contexte de *i+1*).

Métrique : **tout tient** (toutes les assertions de soutien présentes dans le contexte).

Dénominateur appui : **141** (même sélection que la mesure étage 2).


## Hors étage 2

- sans assertion d'appui (2) : gl-q133 (unknown), gl-q134 (unknown) (jamais « tout tient », listées pour traçabilité).

## Avant / après resserrement / après correction invariant

| fournisseur | mode | signal avant | témoin avant | signal après resserrement | témoin après resserrement | signal après correction | témoin après correction | écart correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| brain_prod | verbatim | 39 | 4 | 39 | 4 | — | — | — |
| brain_prod | valeur | 49 | 4 | 37 | 4 | — | — | — |
| rag_naif | verbatim | 85 | 46 | 85 | 46 | — | — | — |
| rag_naif | valeur | 90 | 48 | 71 | 43 | — | — | — |
| brain_banc | verbatim | 84 | 23 | 84 | 23 | 84 | 23 | 61 |
| brain_banc | valeur | 89 | 32 | 75 | 22 | 87 | 24 | 63 |
| mem0 | verbatim | 2 | 0 | 2 | 0 | — | — | — |
| mem0 | valeur | 47 | 19 | 28 | 15 | — | — | — |

| fournisseur | mode | signal (vrai appariement) | témoin (brassé) | écart |
| --- | --- | --- | --- | --- |
| brain_banc | verbatim | 84/141 | 23/141 | 61 |
| brain_banc | valeur | 87/141 | 24/141 | 63 |
| brain_banc_v3 | verbatim | 87/141 | 28/141 | 59 |
| brain_banc_v3 | valeur | 90/141 | 28/141 | 62 |
| brain_banc_v4 | verbatim | 87/141 | 29/141 | 58 |
| brain_banc_v4 | valeur | 90/141 | 29/141 | 61 |

## Lecture

brain_banc : signal valeur 87/141, témoin 24/141 (écart 63). brain_banc_v3 : signal valeur 90/141, témoin 28/141 (écart 62). brain_banc_v4 : signal valeur 90/141, témoin 29/141 (écart 61).

### brain_banc

## Assertions tenues par le témoin (mode valeur)

| assertion | pièce | citation (80 car.) | discriminant |
| --- | --- | --- | --- |
| gl-a1703 | 05-contract-notice-diary.md | Oat Lantern Bakery Ltd | 2024-07-17 | Annual / six weeks | Summary only | date 17/07/2024 |
| gl-a1704 | 05-contract-notice-diary.md | Silver Apron Dining Ltd | 2024-10-14 | Annual / written notice; length unrecorde… | date 14/10/2024 |
| gl-a1715 | 06-expansion-offer-card.md | | Mill Road | 26 Kettle Street | 2 | 1.931 | cargo cycle | | nombre 26 (word:road), nombre 2 (word:street) |
| gl-a1719 | 06-expansion-offer-card.md | | West Yard | 68 Fern Reach | 1 | 2.183 | electric van | | nombre 68 (word:yard), nombre 1 (word:reach), nombre 2183 (word:reach) |
| gl-a1699 | 03-receivables-summary.md | No bank statement accompanies this note. | repli lexical (recouvrance substantielle) |
| gl-a1904 | 10-billing-index.md | | INV-2025-061 | 2025-01-11 | Oat Lantern Bakery Ltd | 771.02 | 123.36 | 894.38 … | nombre 61 (word:inv), nombre 771.02 (word:ltd), nombre 123.36 (word:ltd), nombre 894.38 (word:ltd), nombre 9 (word:arch), date 11/01/2025, texte «INV», texte «ARCH», texte «Q9M» |
| gl-a1948 | 11-invoice-mw-c-jan-h8k.md | **Payment terms: 30 days after issue.** Printed due date: 2025-03-14. | nombre 30 (days), date 14/03/2025 |
| gl-a1989 | 15-invoice-mw-c-dec-r7p.md | **Payment terms: 30 days after issue.** Printed due date: 2025-02-15. | nombre 30 (days), date 15/02/2025 |
| gl-a2010 | 14-invoice-gl-c-feb-n9d.md | **Payment terms: Due on receipt.** Printed due date: 2025-03-18. | date 18/03/2025 |
| gl-a1886 | 09-january-scale-export.md | | Paper Hall | 6 | 6 | 0 | 48 L | 0 | | nombre 6 (word:hall), nombre 0 (word:hall), nombre 48 (word:hall) |
| gl-a1757 | 09-january-scale-export.md | Sheet cells contain the day's summed readings, so two ticket records may share a… | repli lexical (recouvrance substantielle) |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2034 | 20-internal-service-review.md | Prior-year collections | site and month | Invoice transcription | Underlying inv… | repli lexical (recouvrance substantielle) |
| gl-a1723 | 06-expansion-offer-card.md | Existing active locations | 7821.43 | 3417.29 | 2789.63 | 14028.35 | nombre 7821.43 (word:locations), nombre 3417.29 (word:locations), nombre 2789.63 (word:locations), nombre 14028.4 (word:locations) |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2055 | 20-internal-service-review.md | There are 77 not_weighed visits in 45 complete Circuit A runs, among 285 visits. | nombre 77 (word:there), nombre 45 (word:visits), nombre 285 (word:among) |
| gl-a2019 | 16-invoice-gl-c-sep-u6w.md | **Payment terms: Due on receipt.** Printed due date: 2025-10-08. | date 08/10/2025 |
| gl-a1167 | 17-collection-register.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2043 | 20-internal-service-review.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2073 | 24-customer-review.md | **Total recovered mass** | **20.405 t** | nombre 20405 (word:mass) |
| gl-a2356 | 24-customer-review.md | The client review records **683 collections across 11 collected sites** for the … | nombre 683 (word:records), nombre 11 (word:across) |
| gl-a2362 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2199 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a2363 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2225 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2366 | 17-collection-register.md | | Beacon Court | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 52 | | nombre 4 (word:court), nombre 5 (word:court), nombre 52 (word:court) |
| gl-a2367 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a2369 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2290 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a1177 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2187 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a1184 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a1192 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2203 | 24-customer-review.md | | Mill Road | 10 | 9 | 8 | 10 | 8 | 10 | 8 | 9 | 8 | 8 | 8 | 9 | 105 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 105 (word:road) |
| gl-a1196 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a1202 | 17-collection-register.md | | Roast Kitchen | 10 | 8 | 8 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 102 | | nombre 10 (word:kitchen), nombre 8 (word:kitchen), nombre 9 (word:kitchen), nombre 102 (word:kitchen) |
| gl-a2214 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2223 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a1237 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a1261 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2278 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a1264 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2281 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a1265 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2282 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a2056 | 20-internal-service-review.md | | 2025-01 | 20 | 1016.419 | 866.464 | 1882.883 | 1016.419 | | nombre 1, nombre 20, nombre 1016.42, nombre 866464, nombre 1882.88 |
| gl-a2057 | 20-internal-service-review.md | | 2025-02 | 20 | 766.768 | 866.464 | 1633.232 | 766.768 | | nombre 2, nombre 20, nombre 766768, nombre 866464, nombre 1633.23 |
| gl-a2171 | 24-customer-review.md | A not_weighed ticket has no raw_kg. It is a completed collection, not a zero or … | repli lexical (recouvrance substantielle) |
| gl-a2171 | 24-customer-review.md | A not_weighed ticket has no raw_kg. It is a completed collection, not a zero or … | repli lexical (recouvrance substantielle) |
| gl-a1736 | 07-revised-site-rates.md | Invoice INV-2025-069, issued in March for February service, carries **GBP 14.83 … | nombre 69 (word:inv), nombre 14.83 (word:gbp), texte «INV», texte «GBP» |

_… et 4 autres assertions._

### brain_banc_v3

## Assertions tenues par le témoin (mode valeur)

| assertion | pièce | citation (80 car.) | discriminant |
| --- | --- | --- | --- |
| gl-a1639 | 02-signed-service-agreement.md | The customer remains responsible for the contents of each container until collec… | repli lexical (recouvrance substantielle) |
| gl-a1651 | 02-signed-service-agreement.md | Late balances carry simple interest at **4.6 percent per year** from the day aft… | nombre 4.6 (percent) |
| gl-a1703 | 05-contract-notice-diary.md | Oat Lantern Bakery Ltd | 2024-07-17 | Annual / six weeks | Summary only | date 17/07/2024 |
| gl-a1704 | 05-contract-notice-diary.md | Silver Apron Dining Ltd | 2024-10-14 | Annual / written notice; length unrecorde… | date 14/10/2024 |
| gl-a1715 | 06-expansion-offer-card.md | | Mill Road | 26 Kettle Street | 2 | 1.931 | cargo cycle | | nombre 26 (word:road), nombre 2 (word:street) |
| gl-a1719 | 06-expansion-offer-card.md | | West Yard | 68 Fern Reach | 1 | 2.183 | electric van | | nombre 68 (word:yard), nombre 1 (word:reach), nombre 2183 (word:reach) |
| gl-a1716 | 06-expansion-offer-card.md | | Roast Kitchen | 31 Copperleaf Way | 2 | 8.417 | electric van | | nombre 31 (word:kitchen), nombre 2 (word:way), nombre 8417 (word:way) |
| gl-a1699 | 03-receivables-summary.md | No bank statement accompanies this note. | repli lexical (recouvrance substantielle) |
| gl-a1904 | 10-billing-index.md | | INV-2025-061 | 2025-01-11 | Oat Lantern Bakery Ltd | 771.02 | 123.36 | 894.38 … | nombre 61 (word:inv), nombre 771.02 (word:ltd), nombre 123.36 (word:ltd), nombre 894.38 (word:ltd), nombre 9 (word:arch), date 11/01/2025, texte «INV», texte «ARCH», texte «Q9M» |
| gl-a1948 | 11-invoice-mw-c-jan-h8k.md | **Payment terms: 30 days after issue.** Printed due date: 2025-03-14. | nombre 30 (days), date 14/03/2025 |
| gl-a1969 | 12-invoice-mw-c-nov-l6v.md | **Payment terms: 30 days after issue.** Printed due date: 2025-01-11. | nombre 30 (days), date 11/01/2025 |
| gl-a1989 | 15-invoice-mw-c-dec-r7p.md | **Payment terms: 30 days after issue.** Printed due date: 2025-02-15. | nombre 30 (days), date 15/02/2025 |
| gl-a2010 | 14-invoice-gl-c-feb-n9d.md | **Payment terms: Due on receipt.** Printed due date: 2025-03-18. | date 18/03/2025 |
| gl-a1886 | 09-january-scale-export.md | | Paper Hall | 6 | 6 | 0 | 48 L | 0 | | nombre 6 (word:hall), nombre 0 (word:hall), nombre 48 (word:hall) |
| gl-a1757 | 09-january-scale-export.md | Sheet cells contain the day's summed readings, so two ticket records may share a… | repli lexical (recouvrance substantielle) |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2034 | 20-internal-service-review.md | Prior-year collections | site and month | Invoice transcription | Underlying inv… | repli lexical (recouvrance substantielle) |
| gl-a1723 | 06-expansion-offer-card.md | Existing active locations | 7821.43 | 3417.29 | 2789.63 | 14028.35 | nombre 7821.43 (word:locations), nombre 3417.29 (word:locations), nombre 2789.63 (word:locations), nombre 14028.4 (word:locations) |
| gl-a2032 | 19-transfer-scenario.md | For **2025-06**, the retained preparation model contains **52 planned visits**, … | nombre 6, nombre 52 (word:contains), nombre 1399 (word:gbp), texte «GBP» |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2055 | 20-internal-service-review.md | There are 77 not_weighed visits in 45 complete Circuit A runs, among 285 visits. | nombre 77 (word:there), nombre 45 (word:visits), nombre 285 (word:among) |
| gl-a2056 | 20-internal-service-review.md | | 2025-01 | 20 | 1016.419 | 866.464 | 1882.883 | 1016.419 | | nombre 1, nombre 20, nombre 1016.42, nombre 866464, nombre 1882.88 |
| gl-a2057 | 20-internal-service-review.md | | 2025-02 | 20 | 766.768 | 866.464 | 1633.232 | 766.768 | | nombre 2, nombre 20, nombre 766768, nombre 866464, nombre 1633.23 |
| gl-a2058 | 20-internal-service-review.md | | 2025-03 | 0 | 1601.373 | 0.000 | 1601.373 | 1601.373 | | nombre 3, nombre 0, nombre 1601.37 |
| gl-a2019 | 16-invoice-gl-c-sep-u6w.md | **Payment terms: Due on receipt.** Printed due date: 2025-10-08. | date 08/10/2025 |
| gl-a1167 | 17-collection-register.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2043 | 20-internal-service-review.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2073 | 24-customer-review.md | **Total recovered mass** | **20.405 t** | nombre 20405 (word:mass) |
| gl-a1756 | 08-certification-preparation.md | Its detailed total is 20.405 t; the customer summary and corrected certificate c… | nombre 20405 (word:total), nombre 20415 (word:carry) |
| gl-a2356 | 24-customer-review.md | The client review records **683 collections across 11 collected sites** for the … | nombre 683 (word:records), nombre 11 (word:across) |
| gl-a2362 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2199 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a2363 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2225 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2366 | 17-collection-register.md | | Beacon Court | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 52 | | nombre 4 (word:court), nombre 5 (word:court), nombre 52 (word:court) |
| gl-a2367 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a2369 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2290 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a1177 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2187 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a1184 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a1192 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2203 | 24-customer-review.md | | Mill Road | 10 | 9 | 8 | 10 | 8 | 10 | 8 | 9 | 8 | 8 | 8 | 9 | 105 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 105 (word:road) |
| gl-a1196 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a1202 | 17-collection-register.md | | Roast Kitchen | 10 | 8 | 8 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 102 | | nombre 10 (word:kitchen), nombre 8 (word:kitchen), nombre 9 (word:kitchen), nombre 102 (word:kitchen) |
| gl-a2214 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2223 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a1237 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a1261 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2278 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |

_… et 13 autres assertions._

### brain_banc_v4

## Assertions tenues par le témoin (mode valeur)

| assertion | pièce | citation (80 car.) | discriminant |
| --- | --- | --- | --- |
| gl-a1633 | 02-signed-service-agreement.md | The service starts on 2023-05-24. | date 24/05/2023 |
| gl-a1639 | 02-signed-service-agreement.md | The customer remains responsible for the contents of each container until collec… | repli lexical (recouvrance substantielle) |
| gl-a1651 | 02-signed-service-agreement.md | Late balances carry simple interest at **4.6 percent per year** from the day aft… | nombre 4.6 (percent) |
| gl-a1703 | 05-contract-notice-diary.md | Oat Lantern Bakery Ltd | 2024-07-17 | Annual / six weeks | Summary only | date 17/07/2024 |
| gl-a1704 | 05-contract-notice-diary.md | Silver Apron Dining Ltd | 2024-10-14 | Annual / written notice; length unrecorde… | date 14/10/2024 |
| gl-a1715 | 06-expansion-offer-card.md | | Mill Road | 26 Kettle Street | 2 | 1.931 | cargo cycle | | nombre 26 (word:road), nombre 2 (word:street) |
| gl-a1719 | 06-expansion-offer-card.md | | West Yard | 68 Fern Reach | 1 | 2.183 | electric van | | nombre 68 (word:yard), nombre 1 (word:reach), nombre 2183 (word:reach) |
| gl-a1716 | 06-expansion-offer-card.md | | Roast Kitchen | 31 Copperleaf Way | 2 | 8.417 | electric van | | nombre 31 (word:kitchen), nombre 2 (word:way), nombre 8417 (word:way) |
| gl-a1699 | 03-receivables-summary.md | No bank statement accompanies this note. | repli lexical (recouvrance substantielle) |
| gl-a1904 | 10-billing-index.md | | INV-2025-061 | 2025-01-11 | Oat Lantern Bakery Ltd | 771.02 | 123.36 | 894.38 … | nombre 61 (word:inv), nombre 771.02 (word:ltd), nombre 123.36 (word:ltd), nombre 894.38 (word:ltd), nombre 9 (word:arch), date 11/01/2025, texte «INV», texte «ARCH», texte «Q9M» |
| gl-a1948 | 11-invoice-mw-c-jan-h8k.md | **Payment terms: 30 days after issue.** Printed due date: 2025-03-14. | nombre 30 (days), date 14/03/2025 |
| gl-a1969 | 12-invoice-mw-c-nov-l6v.md | **Payment terms: 30 days after issue.** Printed due date: 2025-01-11. | nombre 30 (days), date 11/01/2025 |
| gl-a1989 | 15-invoice-mw-c-dec-r7p.md | **Payment terms: 30 days after issue.** Printed due date: 2025-02-15. | nombre 30 (days), date 15/02/2025 |
| gl-a2010 | 14-invoice-gl-c-feb-n9d.md | **Payment terms: Due on receipt.** Printed due date: 2025-03-18. | date 18/03/2025 |
| gl-a1886 | 09-january-scale-export.md | | Paper Hall | 6 | 6 | 0 | 48 L | 0 | | nombre 6 (word:hall), nombre 0 (word:hall), nombre 48 (word:hall) |
| gl-a1757 | 09-january-scale-export.md | Sheet cells contain the day's summed readings, so two ticket records may share a… | repli lexical (recouvrance substantielle) |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2034 | 20-internal-service-review.md | Prior-year collections | site and month | Invoice transcription | Underlying inv… | repli lexical (recouvrance substantielle) |
| gl-a1723 | 06-expansion-offer-card.md | Existing active locations | 7821.43 | 3417.29 | 2789.63 | 14028.35 | nombre 7821.43 (word:locations), nombre 3417.29 (word:locations), nombre 2789.63 (word:locations), nombre 14028.4 (word:locations) |
| gl-a2032 | 19-transfer-scenario.md | For **2025-06**, the retained preparation model contains **52 planned visits**, … | nombre 6, nombre 52 (word:contains), nombre 1399 (word:gbp), texte «GBP» |
| gl-a2036 | 20-internal-service-review.md | Travel | route and month | Desk model | No vehicle meter log | repli lexical (recouvrance substantielle) |
| gl-a2055 | 20-internal-service-review.md | There are 77 not_weighed visits in 45 complete Circuit A runs, among 285 visits. | nombre 77 (word:there), nombre 45 (word:visits), nombre 285 (word:among) |
| gl-a2056 | 20-internal-service-review.md | | 2025-01 | 20 | 1016.419 | 866.464 | 1882.883 | 1016.419 | | nombre 1, nombre 20, nombre 1016.42, nombre 866464, nombre 1882.88 |
| gl-a2057 | 20-internal-service-review.md | | 2025-02 | 20 | 766.768 | 866.464 | 1633.232 | 766.768 | | nombre 2, nombre 20, nombre 766768, nombre 866464, nombre 1633.23 |
| gl-a2058 | 20-internal-service-review.md | | 2025-03 | 0 | 1601.373 | 0.000 | 1601.373 | 1601.373 | | nombre 3, nombre 0, nombre 1601.37 |
| gl-a2019 | 16-invoice-gl-c-sep-u6w.md | **Payment terms: Due on receipt.** Printed due date: 2025-10-08. | date 08/10/2025 |
| gl-a1167 | 17-collection-register.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2043 | 20-internal-service-review.md | | 2024-04 | 54 | | nombre 4, nombre 54 |
| gl-a2073 | 24-customer-review.md | **Total recovered mass** | **20.405 t** | nombre 20405 (word:mass) |
| gl-a1756 | 08-certification-preparation.md | Its detailed total is 20.405 t; the customer summary and corrected certificate c… | nombre 20405 (word:total), nombre 20415 (word:carry) |
| gl-a2356 | 24-customer-review.md | The client review records **683 collections across 11 collected sites** for the … | nombre 683 (word:records), nombre 11 (word:across) |
| gl-a2362 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2199 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a2363 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2225 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2366 | 17-collection-register.md | | Beacon Court | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 52 | | nombre 4 (word:court), nombre 5 (word:court), nombre 52 (word:court) |
| gl-a2367 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a2369 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |
| gl-a2290 | 24-customer-review.md | | Hearth office | 5 | 4 | 4 | 6 | 3 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 54 | | nombre 5 (word:office), nombre 4 (word:office), nombre 6 (word:office), nombre 3 (word:office), nombre 54 (word:office) |
| gl-a1177 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a2187 | 24-customer-review.md | | Station House | 12 | 10 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 | 12 | 14… | nombre 12 (word:house), nombre 10 (word:house), nombre 13 (word:house), nombre 147 (word:house) |
| gl-a1184 | 17-collection-register.md | | Station House | 11 | 10 | 12 | 12 | 12 | 12 | 13 | 12 | 13 | 12 | 13 | 12 | 14… | nombre 11 (word:house), nombre 10 (word:house), nombre 12 (word:house), nombre 13 (word:house), nombre 144 (word:house) |
| gl-a1192 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a2203 | 24-customer-review.md | | Mill Road | 10 | 9 | 8 | 10 | 8 | 10 | 8 | 9 | 8 | 8 | 8 | 9 | 105 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 105 (word:road) |
| gl-a1196 | 17-collection-register.md | | Mill Road | 10 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 102 | | nombre 10 (word:road), nombre 9 (word:road), nombre 8 (word:road), nombre 102 (word:road) |
| gl-a1202 | 17-collection-register.md | | Roast Kitchen | 10 | 8 | 8 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 9 | 8 | 102 | | nombre 10 (word:kitchen), nombre 8 (word:kitchen), nombre 9 (word:kitchen), nombre 102 (word:kitchen) |
| gl-a2214 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a2223 | 24-customer-review.md | | Roast Kitchen | 10 | 9 | 8 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 10 | 8 | 105 | | nombre 10 (word:kitchen), nombre 9 (word:kitchen), nombre 8 (word:kitchen), nombre 105 (word:kitchen) |
| gl-a1237 | 17-collection-register.md | | West Yard | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 52 | | nombre 4 (word:yard), nombre 5 (word:yard), nombre 52 (word:yard) |
| gl-a1261 | 17-collection-register.md | | Hearth office | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 51 | | nombre 4 (word:office), nombre 5 (word:office), nombre 51 (word:office) |

_… et 14 autres assertions._

## Grille témoin (budget × fournisseur)

k ou variante : même règle que la grille « à unités et budget égaux ». Métrique : **tout tient**, mode verbatim (colonne témoin) et valeur (colonne témoin valeur).

| Budget | Fournisseur | k / variante | témoin (verbatim) | témoin (valeur) | écart (verbatim) |
| --- | --- | --- | --- | --- | --- |
| 8000 | brain_banc | figé | 23/141 | 24/141 | 56 |
| 8000 | Brain banc (g24, réglé sur le budget) | figé | 15/141 | 15/141 | 24 |
| 8000 | Brain banc (g36, réglé sur le budget) | figé | 12/141 | 12/141 | 22 |
| 8000 | Brain banc (g48, réglé sur le budget) | figé | 15/141 | 15/141 | 23 |
| 8000 | porte 3 voisinage, 1 arête (atomes) | figé | 23/141 | 24/141 | 56 |
| 8000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 23/141 | 24/141 | 56 |
| 8000 | porte 3 voisinage, 1 arête (phrases) | figé | 23/141 | 24/141 | 56 |
| 8000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 23/141 | 24/141 | 56 |
| 8000 | brain_prod (variante k=20) | 20 | 12/141 | 13/141 | 32 |
| 8000 | mem0 | 40 | 0/141 | 11/141 | 2 |
| 8000 | rag_naif | 12 | 27/141 | 29/141 | 37 |
| 12000 | brain_banc | figé | 23/141 | 24/141 | 61 |
| 12000 | Brain banc (g24, réglé sur le budget) | figé | 25/141 | 25/141 | 42 |
| 12000 | Brain banc (g36, réglé sur le budget) | figé | 17/141 | 17/141 | 26 |
| 12000 | Brain banc (g48, réglé sur le budget) | figé | 17/141 | 17/141 | 22 |
| 12000 | porte 3 voisinage, 1 arête (atomes) | figé | 23/141 | 24/141 | 61 |
| 12000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 23/141 | 24/141 | 61 |
| 12000 | porte 3 voisinage, 1 arête (phrases) | figé | 28/141 | 28/141 | 59 |
| 12000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 29/141 | 29/141 | 58 |
| 12000 | brain_prod (variante k=20) | 20 | 12/141 | 13/141 | 32 |
| 12000 | mem0 | 40 | 0/141 | 11/141 | 2 |
| 12000 | rag_naif | 12 | 46/141 | 48/141 | 39 |
| 16000 | brain_banc | figé | 23/141 | 24/141 | 61 |
| 16000 | Brain banc (g24, réglé sur le budget) | figé | 31/141 | 32/141 | 52 |
| 16000 | Brain banc (g36, réglé sur le budget) | figé | 25/141 | 25/141 | 34 |
| 16000 | Brain banc (g48, réglé sur le budget) | figé | 20/141 | 20/141 | 32 |
| 16000 | porte 3 voisinage, 1 arête (atomes) | figé | 23/141 | 24/141 | 61 |
| 16000 | porte 3 voisinage, 2 arêtes (atomes) | figé | 23/141 | 24/141 | 61 |
| 16000 | porte 3 voisinage, 1 arête (phrases) | figé | 28/141 | 28/141 | 59 |
| 16000 | porte 3 voisinage, 2 arêtes (phrases) | figé | 29/141 | 29/141 | 58 |
| 16000 | brain_prod (variante k=20) | 20 | 12/141 | 13/141 | 32 |
| 16000 | mem0 | 40 | 0/141 | 11/141 | 2 |
| 16000 | rag_naif | 12 | 54/141 | 56/141 | 42 |
