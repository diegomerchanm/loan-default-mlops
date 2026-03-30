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