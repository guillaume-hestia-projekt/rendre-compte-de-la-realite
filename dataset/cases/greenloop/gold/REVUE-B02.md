# REVUE B02 — contre-lecture adverse et aveugle de l'or GreenLoop

Contre-lecteur : Claude Opus 5 · 2026-09-08 · lecture limitée à `dossiers/greenloop/{README.md,manifest.json,documents/,gold/}` et au protocole (`protocol/README.md`, `PROMISE.md`).
Aucun scratchpad de fabrication, aucun autre or, aucun dépôt hors worktree, aucune API de modèle. Verbatim des 2 353 citations et validité JSON : **non repassés** (établi par le directeur).

## Verdict : **FAIL** — 4 bloquants, 11 majeurs, 10 mineurs

L'or est solide sur ce que le protocole appelle « ne rien inventer » : **0 nombre recalculé** (contrôle mécanique : chaque nombre de chaque `content` est présent dans son document source), **0 mot de jugement** absent de la pièce, granularités jamais faussées (0 jour fabriqué à partir d'un mois), 285 passages 2025 tous présents, `unknowns` et `reversibility_cases` remarquables. Il échoue sur la **frontière canon/run**, sur **l'ancrage temporel des règles du contrat**, et sur **la complétude du jeu de disputes**.

---

## 1. Bloquants

**B1 — Le conflit contrat/facture est rangé en trajectoire : résolution silencieuse.**
`gl-tr0001` (terme de paiement), `gl-tr0002` (intérêt 4,6 % → 8,7 %), `gl-tr0003` (pas de frais → GBP 58.71) présentent la facture comme la *version suivante* de la règle contractuelle. Or le contrat écrit l'inverse : 02 p.2 « *A shorter term printed on a later invoice changes this agreement only if both parties sign an amendment.* » et « *An internal rate sheet or a changed invoice template does not itself amend this agreement.* » Déclarer une succession, c'est trancher — exactement ce que `PROMISE` §5 interdit (« Silent resolutions : 0 »). L'or se contredit lui-même : `gl-e0004` décrit ce même couple comme une escalade « a human must decide ». *Correction* : sortir tr0001–tr0003 des trajectoires ; garder la règle contractuelle (canon) et le terme imprimé (run) comme deux situations sans lien, et laisser la passe d'inférence produire la tension.

**B2 — 24 règles du contrat portent un `validity_start` inféré et mal ancré.**
Les situations `gl-s0462`…`gl-s0487` portent toutes `validity_start = 2023-05-24`, `source = documents/02-…md p. 2|3|4`. Contrôle mécanique : **la valeur 2023-05-24 n'existe sur aucune de ces pages** (12× p.2, 9× p.3, 3× p.4) ; elle n'est écrite qu'en p.1 (« *The service starts on 2023-05-24.* »). Deux fautes cumulées : (a) provenance fausse (mesure « Provenance completeness = 1.00 » cassée) ; (b) valeur inférée — le contrat est exécuté le 2023-05-15 et ne dit nulle part que la confidentialité, la cession ou le règlement des différends prennent effet à la mise en service. *Correction* : `source_date 2023-05-15` (déjà présent) ; supprimer le `validity_start` ou l'ancrer en p.1 avec la mention que la date citée est celle du début de service, pas celle de la clause.

**B3 — Neuf disputes manquantes, faute d'avoir annoté la colonne « Total » du registre.**
17 p.1 publie un total annuel par site (Station House 144, Mill Road 102, Roast Kitchen 102, Quarry Tower 52, Beacon Court 52, West Yard 52, Paper Hall 51, Hearth office 51, Hearth counter 51). 24 p.9 publie les mêmes neuf totaux avec d'autres valeurs (147, 105, 105, 55, 55, 55, 54, 54, 53). L'or porte les neuf de la revue (`gl-a2199`…`gl-a2303`) et **aucun** du registre : 9 assertions absentes, donc 9 disputes absentes, toutes de même forme que les 31 disputes mensuelles retenues. Un système qui les sert serait compté en faux positifs.

**B4 — Fusion d'identité abusive sur le libellé « Mill Rd. » non assigné.**
`gl-s0455` et `gl-s0457` (lignes CSV 110 et 112, `site_code` vide, basis « *margin label; count not transcribed* ») portent le participant `('label','site-mill-road')`. L'or déclare pourtant lui-même en `gl-u0003` : « *The dossier does not identify them as SITE-MR.* » Le cas jumeau « Hearth » a bien reçu une entité séparée (`site-hearth-unassigned`) ; « Mill Rd. » non. *Correction* : créer `site-mill-road-unassigned`, ou renvoyer le participant à `null` avec l'inconnue.

## 2. Majeurs

| # | Objet | Pièce / preuve | Correction |
|---|---|---|---|
| M1 | `gl-d0002` : deux masses d'une **même** facture rangées en dispute | 13 p.1 « *— 1.091 tonnes* » vs « *1.137 \| 177.29 \| 201.58* » | tension « libellé contre montant » ; l'or la porte déjà en `gl-u0011` et `gl-e0007` : triple classement |
| M2 | `gl-d0037` : estimation vs actuel publié | 08 « *0.673 \| Estimated from nearby months* » vs 24 p.3 « *December's 0.719 t … actual material recovered* » | tension estimation/mesure |
| M3 | `gl-d0039` : émetteur de facture vs attribution de facturation | 11 p.1 « *Issued 2025-02-12* … Mosswheel » vs 24 p.10 « *Billing attribution: **GreenLoop Collect Ltd**.* » | portées et instants différents ; règle d'identité ⇒ tension (ou trajectoire, cf. `gl-tr0005`) |
| M4 | `gl-d0038` rangé en dispute alors que la pièce narre la succession | 08 p.1 « *Its earlier estimate remains 1.287 t.* » | trajectoire ; en outre 1.287 t vs 1601.373 kg exige une conversion : pas « lisible sans calcul » |
| M5 | `gl-d0034` fond **deux** questions | 657/683 collectes **et** 9/11 sites | scinder en deux disputes |
| M6 | `gl-tr0007` invente un ordre | 04 daté 2025-05-19 vs 10 « *Export timestamp: not recorded* » | non ordonnable ⇒ inconnue/tension, pas trajectoire |
| M7 | `gl-tr0010` : deux **options** de la même carte présentées en versions successives | 06 p.1, même date 2025-08-21 | alternatives ; le doc 19 écrit lui-même la comparaison |
| M8 | Libellé de situation inférentiel | `gl-s0542` « Invoice INV-2025-062 (**not present in billing-index extract**) » — aucune pièce ne l'écrit | libellé neutre ; le constat vit déjà en `gl-u0005` |
| M9 | Quantités de facture servies sans statut | 11 p.1 « *collected quantity 282.420 kg* » (Mill Rd. = 31.380 pesés + 251.040 estimés) : les 18 lignes de masse des factures 11/12/14/15 sont `not_applicable` | `not_applicable` sert à la fois pour « pas de quantité » et « quantité sans méthode déclarée » ; il faut un statut distinct |
| M10 | Statut incohérent entre deux pièces portant la **même** ligne | `gl-a1747`/`gl-a1749` = `weighed` alors qu'elles contiennent `estimated_kg 866.464` ; `gl-a2056`/`gl-a2057` (doc 20, ligne identique) = `not_applicable` | harmoniser ; une assertion composite qui porte un estimé ne peut être `weighed` |
| M11 | Cinq clauses du contrat absentes de l'or | 02 p.1 « *The customer keeps lids closed…* » ; p.2 « *The parties may review routes and charges at each anniversary…* » ; p.3 « *It does not cover information already public…* » ; p.3 « *Required disclosure must be limited…* » ; p.4 « *Additional operational frequency sheets…* » | la clause de révision annuelle est portante : c'est elle qui encadre la décision du 2025-09-08 |

## 3. Mineurs

M12 `gl-s0160` : rôle `effect` pour la date de dépôt (25 « *Deposit date: 2025-03-11* ») — c'est une seconde **occurrence**. · M13 `gl-s0494` : `effect 2026-05-24` pour une date de reconduction (plutôt `deadline`/`validity_start`). · M14 `gl-s0552` : `source_date 2025-06-19` cité p.7 ; la date est en p.1. · M15 Rôles `notification` et `validity_end` jamais employés (0/786) alors que 05 et 24 p.6 les portent. · M16 `polarity` = `affirm` sur 2 353/2 353 alors que le dossier écrit des négations explicites (« *no fixed recovery fee* », « *No customer termination notice is attached* »). · M17 Dix entités jamais participantes : `org-birch-spoon`, `org-amber-crumb`, `org-pebble-pantry` (pourtant présentes dans 05 et 27), `service-treatment`, `service-setup`, `doc-wt-sh-mar`, `doc-wt-qt-may`, `doc-billing-index`, `site-cinder-lane`, `org-provider-on-invoice`. · M18 `gl-s0082` réunit la ligne de facture « Hearth » (4 visites, 14 p.2) et le processus du libellé non assigné (1 visite) sans `must_stay_separate_from` ni inconnue. · M19 Notes de méthode répétées de 24 p.11–16 (« *Empty raw mass fields remain blank.* ») jamais annotées (6×). · M20 Lignes d'identification des factures non annotées : compte fiscal `TEST-TAX-JTS-W7C`, référence de règlement, coordonnées bancaires (alors que `gl-u0012` discute ce compte). · M21 Le RAPPORT annonce `gold/_build_b02.py` et `gold/_build_b02_part2.py` comme scripts reproductibles : **absents** du dossier (`gold/` ne contient que `RAPPORT-B02.md` et `situations.json`).

---

## 4. Les 39 disputes, une par ligne

Légende : **L** dispute légitime · **T** trajectoire mal rangée · **X** tension d'inférence (n'a rien à faire dans la reconstitution).

| Dispute | Verdict | Preuve (citation) |
|---|---|---|
| d0001 conteneurs WT-GL-SH-MAR-Q7N 2025-03-11 | **L** | 25 « Containers physically removed \| **2** » vs 18 « **containers physically removed on that visit: 3** » — même ticket, même jour, 4 voix |
| d0002 masse facturée INV-2025-070 | **X** | 13 p.1 « — 1.091 tonnes » vs « 1.137 \| 177.29 \| 201.58 » : une seule voix, un seul document ; règle libellé/montant. `PROMISE` §5 dit « two documents » |
| d0003 Station House 2024-01 | **L** | 17 « \| Station House \| 11 \| … » vs 24 p.9 « \| Station House \| 12 \| … » |
| d0004 Station House 2024-08 | **L** | 17 « … \| 12 \| 13 \| … » vs 24 p.9 « … \| 13 \| 13 \| … » |
| d0005 Station House 2024-10 | **L** | 17 « … \| 12 \| 13 \| 12 \| 144 » vs 24 p.9 « … \| 13 \| 13 \| 12 \| 147 » |
| d0006 Mill Road 2024-04 | **L** | 17 « \| Mill Road \| 10 \| 9 \| 8 \| 9 \| … » vs 24 p.9 « … \| 8 \| 10 \| … » |
| d0007 Mill Road 2024-06 | **L** | idem, 6ᵉ colonne 9 vs 10 |
| d0008 Mill Road 2024-08 | **L** | idem, 8ᵉ colonne 8 vs 9 |
| d0009 Roast Kitchen 2024-02 | **L** | 17 « \| Roast Kitchen \| 10 \| 8 \| … » vs 24 p.9 « … \| 9 \| … » |
| d0010 Roast Kitchen 2024-04 | **L** | idem, 4ᵉ colonne 8 vs 9 |
| d0011 Roast Kitchen 2024-11 | **L** | idem, 11ᵉ colonne 9 vs 10 |
| d0012 Quarry Tower 2024-07 | **L** | 17 « \| Quarry Tower \| … \| 4 \| … \| 52 » vs 24 p.9 « … \| 5 \| … \| 55 » |
| d0013 Quarry Tower 2024-09 | **L** | idem, 9ᵉ colonne 4 vs 5 |
| d0014 Quarry Tower 2024-11 | **L** | idem, 11ᵉ colonne 4 vs 5 |
| d0015 Beacon Court 2024-03 | **L** | 17 « \| Beacon Court \| 4 \| 4 \| 5 \| … » vs 24 p.9 « … \| 6 \| … » |
| d0016 Beacon Court 2024-05 | **L** | idem, 5ᵉ colonne 5 vs 6 |
| d0017 Beacon Court 2024-07 | **L** | idem, 7ᵉ colonne 5 vs 6 |
| d0018 West Yard 2024-01 | **L** | 17 « \| West Yard \| 4 \| … \| 52 » vs 24 p.9 « \| West Yard \| 5 \| … \| 55 » |
| d0019 West Yard 2024-03 | **L** | idem, 3ᵉ colonne 4 vs 5 |
| d0020 West Yard 2024-10 | **L** | idem, 10ᵉ colonne 5 vs 6 |
| d0021 Paper Hall 2024-06 | **L** | 17 « \| Paper Hall \| … \| 4 \| … \| 51 » vs 24 p.9 « … \| 5 \| … \| 54 » |
| d0022 Paper Hall 2024-08 | **L** | idem, 8ᵉ colonne 4 vs 5 |
| d0023 Paper Hall 2024-10 | **L** | idem, 10ᵉ colonne 4 vs 5 |
| d0024 Hearth office 2024-01 | **L** | 17 « \| Hearth office \| 4 \| … » vs 24 p.9 « \| Hearth office \| 5 \| … » |
| d0025 Hearth office 2024-04 | **L** | idem, 4ᵉ colonne 4 vs 6 |
| d0026 Hearth office 2024-05 | **L** | idem, 5ᵉ colonne 4 vs **3** (la revue est en dessous) |
| d0027 Hearth office 2024-06 | **L** | idem, 6ᵉ colonne 4 vs 5 |
| d0028 Hearth office 2024-07 | **L** | idem, 7ᵉ colonne 4 vs 5 |
| d0029 Hearth office 2024-08 | **L** | idem, 8ᵉ colonne 5 vs 4 |
| d0030 Hearth office 2024-09 | **L** | idem, 9ᵉ colonne 4 vs 5 |
| d0031 Hearth office 2024-10 | **L** | idem, 10ᵉ colonne 5 vs 4 |
| d0032 Hearth counter 2024-02 | **L** | 17 « \| Hearth counter \| 5 \| 4 \| … \| 51 » vs 24 p.9 « … \| 5 \| … \| 53 » |
| d0033 Hearth counter 2024-11 | **L** | idem, 11ᵉ colonne 4 vs 5 |
| d0034 collectes et sites 2024 | **L** (à scinder) | 17 « **2024: 657 collections across 9 collected sites.** » vs 20 « **657 collections on 11 collected sites.** » vs 24 p.9 « **683 collections across 11 collected sites** » — deux questions en une |
| d0035 masse publiée 2024-01→2025-04 | **L** | 23 « **20.415 tonnes** » vs 24 p.4 « **Total recovered mass** \| **20.405 t** » ; 08 l'écrit lui-même |
| d0036 biogaz de la même fenêtre | **L** | 23 « Biogas equivalent \| **3761 Nm³** » vs 24 p.4 « **3763 Nm³** » |
| d0037 masse de 2024-12 | **X** | 08 « Estimated from nearby months » vs 24 p.3 « **0.719 t** … actual material recovered » : estimation contre mesure, statuts différents, pas même portée |
| d0038 masse de 2025-03 dans le log de préparation | **T** | 08 « Its earlier estimate remains 1.287 t. » puis « \| 2025-03 \| 1601.373 \| 0.000 \| 1601.373 \| » : la pièce déclare la succession |
| d0039 facturation de 2025-01 | **X** | 11 p.1 (Mosswheel, une facture) vs 24 p.10 (GreenLoop, fenêtre de quatre mois) : portée et instant différents, règle d'identité |

**Bilan : 35 légitimes · 1 trajectoire mal rangée · 3 tensions d'inférence.** À quoi s'ajoutent, hors table, **5 trajectoires sur 10 mal rangées** (tr0001, tr0002, tr0003 = tensions canon/run ; tr0007 = ordre inventé ; tr0010 = alternatives) : le total des tensions logées dans la reconstitution est donc de **8**.

## 5. Où je place la frontière, et ce que le protocole doit changer

Une **dispute** exige *deux voix* (deux documents, ou deux perspectives) répondant à *la même question*, sur *la même portée*, au *même instant*, et le désaccord doit se lire en comparant deux cellules — sans conversion d'unité, sans règle d'identité, sans hypothèse sur le statut de la quantité. Dès qu'il faut poser « ce libellé désigne la même chose que ce montant », « cette estimation vaut cette mesure », « cet émetteur est cette attribution », ou convertir des tonnes en kilogrammes, on est dans la **tension** : elle appartient à `tensions.json`, jamais à `situations.json`. Une **trajectoire** n'est légitime que si l'instrument postérieur a *le pouvoir* de remplacer l'antérieur selon les termes de l'antérieur ; sinon la succession apparente est une tension canon/run. C'est le point où cet or bascule.

Sept modifications de protocole :
1. **Test d'admissibilité d'une trajectoire** : exiger que la pièce postérieure ait autorité pour amender la précédente, ou qu'une pièce déclare la succession. Sans ce test, tout or choisira la facture contre le contrat.
2. **Une pièce, un classement** : interdire qu'un même couple soit à la fois dispute, inconnue et escalade (d0002/u0011/e0007 ; d0035/e0005 ; d0001/e0006). Un classement primaire, des renvois.
3. **Écrire dans le protocole que la dispute suppose deux documents** — `PROMISE` §5 le dit déjà (« two documents ») ; §2 du protocole ne le reprend pas. Une divergence interne à une pièce est une tension libellé/montant.
4. **Trajectoire bien formée** : versions ordonnées, `validity_start` non nul, `validity_end` renseigné dès que la suivante commence. Une version sans date est une inconnue, pas une version.
5. **Sortir `escalation_opportunities` de `situations.json`** : six des onze escalades (e0001–e0004, e0008, e0009) comparent explicitement deux documents à l'intérieur du fichier de reconstitution, ce que `PROMISE` §6 interdit.
6. **Statut de quantité** : ajouter `stated_without_status` (et/ou `mixed`). Aujourd'hui `not_applicable` recouvre « il n'y a pas de quantité » et « il y a une masse dont la pièce ne dit pas la méthode » — c'est précisément l'endroit où une estimation peut passer pour une mesure.
7. **Mesure nouvelle « exactitude de l'ancrage temporel »** : la valeur d'une entrée temporelle doit figurer littéralement sur la page citée. Ce contrôle, appliqué ici, sort 25 défauts sur 786 que la mesure « Temporal role accuracy » ne voit pas.

## 6. Taux de couverture mesuré

Six pièces lues en entier (02 contrat, 24 revue 16 pages, 17 registre, 11 facture, 25 bon de pesée, 20 note interne). Unité = ligne de tableau ou phrase, en-têtes de colonnes et renvois de pagination exclus ; une unité est couverte si ≥ 60 % de ses mots pleins se retrouvent dans une même assertion de la même pièce.

| Pièce | Unités | Manques | Couverture |
|---|---:|---:|---:|
| 02 accord signé | 74 | 5 | 0,932 |
| 24 revue client | 380 | 27 | 0,929 |
| 17 registre | 308 | 5 | 0,984 |
| 11 facture janvier | 23 | 3 | 0,870 |
| 25 bon de pesée | 14 | 2 | 0,857 |
| 20 revue interne | 28 | 4 | 0,857 |
| **Total** | **827** | **46** | **0,944** |

Après tri manuel des faux positifs (lignes de titre, renvois, coupures de phrase sur deux-points), **29 manques textuels réels**, auxquels s'ajoutent les **9 totaux annuels du registre** (B3) : **38 manques**. Couverture triée ≈ 0,96 ; je retiens la mesure brute 0,944 comme chiffre déclaré.

## 7. Ce que je n'ai PAS vérifié

- Le verbatim des 2 353 citations et la validité du JSON (établis par le directeur, non repassés).
- L'arithmétique interne du dossier (visites × tarif, 16 % de taxe, moyennes de site, 184,4317 Nm³/t) : je l'ai volontairement laissée hors de la reconstitution, c'est de l'inférence.
- Le recompte ligne à ligne des 285 lignes CSV contre le registre, l'index de tickets et la liste de visites de la revue : j'ai vérifié les identifiants et les cas signalés, pas les 285 × 4 cellules.
- Les 22 autres pièces n'ont été lues qu'intégralement pour 01, 03–09, 12–16, 19, 23, 26, 27 et par sondage pour 18, 21, 22, 28 — la mesure de couverture ne porte que sur les six pièces déclarées.
- La cohérence de l'or avec `questions.json` (absent du dossier) et avec un éventuel `tensions.json`.
- Les scripts `_build_b02*.py` : introuvables, donc reproductibilité non testée.
- Aucun dossier interdit n'a été ouvert : ni `/tmp/claude-1000/**`, ni `ambactos-brain-answers`, ni lesgaspard, ni MOREAU/Coutume, ni les sessions d'agents.

{"verdict":"FAIL","bloquants":4,"majeurs":11,"mineurs":10,"disputes_legitimes":35,"disputes_mal_rangees":1,"tensions_dans_la_reconstitution":3,"manques":38,"couverture":0.944}
