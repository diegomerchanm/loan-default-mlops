import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard — Performances des modèles")
st.divider()

# Vraies métriques issues du NB3
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

with col1:
    st.markdown("**Régression Logistique**")
    st.metric("F1-Score", "0.9906")
    st.metric("Recall", "1.0")
    st.metric("AUC-ROC", "1.0")

with col2:
    st.markdown("**Decision Tree**")
    st.metric("F1-Score", "0.9689")
    st.metric("Recall", "0.9676")
    st.metric("AUC-ROC", "0.9804")

with col3:
    st.markdown("**Random Forest**")
    st.metric("F1-Score", "0.9752")
    st.metric("Recall", "0.9568")
    st.metric("AUC-ROC", "0.9997")

st.divider()

st.success(
    "Meilleur modèle retenu : Régression Logistique — "
    "F1 = 0.9906, Recall = 1.0, AUC-ROC = 1.0"
)

st.caption(
    "Métriques issues du NB3 — Entraînement sur Loan_Data.csv "
    "(8 000 train / 2 000 test — stratifié)"
)