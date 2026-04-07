import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Prédiction", page_icon="🔮", layout="wide")

# ── Chargement des modèles ────────────────────────────────────────────────────
BASE_PATH = os.path.join(os.path.dirname(__file__), "../../model")

def load_model(filename):
    try:
        return joblib.load(os.path.join(BASE_PATH, filename))
    except FileNotFoundError:
        return None

MODELES = {
    "Régression Logistique (prod — Recall 1.0)": "model_regression_logistique.joblib",
    "Decision Tree"                             : "model_decision_tree.joblib",
    "Random Forest"                             : "model_random_forest.joblib",
}

models_loaded = {nom: load_model(fichier) for nom, fichier in MODELES.items()}
model_lr   = load_model("model_regression_logistique.joblib")
model_best = load_model("best_model.joblib")
model      = model_lr if model_lr is not None else model_best

# ── SESSION STATE — valeurs par défaut ───────────────────────────────────────
defaults = {
    "credit_lines"    : 1,
    "loan_amt"        : 10_000.0,
    "total_debt"      : 15_000.0,
    "fico_score"      : 650,
    "income"          : 50_000.0,
    "years_employed"  : 5,
    "modele_choisi"   : list(MODELES.keys())[0],
    "show_comparison" : False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("🔮 Prédiction du risque de défaut")
st.markdown(
    "Renseignez le profil financier du client. "
    "Le modèle estime sa **probabilité de défaut (PD)** et sa classe de risque."
)

if model is None:
    st.warning("⚠️ Modèle non disponible.")

st.info(
    "**Modèle de production recommandé : Régression Logistique** — "
    "sélectionné pour son Recall de 1.0 (détecte 100% des défauts réels)."
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
            index=st.session_state["credit_lines"],
            help="Variable la plus prédictive — corrélation +0.86 avec le défaut"
        )

        loan_amt = st.number_input(
            "Montant du prêt en cours — € (loan_amt_outstanding)",
            min_value=0.0, max_value=500_000.0,
            value=st.session_state["loan_amt"], step=500.0,
        )

        total_debt = st.number_input(
            "Dette totale en cours — € (total_debt_outstanding)",
            min_value=0.0, max_value=1_000_000.0,
            value=st.session_state["total_debt"], step=500.0,
        )

    with col2:
        st.markdown("**👤 Profil personnel & financier**")

        fico_score = st.slider(
            "Score FICO (fico_score)",
            min_value=300, max_value=850,
            value=st.session_state["fico_score"], step=1,
        )

        income = st.number_input(
            "Revenu annuel — € (income)",
            min_value=0.0, max_value=500_000.0,
            value=st.session_state["income"], step=1_000.0,
        )

        years_employed = st.selectbox(
            "Années d'ancienneté professionnelle (years_employed)",
            options=list(range(0, 41)),
            index=st.session_state["years_employed"],
        )

    st.divider()

    if income > 0:
        dti = (total_debt / income) * 100
        st.markdown(
            f"📐 **Ratio dette/revenu calculé : {dti:.1f}%** "
            f"{'🔴 Élevé (> 40%)' if dti > 40 else '🟢 Acceptable (≤ 40%)'}"
        )

    modele_choisi = st.selectbox(
        "🎯 Modèle à utiliser pour la prédiction",
        options=list(MODELES.keys()),
        index=list(MODELES.keys()).index(st.session_state["modele_choisi"]),
        help="La Régression Logistique est le modèle de production recommandé"
    )

    show_comparison = st.checkbox(
        "🔬 Afficher aussi les 2 autres modèles en comparaison",
        value=st.session_state["show_comparison"],
        help="À titre de démonstration uniquement"
    )

    submitted = st.form_submit_button(
        "🔍 Analyser le risque de défaut",
        use_container_width=True
    )

# ── RÉSULTAT ──────────────────────────────────────────────────────────────────
if submitted:
    # Sauvegarde dans session_state
    st.session_state["credit_lines"]    = credit_lines
    st.session_state["loan_amt"]        = loan_amt
    st.session_state["total_debt"]      = total_debt
    st.session_state["fico_score"]      = fico_score
    st.session_state["income"]          = income
    st.session_state["years_employed"]  = years_employed
    st.session_state["modele_choisi"]   = modele_choisi
    st.session_state["show_comparison"] = show_comparison

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

    model = models_loaded[modele_choisi]

    st.divider()
    st.subheader(f"📊 Résultat — {modele_choisi}")

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
                use_container_width=True
            )
    else:
        st.info("Modèle non chargé — voici le vecteur qui serait transmis au modèle :")
        st.dataframe(
            input_data.T.rename(columns={0: "Valeur saisie"}),
            use_container_width=True
        )

    # ── COMPARAISON ───────────────────────────────────────────────────────────
    if show_comparison:
        st.divider()
        st.subheader("🔬 Comparaison avec les autres modèles")
        st.caption(
            "Ces résultats sont fournis à titre comparatif pour l'équipe risques."
        )

        autres_modeles = {
            nom: mod for nom, mod in models_loaded.items()
            if nom != modele_choisi
        }

        cols = st.columns(len(autres_modeles))
        for i, (nom, mod) in enumerate(autres_modeles.items()):
            with cols[i]:
                st.markdown(f"**{nom}**")
                if mod is not None:
                    proba_comp = mod.predict_proba(input_data)[0][1]
                    pred_comp  = mod.predict(input_data)[0]
                    if pred_comp == 1:
                        st.error("🚨 DÉFAUT PROBABLE")
                    else:
                        st.success("✅ PAS DE DÉFAUT PRÉVU")
                    st.metric("PD", f"{proba_comp*100:.1f}%")
                    st.progress(float(proba_comp))
                else:
                    st.warning(f"Modèle {nom} non disponible")