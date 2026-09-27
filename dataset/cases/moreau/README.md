# Dossier démo - MOREAU c/ ATELIER RIVIÈRE

Pack **prêt pour la démo Filebrain** : 12 pièces d’apparence réaliste, 100 % fictives.

## Contenu

- `SCENARIO.md` - intrigue, chiffres, pièges MoA  
- `GOLDEN-faits.yaml` - 15 faits + contradictions + requêtes  
- `pieces/` - 11 PDF natifs + 1 `.eml`  
- `MANIFEST.sha256` - empreintes  

## Régénérer

```bash
cd ~/filebrain-avocat
python3 scripts/gen_fixtures_prudhommes.py
# ou : just fixtures
```

## Vérifier l’extraction

```bash
pdftotext -layout pieces/07-lettre-licenciement.pdf -
```

## Démo Filebrain (parcours type)

1. Créer le dossier **MOREAU / ATELIER RIVIÈRE**.  
2. Déposer les 12 pièces (PDF d’abord ; e-mail si le canal est branché).  
3. Ingest → extraire_faits (MoA).  
4. Montrer la **file à revue** sur la contradiction des heures sup.  
5. Chronologie : 15/09/2019 → 28/01/2024 → 05/03/2024.  
6. Recherche : « porte est large », « 1 720 », « LUMO ».  

R.G. fictif **24/01984** - Conseil de prud'hommes de Beaumont-les-Rives.
