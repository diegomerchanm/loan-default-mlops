# Loan Default MLOps

End-to-end MLOps pipeline for retail banking credit risk modeling.

## Stack
Python · scikit-learn · MLflow · Streamlit · Docker · GitHub Actions · Render

## Project Structure
loan-default-mlops/
├── data/               ← Dataset local (gitignored)
├── model/              ← Model artifacts
├── notebooks/          ← EDA & training
├── app/                ← Streamlit app
└── .github/workflows/  ← CI/CD

## Setup local
pip install -r requirements.txt

## Team branches
| Branch | Responsable | Scope |
|---|---|---|
| feat/data-prep | [nombre] | EDA, preprocessing, training |
| feat/mlflow | [nombre] | Experiment tracking, registry |
| feat/app | [nombre] | Streamlit UI |
| feat/cicd | [nombre] | Docker, GitHub Actions, Render |

## Déploiement

### Prérequis
- Compte [Render](https://render.com) connecté au repo GitHub
- Secret `RENDER_DEPLOY_HOOK` configuré dans GitHub Actions

### Lancer l'app en local avec Docker
```bash
docker build -t loan-default-mlops .
docker run -p 8501:8501 loan-default-mlops
```
Accéder à l'app : http://localhost:8501

### CI/CD
Chaque push sur `main` déclenche automatiquement :
1. Installation des dépendances
2. Déploiement sur Render via Deploy Hook