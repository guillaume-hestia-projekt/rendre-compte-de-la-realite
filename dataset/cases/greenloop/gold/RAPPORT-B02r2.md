# RAPPORT B02r2 — reprise 1 de l'or GreenLoop

Annotateur: grok · 2026-09-08 · `annotation.blind`: true  
Fichiers: `gold/situations.json` (`gold-situations/1.1.0`), `gold/escalations.json` (`gold-escalations/1.0.0`).  
Lecture limitée à `dossiers/greenloop/{README.md,manifest.json,documents/,gold/}` et au protocole (§2 bis, `PROMISE.md`).

## Point → objets → preuve

**B1** Sortie de `gl-tr0001`–`gl-tr0003`. Canon `gl-s0472`–`gl-s0474` et termes imprimés (`gl-s0520`, `gl-s0524`…) sans succession. 02 p.2 : « A shorter term printed on a later invoice changes this agreement only if both parties sign an amendment. »

**B2** `validity_start 2023-05-24` retiré de `gl-s0462`…`gl-s0487` ; `source_date 2023-05-15` p.1 conservé. Le début de service reste seul sur `gl-s0460` p.1 : « The service starts on 2023-05-24. »

**B3** Neuf totaux du registre (`gl-a2362`…`gl-a2370` sur `gl-s0332`) et neuf disputes `gl-d0041`–`gl-d0049` contre `gl-a2199`…`gl-a2303`. 17 : `| Station House | 11 | … | 144 |` vs 24 p.9 : `| Station House | 12 | … | 147 |`.

**B4** Entité `site-mill-road-unassigned` ; `gl-s0455`/`gl-s0457` y participent, séparées de `gl-s0359`/`gl-s0365`. `gl-u0003` : « The dossier does not identify them as SITE-MR. »

**M1–M3** `gl-d0002`, `gl-d0037`, `gl-d0039` retirées (tensions). Assertions inchangées (`gl-a2013`/`gl-a2014` ; `gl-a1738`/`gl-a2070` ; `gl-a1929`/`gl-a2329`).

**M4** `gl-d0038` → `gl-tr0011`. 08 : « Its earlier estimate remains 1.287 t. » (`gl-a1744`, début 2025-05-22) puis `| 2025-03 | 1601.373 | 0.000 | 1601.373 |` (`gl-a1751`, 2025-06-18).

**M5** `gl-d0034` = collectes 657/657/683 ; `gl-d0040` = sites 9/11/11. 17 : « **2024: 657 collections across 9 collected sites.** »

**M6** `gl-tr0007` → `gl-u0016`. 10 : « Export timestamp: not recorded ». **M7** `gl-tr0010` supprimée ; `gl-a1723`/`gl-a1724` restent deux options du 2025-08-21.

**M8** `gl-s0542` : « Invoice INV-2025-062 issued 2025-01-16 to Juniper Table Services Ltd ».

**M9–M10** 34 masses des factures 11/14 en `stated_without_status`. Composites à `estimated_kg` non nul : `mixed` (`gl-a1747`/`gl-a1749`/`gl-a1753` harmonisés avec `gl-a2056`/`gl-a2057`/`gl-a2059` et 24 p.10).

**M11** Cinq clauses 02 : couvercles p.1 ; « The parties may review routes and charges at each anniversary… » p.2 (`gl-s0475`) ; exception public / divulgation p.3 ; feuilles de fréquence p.4.

**M12–M21** Dépôt `gl-s0160` = `occurrence` (25 : « Deposit date: 2025-03-11 »). Reconduction `gl-s0494` = `validity_start 2026-05-24`. `source_date` de `gl-s0552` ancré p.1. `notification` `gl-s0495` 2025-08-27 (05). `validity_end` Fenroot `2024-06` (24 p.6). `polarity: "deny"` sur 25 négations (02 : « This agreement sets **no fixed recovery fee**. » ; 17 : « No customer termination notice is attached »). Dix entités orphelines participantes. `must_stay_separate_from` entre `gl-s0082` et `gl-s0556` (14 p.2 « Hearth | 4 » vs 1 visite). Six notes 24 p.11–16 : « Empty raw mass fields remain blank. » Taxe/banque `TEST-TAX-JTS-W7C` / `TEST-BANK-GL-P7H`.

**S13–S14** Escalades dans `gold/escalations.json` avec `refers_to`. Primaire : `gl-d0001`, `gl-d0035`/`gl-d0036`, `gl-u0011` ; `gl-e0006`/`gl-e0005`/`gl-e0007` en renvoi. `gl-e0004` primaire (canon/run, pas dispute).

**S15** 29 manques textuels des six pièces + 9 totaux du registre ; phrases réelles attenantes (méthode p.7, identification facture 11, bon 25).

## Comptes

| Objet | B02 | B02r2 |
| --- | ---: | ---: |
| Situations | 555 | 556 |
| Assertions | 2353 | 2403 |
| Disputes | 39 | 45 |
| Trajectoires | 10 | 6 |
| Inconnues | 15 | 16 |
| Escalades | 11 (dans situations.json) | 11 (`escalations.json`) |

## Ce que je n'ai PAS vérifié

- L'arithmétique interne (visites × tarif, 16 %, moyennes de site, 184.4317 Nm³/t).
- Le recompte 285 × 4 cellules CSV contre registre, index et revue.
- La couverture des 22 pièces hors des six de la revue.
- `questions.json` et `tensions.json` (absents du dossier).
- Les en-têtes de colonnes, le TOC p.2 et les renvois de pagination (faux positifs de la revue).

{"verdict":"OK","points_appliques":15,"situations":556,"assertions":2403,"disputes":45,"trajectoires":6,"escalades":11,"manques_combles":47,"heures":2.5}
