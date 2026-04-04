import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard — Performances des modèles")
st.divider()

# Métriques (à remplacer par les vraies une fois MLflow prêt)
df = pd.DataFrame({
    "Modèle"   : ["Decision Tree", "Logistic Regression", "Random Forest"],
    "Accuracy" : [0.932, 0.935, 0.941],
    "AUC-ROC"  : [0.621, 0.843, 0.862],
    "Precision": [0.54,  0.72,  0.78],
    "Recall"   : [0.38,  0.41,  0.46],
    "F1-Score" : [0.44,  0.52,  0.58],
})

st.subheader("🏆 Comparaison des modèles")
st.dataframe(
    df.style.highlight_max(subset=["AUC-ROC", "F1-Score"], color="#d4edda"),
    width='stretch'
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df, x="Modèle", y="AUC-ROC", title="AUC-ROC par modèle",
                 color="Modèle", color_discrete_sequence=["#636EFA","#EF553B","#00CC96"])
    fig.update_layout(showlegend=False, yaxis_range=[0,1])
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
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        title="Radar des métriques"
    )
    st.plotly_chart(fig2, width='stretch')

st.info("💡 Les métriques seront mises à jour automatiquement une fois les runs MLflow intégrés.")