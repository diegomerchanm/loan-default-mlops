# CLAUDE.md — loan-default-mlops

## Projet

Pipeline MLOps end-to-end pour la prédiction de défaut de paiement sur prêts personnels (banque de détail).

## Dataset

- **Fichier** : `Loan_Data.csv` (ne jamais uploader dans le repo)
- **Taille** : 10 000 lignes
- **Features** : `credit_lines_outstanding`, `loan_amt_outstanding`, `total_debt_outstanding`, `income`, `years_employed`, `fico_score`
- **Cible** : `default` (binaire : 0 = pas de défaut, 1 = défaut)

## Stack technique

- **Langage** : Python 3.11
- **ML** : scikit-learn
- **Tracking** : MLflow
- **Interface** : Streamlit
- **Conteneurisation** : Docker
- **CI/CD** : GitHub Actions
- **Déploiement** : Render

## Structure du projet

```
loan-default-mlops/
├── data/               # Données locales uniquement (ignorées par git)
├── model/              # Modèles entraînés et artefacts MLflow
├── notebooks/          # Jupyter notebooks EDA et expérimentation
├── app/                # Application Streamlit
├── .github/workflows/  # Pipelines CI/CD GitHub Actions
├── requirements.txt
├── Dockerfile
└── CLAUDE.md
```

## Modèles entraînés

- Decision Tree
- Logistic Regression
- Random Forest

## Équipe et branches

Équipe de 4 personnes. Branches de travail :

| Branche           | Responsabilité              |
|-------------------|-----------------------------|
| `feat/data-prep`  | Préparation et nettoyage des données |
| `feat/mlflow`     | Tracking et sélection des modèles    |
| `feat/app`        | Application Streamlit                |
| `feat/cicd`       | Pipeline CI/CD et déploiement        |

## Phases du projet

| Phase | Nom                        | Description |
|-------|----------------------------|-------------|
| 0     | Setup                      | Initialisation du repo, environnement, structure |
| 1     | EDA                        | Analyse exploratoire des données |
| 2     | Ingénierie des modèles     | Entraînement, tuning, tracking MLflow |
| 3     | Sélection du modèle        | Comparaison et choix du meilleur modèle |
| 4     | Streamlit                  | Développement de l'interface utilisateur |
| 5     | CI/CD                      | Automatisation tests, build Docker, déploiement Render |
| 6     | Soutenance                 | Présentation finale |

## Conventions de code

- **Variables, fonctions et commentaires** : en français
- **Commits** : Conventional Commits
  - `feat:` nouvelle fonctionnalité
  - `fix:` correction de bug
  - `chore:` tâche technique (dépendances, config)
  - `docs:` documentation

## Règles de sécurité

- Ne **jamais** uploader `Loan_Data.csv` ou tout fichier de données dans le repo
- Ne **jamais** hardcoder des credentials (clés API, mots de passe, tokens)
- Utiliser des variables d'environnement ou un fichier `.env` (listé dans `.gitignore`)
