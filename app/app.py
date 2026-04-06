import streamlit as st

st.set_page_config(
    page_title="Loan Default Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .hero-title    { font-size:2.6rem; font-weight:800; color:#1a1a2e; margin-bottom:0; }
    .hero-sub      { font-size:1.1rem; color:#555; margin-top:4px; }
    .kpi-box       { background:#f7f9fc; border-radius:12px; padding:18px 22px;
                     border-left:4px solid #3b82f6; margin-bottom:8px; }
    .kpi-label     { font-size:.8rem; color:#888; font-weight:600; text-transform:uppercase; }
    .kpi-value     { font-size:1.9rem; font-weight:800; color:#1a1a2e; }
    .kpi-delta     { font-size:.8rem; color:#888; margin-top:2px; }
    .section-title { font-size:1.3rem; font-weight:700; color:#1a1a2e; margin-top:1rem; }
    .insight-box   { background:#eef2ff; border-left:4px solid #6366f1;
                     border-radius:8px; padding:14px 18px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">🏦 Loan Default Predictor</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">'
    'Système de scoring de risque de crédit — Division Risques · Banque de détail'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Indicateurs clés du portefeuille</p>',
            unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown("""
    <div class="kpi-box">
        <div class="kpi-label">Clients analysés</div>
        <div class="kpi-value">10 000</div>
        <div class="kpi-delta">Dataset d'entraînement</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-box" style="border-color:#e74c3c">
        <div class="kpi-label">Taux de défaut (PD)</div>
        <div class="kpi-value">18.5%</div>
        <div class="kpi-delta">↑ Supérieur au seuil attendu</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-box" style="border-color:#f39c12">
        <div class="kpi-label">Perte attendue (EL)</div>
        <div class="kpi-value">EL = PD × LGD × EAD</div>
        <div class="kpi-delta">Cadre Bâle III</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-box" style="border-color:#27ae60">
        <div class="kpi-label">Feature la + prédictive</div>
        <div class="kpi-value">r = 0.86</div>
        <div class="kpi-delta">credit_lines_outstanding</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown("""
    <div class="kpi-box" style="border-color:#8e44ad">
        <div class="kpi-label">Modèles comparés</div>
        <div class="kpi-value">3</div>
        <div class="kpi-delta">DT · LR · Random Forest</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── CONTEXTE + NAVIGATION ─────────────────────────────────────────────────────
col_ctx, col_nav = st.columns([3, 2])

with col_ctx:
    st.markdown('<p class="section-title">🎯 Contexte & enjeux métier</p>',
                unsafe_allow_html=True)
    st.markdown("""
    La banque observe des **taux de défaut supérieurs aux prévisions** sur son portefeuille 
    de prêts personnels. Dans le cadre réglementaire **Bâle III / IFRS 9**, elle est tenue 
    de provisionner les pertes attendues et d'allouer du capital en conséquence.

    Ce système de scoring permet à la division Risques de :

    - **Estimer la PD** *(Probability of Default)* avant tout octroi de crédit
    - **Détecter les profils à risque** grâce aux signaux clés : lignes de crédit, 
      dette totale, score FICO
    - **Alimenter le calcul de l'Expected Loss** : EL = PD × LGD × EAD
    - **Orienter les décisions d'octroi** et les niveaux de garanties requis

    > ⚠️ *Le déséquilibre des classes (81.5% non-défaut / 18.5% défaut) impose 
    de privilégier le **F1-Score et le Recall** plutôt que l'accuracy comme 
    métriques d'évaluation.*
    """)

with col_nav:
    st.markdown('<p class="section-title">🧭 Navigation</p>', unsafe_allow_html=True)

    st.info("""
    **🔮 Prédiction**

    Saisir le profil d'un client et obtenir :
    - Sa probabilité de défaut (PD)
    - Sa classe de risque (Faible / Modéré / Élevé)
    - Une recommandation d'octroi
    """)

    st.success("""
    **📊 Dashboard**

    Comparer les 3 modèles entraînés :
    - Decision Tree
    - Logistic Regression
    - Random Forest
    """)

st.divider()

# ── INSIGHTS EDA ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">🔍 Principaux enseignements de l\'EDA</p>',
            unsafe_allow_html=True)

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown("""
    <div class="insight-box">
        <b>📈 credit_lines_outstanding</b><br>
        Corrélation de <b>+0.86</b> avec le défaut.<br>
        Variable la plus prédictive du modèle.
    </div>""", unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="insight-box">
        <b>📉 fico_score</b><br>
        Corrélation de <b>-0.32</b> avec le défaut.<br>
        Plus le score est élevé, moins le risque est fort.
    </div>""", unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="insight-box">
        <b>⚖️ Déséquilibre des classes</b><br>
        18.5% de défauts seulement.<br>
        Métrique retenue : <b>F1-Score & Recall</b>.
    </div>""", unsafe_allow_html=True)

st.divider()

# ── GRILLE DE RISQUE ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">🗂️ Grille de notation interne</p>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:#d4edda;border-radius:10px;padding:16px;text-align:center">
        <div style="font-size:1.5rem">🟢</div>
        <div style="font-weight:700;font-size:1.1rem;color:#155724">Risque FAIBLE</div>
        <div style="color:#155724;margin-top:8px">PD &lt; 30%</div>
        <div style="color:#155724;font-size:.85rem;margin-top:4px">
            Octroi recommandé · Conditions standard
        </div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#fff3cd;border-radius:10px;padding:16px;text-align:center">
        <div style="font-size:1.5rem">🟡</div>
        <div style="font-weight:700;font-size:1.1rem;color:#856404">Risque MODÉRÉ</div>
        <div style="color:#856404;margin-top:8px">30% ≤ PD &lt; 60%</div>
        <div style="color:#856404;font-size:.85rem;margin-top:4px">
            Analyse approfondie · Garanties requises
        </div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#f8d7da;border-radius:10px;padding:16px;text-align:center">
        <div style="font-size:1.5rem">🔴</div>
        <div style="font-weight:700;font-size:1.1rem;color:#721c24">Risque ÉLEVÉ</div>
        <div style="color:#721c24;margin-top:8px">PD ≥ 60%</div>
        <div style="color:#721c24;font-size:.85rem;margin-top:4px">
            Refus recommandé · Comité de crédit
        </div>
    </div>""", unsafe_allow_html=True)

st.divider()

st.caption(
    "🏦 Banque de détail · Division Risques de Crédit · "
    "Dataset synthétique pédagogique (Loan_Data.csv — 10 000 clients) · "
    "Projet MLOps — 2025"
)