import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard — Performances des modèles")
st.divider()

# ── Chargement dynamique des métriques depuis le CSV du NB3 ───────────────────
CSV_PATH = Path(__file__).parents[2] / "outputs" / "NB3_comparaison_modeles.csv"

try:
    df_raw = pd.read_csv(CSV_PATH)
    df = df_raw[["modèle", "f1_test", "recall_test", "precision_test",
                 "accuracy_test", "roc_auc_test"]].rename(columns={
        "modèle"         : "Modèle",
        "f1_test"        : "F1-Score",
        "recall_test"    : "Recall",
        "precision_test" : "Precision",
        "accuracy_test"  : "Accuracy",
        "roc_auc_test"   : "AUC-ROC",
    })
    st.success("Métriques chargées depuis outputs/NB3_comparaison_modeles.csv")
except FileNotFoundError:
    st.warning("Fichier outputs/NB3_comparaison_modeles.csv introuvable — métriques de secours affichées.")
    df = pd.DataFrame({
        "Modèle"   : ["Régression Logistique", "Decision Tree", "Random Forest"],
        "Accuracy" : [0.9965, 0.9885, 0.9910],
        "AUC-ROC"  : [1.0,    0.9804, 0.9997],
        "Precision": [0.9814, 0.9702, 0.9944],
        "Recall"   : [1.0,    0.9676, 0.9568],
        "F1-Score" : [0.9906, 0.9689, 0.9752],
    })

st.subheader("🏆 Comparaison des modèles")
st.dataframe(
    df.style.highlight_max(subset=["AUC-ROC", "F1-Score", "Recall"], color="#d4edda"),
    width='stretch'
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df, x="Modèle", y="AUC-ROC", title="AUC-ROC par modèle",
                 color="Modèle", color_discrete_sequence=["#636EFA","#EF553B","#00CC96"])
    fig.update_layout(showlegend=False, yaxis_range=[0.95, 1.01])
    st.plotly_chart(fig, width='stretch')

with col2:
    cols = ["Accuracy","AUC-ROC","Precision","Recall","F1-Score"]
    fig2 = go.Figure()
    for _, row in df.iterrows():
        fig2.add_trace(go.Scatterpolar(
            r=[row[c] for c in cols], theta=cols,
            fill='toself', name=row["Modèle"]
        ))
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0.95, 1.01])),
        title="Radar des métriques"
    )
    st.plotly_chart(fig2, width='stretch')

st.divider()

# Métriques détaillées
st.subheader("📋 Métriques détaillées")

col1, col2, col3 = st.columns(3)

for col, (_, row) in zip([col1, col2, col3], df.iterrows()):
    with col:
        st.markdown(f"**{row['Modèle']}**")
        st.metric("F1-Score", f"{row['F1-Score']:.4f}")
        st.metric("Recall",   f"{row['Recall']:.4f}")
        st.metric("AUC-ROC",  f"{row['AUC-ROC']:.4f}")
        
st.divider()

# Meilleur modèle
best = df.loc[df["F1-Score"].idxmax()]
st.success(
    f"Meilleur modèle retenu : {best['Modèle']} — "
    f"F1 = {best['F1-Score']:.4f}, "
    f"Recall = {best['Recall']:.4f}, "
    f"AUC-ROC = {best['AUC-ROC']:.4f}"
)

st.caption(
    "Métriques issues du NB3 — Entraînement sur Loan_Data.csv "
    "(8 000 train / 2 000 test — stratifié)"
)