import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Prédiction", page_icon="🔮", layout="wide")

# ── Chargement modèle ─────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../model/best_model.joblib")

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None

model = load_model()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("🔮 Prédiction du risque de défaut")
st.markdown(
    "Renseignez le profil financier du client. "
    "Le modèle estime sa **probabilité de défaut (PD)** et sa classe de risque."
)

if model is None:
    st.warning(
        "⚠️ Modèle non disponible — en attente de `model/best_model.joblib` "
        "(Camille — NB3). Le formulaire est fonctionnel, "
        "la prédiction sera activée dès réception du modèle."
    )

st.divider()

# ── FORMULAIRE ────────────────────────────────────────────────────────────────
with st.form("prediction_form"):
    st.subheader("📋 Profil financier du client")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📊 Situation de crédit**")

        credit_lines = st.selectbox(
            "Lignes de crédit en cours (credit_lines_outstanding)",
            options=[0, 1, 2, 3, 4, 5],
            index=1,
            help="Variable la plus prédictive — corrélation +0.86 avec le défaut"
        )

        loan_amt = st.number_input(
            "Montant du prêt en cours — € (loan_amt_outstanding)",
            min_value=0.0,
            max_value=500_000.0,
            value=10_000.0,
            step=500.0,
            help="Montant total du prêt encore dû"
        )

        total_debt = st.number_input(
            "Dette totale en cours — € (total_debt_outstanding)",
            min_value=0.0,
            max_value=1_000_000.0,
            value=15_000.0,
            step=500.0,
            help="Corrélation +0.76 avec le défaut — second prédicteur clé"
        )

    with col2:
        st.markdown("**👤 Profil personnel & financier**")

        fico_score = st.slider(
            "Score FICO (fico_score)",
            min_value=300,
            max_value=850,
            value=650,
            step=1,
            help="Plus le score est élevé, moins le risque de défaut est fort (corrélation -0.32)"
        )

        income = st.number_input(
            "Revenu annuel — € (income)",
            min_value=0.0,
            max_value=500_000.0,
            value=50_000.0,
            step=1_000.0,
            help="Revenu brut annuel du client"
        )

        years_employed = st.selectbox(
            "Années d'ancienneté professionnelle (years_employed)",
            options=list(range(0, 41)),
            index=5,
            help="Stabilité professionnelle — variable discrète (0 à 40 ans)"
        )

    st.divider()

    if income > 0:
        dti = (total_debt / income) * 100
        st.markdown(
            f"📐 **Ratio dette/revenu calculé : {dti:.1f}%** "
            f"{'🔴 Élevé (> 40%)' if dti > 40 else '🟢 Acceptable (≤ 40%)'}"
        )

    submitted = st.form_submit_button(
        "🔍 Analyser le risque de défaut",
        use_container_width=True
    )

# ── RÉSULTAT ──────────────────────────────────────────────────────────────────
if submitted:
    input_data = pd.DataFrame([{
        "credit_lines_outstanding" : credit_lines,
        "loan_amt_outstanding"     : loan_amt,
        "total_debt_outstanding"   : total_debt,
        "income"                   : income,
        "years_employed"           : years_employed,
        "fico_score"               : fico_score,
        "ratio_dette_revenu"       : total_debt / income if income > 0 else 0,
        "ratio_dette_pret"         : total_debt / loan_amt if loan_amt > 0 else 0,
    }])

    st.divider()
    st.subheader("📊 Résultat de l'analyse")

    if model is not None:
        proba      = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            if prediction == 1:
                st.error("🚨 DÉFAUT PROBABLE")
            else:
                st.success("✅ PAS DE DÉFAUT PRÉVU")
            st.metric("Probabilité de défaut (PD)", f"{proba*100:.1f}%")

        with col2:
            if proba < 0.30:
                niveau  = "🟢 Faible"
                conseil = "Octroi recommandé aux conditions standard."
            elif proba < 0.60:
                niveau  = "🟡 Modéré"
                conseil = "Analyse approfondie requise. Envisager des garanties."
            else:
                niveau  = "🔴 Élevé"
                conseil = "Refus recommandé. Passage en comité de crédit."

            st.markdown(f"**Classe de risque : {niveau}**")
            st.progress(float(proba))
            st.caption(conseil)

        with col3:
            st.markdown("**📐 Indicateurs calculés**")
            if income > 0:
                dti = (total_debt / income) * 100
                st.metric("Ratio dette / revenu", f"{dti:.1f}%")
            st.metric("Score FICO saisi", fico_score)
            st.metric("Lignes de crédit", credit_lines)

        with st.expander("📋 Données transmises au modèle"):
            st.dataframe(
                input_data.T.rename(columns={0: "Valeur saisie"}),
                width='stretch'
            )
    else:
        st.info("Modèle non chargé — voici le vecteur qui serait transmis au modèle :")
        st.dataframe(
            input_data.T.rename(columns={0: "Valeur saisie"}),
            width='stretch'
        )