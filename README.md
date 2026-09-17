# Dashboard Premier League 2019–2024

## Contenu du dossier
- `cadrage.md` — document de cadrage (message clé, audience, KPIs, structure)
- `app.py` — dashboard Streamlit
- `requirements.txt` — dépendances Python
- `data/` — fichiers de données (se remplit automatiquement au premier lancement, voir ci-dessous)

## Installation

```bash
pip install -r requirements.txt
```

## Lancer le dashboard

```bash
streamlit run app.py
```

Au premier lancement (avec connexion internet), le script **télécharge automatiquement**
les 5 saisons de Premier League depuis football-data.co.uk et les enregistre dans
`data/`. Les lancements suivants relisent directement ces fichiers locaux (grâce à
`@st.cache_data`), donc plus besoin de connexion ensuite.

### Téléchargement manuel (si pas de connexion / pour vérifier les données)
Si tu préfères récupérer les fichiers toi-même, place-les dans `data/` avec ces noms
exacts, puis relance l'app :

| Saison | Lien | Nom de fichier attendu |
|---|---|---|
| 2019/20 | https://www.football-data.co.uk/mmz4281/1920/E0.csv | `data/E0_1920.csv` |
| 2020/21 | https://www.football-data.co.uk/mmz4281/2021/E0.csv | `data/E0_2021.csv` |
| 2021/22 | https://www.football-data.co.uk/mmz4281/2122/E0.csv | `data/E0_2122.csv` |
| 2022/23 | https://www.football-data.co.uk/mmz4281/2223/E0.csv | `data/E0_2223.csv` |
| 2023/24 | https://www.football-data.co.uk/mmz4281/2324/E0.csv | `data/E0_2324.csv` |

⚠️ **Avant de rendre le projet** : lance l'app une fois avec une connexion internet
pour que les 5 CSV soient bien présents dans `data/` (le sujet demande d'inclure
les fichiers de données utilisés dans le rendu).

## Déploiement sur Streamlit Community Cloud
1. Pousse ce dossier (avec `data/` rempli) sur un repo GitHub.
2. Va sur https://share.streamlit.io, connecte le repo.
3. Fichier principal : `app.py`.
4. Récupère le lien `*.streamlit.app` à mettre dans ton rendu.

## Ce que tu dois savoir expliquer à l'oral
- Pourquoi ces 3 KPIs et pas le nombre de buts / de victoires brutes (cf. `cadrage.md`).
- Pourquoi un `line chart` pour l'avantage domicile (tendance dans le temps) et un
  `scatter` pour conversion/discipline (comparaison entre équipes, deux variables).
- Comment les filtres (saisons, équipes, lieu) recalculent KPIs et graphiques sans
  recharger les données brutes (grâce à `st.cache_data` sur le chargement, pas sur
  le filtrage).
