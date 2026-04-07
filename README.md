# Loan Default MLOps

Pipeline MLOps end-to-end pour la prédiction de défaut de paiement sur prêts personnels — Banque de détail.

[![CI/CD](https://github.com/diegomerchanm/loan-default-mlops/actions/workflows/deploy.yml/badge.svg)](https://github.com/diegomerchanm/loan-default-mlops/actions/workflows/deploy.yml)

## 🚀 Application en production

👉 [https://loan-default-mlops-tibj.onrender.com](https://loan-default-mlops-tibj.onrender.com)

> ⚠️ L'app tourne sur Render free tier — prévoir 30s de démarrage si inactive.

---

## Stack

Python 3.11 · scikit-learn · MLflow · Streamlit · Docker · GitHub Actions · Render

---

## Structure du projet

```
loan-default-mlops/
├── app/                  ← Application Streamlit (multipage)
│   ├── app.py            ← Page d'accueil
│   ├── pages/
│   │   ├── 01_prediction.py   ← Prédiction de défaut client
│   │   └── 02_dashboard.py    ← Comparaison des modèles
│   └── utils/
│       └── model_loader.py
├── model/                ← Modèles entraînés (.joblib)
├── notebooks/            ← NB1 EDA · NB2 Features · NB3 Modélisation · NB4 MLflow
├── outputs/              ← Graphiques et métriques générés
├── tests/                ← Tests CI (pytest)
├── .github/workflows/    ← Pipeline GitHub Actions
├── Dockerfile
└── requirements.txt
```

---

## Équipe

| Branche | Responsable | Périmètre |
|---|---|---|
| `feat/data-prep` | Xia Bizot | EDA, preprocessing, feature engineering, modélisation |
| `feat/mlflow` | Camille Koenig | Experiment tracking MLflow, model registry |
| `feat/app` | Jayson Nguyen phang | Application Streamlit, intégration du modèle |
| `feat/cicd` | Diego Merchan | Dockerfile, GitHub Actions, déploiement Render |

---

## Prérequis

- Python 3.11 obligatoire
- `Loan_Data.csv` à placer dans `data/` (non versionné)

## Setup local

```bash
git clone https://github.com/diegomerchanm/loan-default-mlops.git
cd loan-default-mlops
py -3.11 -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Lancer l'app en local

```bash
streamlit run app/app.py
```

## Lancer avec Docker

```bash
docker build -t loan-default-mlops .
docker run -p 8501:8501 loan-default-mlops
```

---

## CI/CD

Chaque push sur `main` déclenche automatiquement :

1. **ci_pipeline** — installation des dépendances + tests pytest
2. **cd_pipeline** — déploiement sur Render (si CI passe)

Les tests vérifient : imports, version Python, structure du projet, Dockerfile, et prédiction du modèle.

---

## Modèles

| Modèle | Recall | F1-Score | AUC-ROC |
|---|---|---|---|
| Régression Logistique ✅ | 1.000 | 0.9906 | 1.000 |
| Random Forest | 0.957 | 0.9752 | 0.9997 |
| Decision Tree | 0.968 | 0.9689 | 0.9804 |

Métrique primaire : **Recall** (contexte risque crédit — manquer un défaut coûte plus cher qu'un faux positif).
