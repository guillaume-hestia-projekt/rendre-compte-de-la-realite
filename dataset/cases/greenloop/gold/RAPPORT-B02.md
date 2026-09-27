# RAPPORT B02 — or de reconstitution GreenLoop (annotation aveugle)

Annotateur: grok · Date: 2026-09-08 · `annotation.blind`: true  
Fichier: `gold/situations.json` · schéma `gold-situations/1.1.0`  
Lecture limitée à `benchmark/dossiers/greenloop/{README.md,manifest.json,documents/}`. Aucun scratchpad, aucun autre or, aucun dépôt hors worktree.

## Volumes

| Objet | N |
| --- | ---: |
| Situations | 555 |
| — strate `process` | 168 |
| — strate `event` | 334 |
| — strate `other` | 53 |
| Assertions | 2353 |
| Disputes | 39 |
| Trajectoires | 10 |
| Inconnues | 15 |
| Escalades | 11 |
| Cas de réversibilité | 11 |
| Cadres manquants distincts (`catalogue_gap`) | 29 |

Genres: `event` 334, `process` 168, `rule` 26, `state` 16, `plan` 5, `relation` 3, `definition` 2, `preference` 1.  
Passages 2025: 285 situations d’événement (un ticket = une situation), toutes présentes.  
Sources: 27 du manifeste (gl-17 a deux représentations byte-identiques; le fichier 28 n’est pas une source indépendante).  
`frame`: `unknown` partout. Citations: 2353/2353 sont des sous-chaînes verbatim du fichier source, sur la page déclarée.

## Discernement — trois passages

1. **WT-GL-SH-MAR-Q7N (Station House, 2025-03-11).** Le bon de pesée final, le CSV, le registre et la revue client portent **2** contenants; l’index des tickets (note de transcription **et** ligne de tableau) porte **3**. Même question, même portée, même jour → dispute, sans départager.
2. **Visite étiquetée « Hearth » le 2025-02-05 (WT-20250205-HO-CP).** Pas de `site_code`, pas d’adresse; le préfixe de ticket est `HO`. La revue exige de conserver le libellé non assigné. Entité séparée de Hearth office / Hearth counter, plus une inconnue d’identité.
3. **Masse / biogaz de la fenêtre 2024-01–2025-04.** Le certificat corrigé et le bandeau de la revue publient **20.415 t** et **3761 Nm³**; le tableau consolidé de la même revue publie **20.405 t** et **3763 Nm³**. Totaux de documents, pas faits du monde; les deux voix restent.

Autres tensions enregistrées comme **trajectoires** (pas comme conflits): terme de paiement 30 jours → due on receipt; intérêt 4,6 % → 8,7 %; pas de frais de recouvrement → GBP 58.71; tarif Quarry Tower 14.83 → 24.67 au 2025-09-08; opérateur de réception Fenroot puis Cinderbank; clôture fin 2025-05 puis redémarrage 2025-09-09.

## Ce que je n’ai PAS vérifié

- L’arithmétique interne (visites × tarif = net; 16 % de taxe; moyennes de site × visites non pesées = `estimated_kg`; 184.4317 Nm³/t).
- Le recompte manuel un par un des 285 lignes CSV contre le registre (égalité des identifiants de tickets vérifiée; pas une lecture humaine ligne à ligne).
- Toute pièce hors du dossier (banque, avis client, PDF antérieur du certificat, classeur d’expansion).
- Le scratchpad de fabrication et tout or MOREAU / Coutume / lesgaspard — non ouverts.
- Les clauses du contrat parfois regroupées en une assertion de règle (le texte est cité; chaque phrase n’a pas toujours son propre `gl-a`).

Scripts de génération (reproductibles depuis le dossier seul): `gold/_build_b02.py`, `gold/_build_b02_part2.py`.

{"verdict":"OK","situations":555,"assertions":2353,"disputes":39,"trajectoires":10,"inconnues":15,"escalades":11,"cadres_manquants":29,"heures":3.5}
