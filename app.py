# ============================================================
# ATTRITION AI — ULTRA PREMIUM VISUAL VERSION
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Attrition AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-deep:    #05070f;
    --bg-mid:     #0b0f1e;
    --accent1:    #f97316;
    --accent2:    #ec4899;
    --accent3:    #06b6d4;
    --success:    #10b981;
    --danger:     #ef4444;
    --glass-bg:   rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.08);
    --text-main:  #f1f5f9;
    --text-muted: #64748b;
    --font:       'Sora', sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(249,115,22,0.12), transparent),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(236,72,153,0.10), transparent),
        radial-gradient(ellipse 50% 60% at 50% 50%, rgba(6,182,212,0.05), transparent),
        linear-gradient(160deg, #05070f 0%, #0b0f1e 50%, #05070f 100%) !important;
    background-attachment: fixed !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b18 0%, #0d1225 100%) !important;
    border-right: 1px solid rgba(249,115,22,0.15) !important;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1400px !important;
}

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeSlideUp 0.6s ease both;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(249,115,22,0.6), transparent);
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(249,115,22,0.12), 0 0 0 1px rgba(249,115,22,0.2);
}

.metric-wrap {
    display: flex;
    gap: 1.2rem;
    margin: 1.2rem 0;
}
.metric-box {
    flex: 1;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    animation: fadeSlideUp 0.7s ease both;
    transition: transform 0.25s, box-shadow 0.25s;
}
.metric-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(249,115,22,0.15);
}
.metric-box .label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.metric-box .value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.metric-box .sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
}
.metric-box .accent-line {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 16px 16px;
}
.accent-orange { background: linear-gradient(90deg, var(--accent1), var(--accent2)); }
.accent-cyan   { background: linear-gradient(90deg, var(--accent3), var(--accent1)); }
.accent-pink   { background: linear-gradient(90deg, var(--accent2), var(--accent3)); }

.page-title {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent1) 70%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeSlideUp 0.5s ease both;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
    animation: fadeSlideUp 0.6s ease both;
}

.risk-high {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 50px;
    padding: 0.6rem 1.4rem;
    color: #fca5a5;
    font-weight: 700;
    font-size: 1rem;
    animation: pulse 2s infinite;
}
.risk-low {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 50px;
    padding: 0.6rem 1.4rem;
    color: #6ee7b7;
    font-weight: 700;
    font-size: 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.4rem !important;
    font-family: var(--font) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(249,115,22,0.35) !important;
}
.stButton > button:hover {
    transform: scale(1.04) translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(249,115,22,0.5) !important;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 2.2rem 0 1rem;
}
.section-header .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent1);
    box-shadow: 0 0 8px var(--accent1);
}
.section-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}
.section-header .line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(249,115,22,0.4), transparent);
}

.insight-box {
    background: linear-gradient(135deg, rgba(249,115,22,0.08), rgba(236,72,153,0.06));
    border: 1px solid rgba(249,115,22,0.2);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin: 0.6rem 0;
    font-size: 0.85rem;
    color: #cbd5e1;
}
.insight-box strong { color: var(--accent1); }

.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(249,115,22,0.3), rgba(236,72,153,0.2), transparent);
    margin: 2rem 0;
    border: none;
}

.risk-bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 50px;
    height: 10px;
    overflow: hidden;
    margin-top: 0.5rem;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #10b981, #f97316, #ef4444);
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
    50%       { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(255,255,255,0.04)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(size=11)
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)")
)

with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1.5rem'>
        <div style='font-size:1.25rem;font-weight:800;background:linear-gradient(135deg,#f97316,#ec4899);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            🔴 Attrition AI
        </div>
        <div style='font-size:0.7rem;color:#64748b;letter-spacing:0.1em;text-transform:uppercase;'>
            Powered by Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio("Navigate", ["🎯 Score", "📊 Dashboard"], label_visibility="collapsed")
    st.markdown("<hr style='border:none;height:1px;background:rgba(249,115,22,0.2);margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#475569;line-height:1.8;'>
        <b style='color:#64748b;'>Model Features</b><br>
        Age · Income · Overtime<br>
        Job Satisfaction · Tenure<br>
        Promotion History · Manager Risk
    </div>
    """, unsafe_allow_html=True)

@st.cache_resource
def load():
    model     = joblib.load("attrition_model.pkl")
    scaler    = joblib.load("scaler.pkl")
    encoders  = joblib.load("label_encoders.pkl")
    features  = joblib.load("feature_names.pkl")
    threshold = joblib.load("optimal_threshold.pkl")
    explainer = None
    try:
        import shap
        explainer = shap.Explainer(model.predict_proba, scaler.transform)
    except Exception:
        pass
    return model, scaler, encoders, features, threshold, explainer

model, scaler, encoders, features, threshold, explainer = load()

def prepare(data):
    df = pd.DataFrame([data])
    for col, le in encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col])
            except Exception:
                df[col] = 0
    df['TenureToSalaryRatio']  = df['YearsAtCompany'] / (df['MonthlyIncome'] / 1000 + 1e-9)
    df['NoPromotionFlag']      = (df['YearsSinceLastPromotion'] >= 3).astype(int)
    df['OvertimeRiskWeight']   = (df['OverTime'] == 1).astype(int) * 2
    df['SatisfactionScore']    = (df['JobSatisfaction'] + df['EnvironmentSatisfaction'] + df['RelationshipSatisfaction']) / 3
    df['CareerStagnation']     = df['YearsInCurrentRole'] / (df['TotalWorkingYears'] + 1)
    df['LowIncomeFlag']        = (df['MonthlyIncome'] < 3000).astype(int)
    df['ManagerRisk']          = (df['YearsWithCurrManager'] < 2).astype(int)
    for f in features:
        if f not in df.columns:
            df[f] = 0
    df = df[features]
    return scaler.transform(df), df

def make_gauge(prob, threshold):
    color = "#ef4444" if prob >= threshold else "#10b981"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(prob * 100, 1),
        delta={'reference': round(threshold * 100, 1),
               'increasing': {'color': '#ef4444'},
               'decreasing': {'color': '#10b981'},
               'font': {'size': 14}},
        number={'suffix': '%', 'font': {'size': 42, 'color': '#f1f5f9', 'family': 'Sora'}},
        title={'text': "Attrition Risk Score", 'font': {'size': 15, 'color': '#94a3b8', 'family': 'Sora'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155",
                     'tickfont': {'size': 10, 'color': '#64748b'}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0,  40],  'color': 'rgba(16,185,129,0.12)'},
                {'range': [40, 70],  'color': 'rgba(234,179,8,0.12)'},
                {'range': [70, 100], 'color': 'rgba(239,68,68,0.12)'},
            ],
            'threshold': {'line': {'color': '#f97316', 'width': 2},
                          'thickness': 0.75, 'value': threshold * 100}
        }
    ))
    fig.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Sora"),
                      margin=dict(l=30, r=30, t=20, b=10))
    return fig

def make_feature_bar(raw_df, model):
    try:
        imp = model.feature_importances_
        names = raw_df.columns.tolist()
        top_idx = np.argsort(imp)[-10:][::-1]
        fig = go.Figure(go.Bar(
            x=[imp[i] for i in top_idx],
            y=[names[i] for i in top_idx],
            orientation='h',
            marker=dict(
                color=[imp[i] for i in top_idx],
                colorscale=[[0,'#06b6d4'],[0.5,'#f97316'],[1,'#ec4899']],
                line=dict(width=0)
            )
        ))
        fig.update_layout(title="Feature Importance (Top 10)", height=320,
                          yaxis=dict(autorange="reversed"), **PLOTLY_LAYOUT)
        return fig
    except Exception:
        return None

# ============================================================
# PAGE 1 — SCORING
# ============================================================
if page == "🎯 Score":

    st.markdown('<div class="page-title">🎯 Employee Risk Scoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Enter employee attributes to generate an AI-powered attrition risk prediction.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="section-header">
        <div class="dot"></div><h3>Employee Profile</h3><div class="line"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        age     = st.slider("🎂 Age", 18, 60, 30)
        income  = st.number_input("💰 Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=100)
    with r1c2:
        job_sat  = st.slider("😊 Job Satisfaction", 1, 4, 3)
        overtime = st.selectbox("⏱️ Works Overtime?", ["Yes", "No"])
    with r1c3:
        years   = st.slider("🏢 Years at Company", 0, 40, 5)
        env_sat = st.slider("🌿 Environment Satisfaction", 1, 4, 3)

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        years_role = st.slider("📌 Years in Current Role", 0, 20, 3)
    with r2c2:
        yrs_promo  = st.slider("🚀 Years Since Promotion", 0, 15, 2)
    with r2c3:
        total_yrs  = st.slider("📅 Total Working Years", 0, 40, 10)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("🚀 Run AI Risk Analysis")

    if run:
        data = {
            "Age": age, "MonthlyIncome": income,
            "JobSatisfaction": job_sat, "OverTime": overtime,
            "YearsAtCompany": years, "EnvironmentSatisfaction": env_sat,
            "RelationshipSatisfaction": 3, "YearsInCurrentRole": years_role,
            "YearsSinceLastPromotion": yrs_promo, "TotalWorkingYears": total_yrs,
            "YearsWithCurrManager": 3,
        }
        X, raw = prepare(data)
        prob   = float(model.predict_proba(X)[0, 1])
        cost   = income * 12 * 1.5
        risk_color = "#ef4444" if prob >= threshold else "#10b981"

        st.markdown(f"""
        <div class="metric-wrap">
            <div class="metric-box">
                <div class="label">Attrition Probability</div>
                <div class="value">{prob:.1%}</div>
                <div class="sub">Model confidence score</div>
                <div class="risk-bar-wrap">
                    <div class="risk-bar-fill" style="width:{prob*100:.1f}%"></div>
                </div>
                <div class="accent-line accent-orange"></div>
            </div>
            <div class="metric-box">
                <div class="label">Decision Threshold</div>
                <div class="value">{threshold:.1%}</div>
                <div class="sub">Optimal cut-off</div>
                <div class="accent-line accent-cyan"></div>
            </div>
            <div class="metric-box">
                <div class="label">Replacement Cost Est.</div>
                <div class="value">${cost:,.0f}</div>
                <div class="sub">1.5× annual salary</div>
                <div class="accent-line accent-pink"></div>
            </div>
            <div class="metric-box">
                <div class="label">Risk Level</div>
                <div class="value" style="background:linear-gradient(135deg,{risk_color},{risk_color}88);
                     -webkit-background-clip:text;">{"HIGH" if prob >= threshold else "LOW"}</div>
                <div class="sub">vs threshold</div>
                <div class="accent-line" style="background:{risk_color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div class="section-header">
            <div class="dot"></div><h3>Risk Analysis</h3><div class="line"></div>
        </div>""", unsafe_allow_html=True)

        gc1, gc2 = st.columns(2)

        with gc1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(make_gauge(prob, threshold), use_container_width=True)
            verdict = ('<div class="risk-high">⚠️ HIGH RISK — Immediate Action Required</div>'
                       if prob >= threshold else
                       '<div class="risk-low">✅ LOW RISK — Employee Appears Stable</div>')
            st.markdown(verdict, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with gc2:
            cats   = ['Job Sat.', 'Env. Sat.', 'Income Score', 'Tenure', 'Work-Life']
            scores = [job_sat/4, env_sat/4, min(income/10000,1), min(years/20,1),
                      0.0 if overtime=="Yes" else 1.0]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=scores+[scores[0]], theta=cats+[cats[0]],
                fill='toself', name='Employee',
                line=dict(color='#f97316', width=2),
                fillcolor='rgba(249,115,22,0.15)',
                marker=dict(color='#f97316', size=7)
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[0.7]*5+[0.7], theta=cats+[cats[0]],
                name='Benchmark',
                line=dict(color='#06b6d4', width=1.5, dash='dot'),
                fillcolor='rgba(6,182,212,0.05)', fill='toself',
                marker=dict(color='#06b6d4', size=5)
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,1],
                                   gridcolor="rgba(255,255,255,0.07)",
                                   tickfont=dict(size=9, color='#64748b')),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.07)",
                                    tickfont=dict(size=10, color='#94a3b8'))
                ),
                title=dict(text="Employee Dimensions vs Benchmark",
                           font=dict(size=14, color='#94a3b8', family='Sora')),
                height=300, paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Sora"),
                legend=dict(font=dict(size=10, color='#94a3b8'), bgcolor="rgba(0,0,0,0)")
            )
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""<div class="section-header">
            <div class="dot"></div><h3>Model Explanation</h3><div class="line"></div>
        </div>""", unsafe_allow_html=True)

        ex1, ex2 = st.columns([1.4, 1])

        with ex1:
            shap_done = False
            if explainer:
                try:
                    import shap
                    shap_vals = explainer(X)
                    fig_shap, ax = plt.subplots(figsize=(8, 4))
                    fig_shap.patch.set_alpha(0)
                    ax.set_facecolor("none")
                    shap.plots.waterfall(shap_vals[0], show=False, ax=ax)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.pyplot(fig_shap, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    shap_done = True
                except Exception:
                    pass
            if not shap_done:
                fig_imp = make_feature_bar(raw, model)
                if fig_imp:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_imp, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        with ex2:
            factors = []
            if overtime == "Yes":  factors.append(("⏱️ Overtime",            "HIGH", "#ef4444"))
            if job_sat <= 2:       factors.append(("😞 Job Satisfaction",     "LOW",  "#ef4444"))
            if yrs_promo >= 3:     factors.append(("🚀 No Recent Promotion",  "FLAG", "#f97316"))
            if income < 3000:      factors.append(("💰 Low Income",           "FLAG", "#f97316"))
            if env_sat <= 2:       factors.append(("🌿 Environment Sat.",     "LOW",  "#f97316"))
            if years < 2:          factors.append(("🏢 Very New Employee",    "NOTE", "#06b6d4"))

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**🔍 Risk Factors Detected**")
            if factors:
                for name, level, col in factors:
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:0.45rem 0.7rem;margin:0.3rem 0;border-radius:8px;
                                background:rgba(255,255,255,0.03);border-left:3px solid {col};">
                        <span style="font-size:0.85rem;color:#cbd5e1">{name}</span>
                        <span style="font-size:0.72rem;font-weight:700;color:{col};
                               background:{col}22;border-radius:4px;padding:2px 8px;">{level}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="insight-box">✅ No major risk factors detected.</div>', unsafe_allow_html=True)

            st.markdown("<br>**💡 Recommendations**", unsafe_allow_html=True)
            recs = []
            if overtime == "Yes": recs.append("Reduce overtime or compensate better")
            if job_sat <= 2:      recs.append("Schedule 1-on-1 to address concerns")
            if yrs_promo >= 3:    recs.append("Consider promotion or role expansion")
            if income < 3000:     recs.append("Benchmark salary against market rates")
            if not recs:          recs.append("Continue current engagement strategy")
            for r in recs:
                st.markdown(f'<div class="insight-box">→ <strong>{r}</strong></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE 2 — DASHBOARD
# ============================================================
else:
    st.markdown('<div class="page-title">📊 Company Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Organisation-wide attrition intelligence.</div>', unsafe_allow_html=True)

    try:
        df = pd.read_csv("attrition_risk_scored.csv")
        high_risk_n = (df['RiskScore'] > threshold).sum()
        avg_risk    = df['RiskScore'].mean()
        total_cost  = df.loc[df['RiskScore'] > threshold, 'MonthlyIncome'].sum() * 12 * 1.5 \
                      if 'MonthlyIncome' in df.columns else 0

        st.markdown(f"""
        <div class="metric-wrap">
            <div class="metric-box">
                <div class="label">Total Employees</div>
                <div class="value">{len(df):,}</div>
                <div class="sub">In dataset</div>
                <div class="accent-line accent-orange"></div>
            </div>
            <div class="metric-box">
                <div class="label">Avg Risk Score</div>
                <div class="value">{avg_risk:.1%}</div>
                <div class="sub">Across all employees</div>
                <div class="accent-line accent-pink"></div>
            </div>
            <div class="metric-box">
                <div class="label">High-Risk Count</div>
                <div class="value">{high_risk_n:,}</div>
                <div class="sub">Above threshold</div>
                <div class="accent-line accent-cyan"></div>
            </div>
            <div class="metric-box">
                <div class="label">High-Risk Ratio</div>
                <div class="value">{high_risk_n/len(df):.1%}</div>
                <div class="sub">Flagged employees</div>
                <div class="accent-line accent-orange"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div class="section-header">
            <div class="dot"></div><h3>Risk Distribution</h3><div class="line"></div>
        </div>""", unsafe_allow_html=True)

        r1a, r1b = st.columns([1.6, 1])

        with r1a:
            bins = np.linspace(0, 1, 31)
            hist_vals, bin_edges = np.histogram(df['RiskScore'], bins=bins)
            bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2
            bar_colors = ["rgba(16,185,129,0.85)" if m < 0.4 else
                          "rgba(234,179,8,0.85)"  if m < 0.7 else
                          "rgba(239,68,68,0.85)"  for m in bin_mids]
            fig_hist = go.Figure(go.Bar(
                x=bin_mids, y=hist_vals,
                marker_color=bar_colors, marker_line_width=0,
                hovertemplate="Risk: %{x:.2f}<br>Count: %{y}<extra></extra>"
            ))
            fig_hist.add_vline(x=threshold, line_dash="dash",
                               line_color="#f97316", line_width=2,
                               annotation_text=f"Threshold {threshold:.0%}",
                               annotation_font_color="#f97316",
                               annotation_position="top right")
            fig_hist.update_layout(title="Risk Score Distribution", xaxis_title="Risk Score",
                                   yaxis_title="# Employees", bargap=0.05, height=320, **PLOTLY_LAYOUT)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1b:
            low = (df['RiskScore'] <= 0.4).sum()
            med = ((df['RiskScore'] > 0.4) & (df['RiskScore'] <= 0.7)).sum()
            high = (df['RiskScore'] > 0.7).sum()
            fig_donut = go.Figure(go.Pie(
                labels=["Low Risk","Medium Risk","High Risk"],
                values=[low, med, high], hole=0.62,
                marker=dict(colors=["#10b981","#eab308","#ef4444"],
                            line=dict(color="#0b0f1e", width=2)),
                textfont=dict(family="Sora", size=11, color="#f1f5f9"),
                hovertemplate="%{label}<br>%{value} (%{percent})<extra></extra>"
            ))
            fig_donut.update_layout(title="Risk Tier Breakdown", height=320, **PLOTLY_LAYOUT)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if "Department" in df.columns or "Age" in df.columns:
            st.markdown("""<div class="section-header">
                <div class="dot"></div><h3>Segment Analysis</h3><div class="line"></div>
            </div>""", unsafe_allow_html=True)
            r2a, r2b = st.columns(2)

            with r2a:
                if "Department" in df.columns:
                    dept_avg = df.groupby("Department")["RiskScore"].mean().sort_values()
                    fig_dept = go.Figure(go.Bar(
                        x=dept_avg.values, y=dept_avg.index, orientation='h',
                        marker=dict(color=dept_avg.values,
                                    colorscale=[[0,'#10b981'],[0.5,'#f97316'],[1,'#ef4444']],
                                    cmin=0, cmax=1, line=dict(width=0)),
                        hovertemplate="%{y}: %{x:.1%}<extra></extra>"
                    ))
                    fig_dept.update_layout(title="Avg Risk by Department",
                                           xaxis_tickformat=".0%", height=300, **PLOTLY_LAYOUT)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_dept, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with r2b:
                if "Age" in df.columns:
                    df['AgeBand'] = pd.cut(df['Age'], bins=[18,25,30,35,40,50,60],
                                           labels=["18-25","26-30","31-35","36-40","41-50","51-60"])
                    age_risk = df.groupby("AgeBand")["RiskScore"].mean()
                    fig_age = go.Figure(go.Bar(
                        x=age_risk.index.astype(str), y=age_risk.values,
                        marker=dict(color=age_risk.values,
                                    colorscale=[[0,'#06b6d4'],[1,'#ec4899']],
                                    line=dict(width=0)),
                        hovertemplate="Age %{x}<br>%{y:.1%}<extra></extra>"
                    ))
                    fig_age.update_layout(title="Risk by Age Group",
                                          yaxis_tickformat=".0%", height=300, **PLOTLY_LAYOUT)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_age, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        r3a, r3b = st.columns(2)
        with r3a:
            if "OverTime" in df.columns:
                ot_box = px.box(df, x="OverTime", y="RiskScore", color="OverTime",
                                color_discrete_map={"Yes":"#ef4444","No":"#10b981"},
                                title="Risk: Overtime vs No Overtime", points="outliers")
                ot_box.update_layout(height=300, showlegend=False, **PLOTLY_LAYOUT)
                ot_box.update_traces(marker_size=3)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.plotly_chart(ot_box, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with r3b:
            if "MonthlyIncome" in df.columns:
                sample = df.sample(min(400, len(df)), random_state=42)
                fig_sc = px.scatter(sample, x="MonthlyIncome", y="RiskScore",
                                    color="RiskScore",
                                    color_continuous_scale=["#10b981","#f97316","#ef4444"],
                                    opacity=0.7, title="Income vs Risk Score")
                fig_sc.update_layout(height=300, coloraxis_showscale=False, **PLOTLY_LAYOUT)
                fig_sc.update_traces(marker_size=5)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_sc, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        heat_cols = [c for c in ["JobSatisfaction","EnvironmentSatisfaction",
                                  "YearsAtCompany","YearsSinceLastPromotion"] if c in df.columns]
        if len(heat_cols) >= 2:
            st.markdown("""<div class="section-header">
                <div class="dot"></div><h3>Correlation Intelligence</h3><div class="line"></div>
            </div>""", unsafe_allow_html=True)
            corr_df = df[heat_cols + ["RiskScore"]].corr()
            fig_heat = go.Figure(go.Heatmap(
                z=corr_df.values, x=corr_df.columns, y=corr_df.index,
                colorscale=[[0,'#06b6d4'],[0.5,'#0b0f1e'],[1,'#ec4899']],
                zmid=0, text=np.round(corr_df.values,2), texttemplate="%{text}",
                textfont=dict(size=11, color="#f1f5f9"),
                hovertemplate="%{x} vs %{y}<br>r = %{z:.3f}<extra></extra>"
            ))
            fig_heat.update_layout(title="Feature Correlation Matrix", height=320, **PLOTLY_LAYOUT)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_heat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""<div class="section-header">
            <div class="dot"></div><h3>🔴 High-Risk Employees</h3><div class="line"></div>
        </div>""", unsafe_allow_html=True)
        high_df   = df[df['RiskScore'] > threshold].sort_values("RiskScore", ascending=False)
        show_cols = [c for c in ["EmployeeNumber","Department","Age",
                                  "MonthlyIncome","OverTime","RiskScore"] if c in high_df.columns]
        styled = high_df[show_cols].head(15).style \
            .background_gradient(subset=["RiskScore"], cmap="RdYlGn_r") \
            .format({"RiskScore": "{:.2%}", "MonthlyIncome": "${:,.0f}"})
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.dataframe(styled, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if total_cost > 0:
            st.markdown(f"""
            <div class="insight-box" style="margin-top:1rem;font-size:0.92rem;">
                💸 <strong>Estimated Replacement Cost Exposure:</strong>
                ${total_cost:,.0f} — based on 1.5× annual salary for {high_risk_n} high-risk employees.
            </div>""", unsafe_allow_html=True)

    except FileNotFoundError:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">⚠️</div>
            <div style="font-size:1.2rem;font-weight:700;color:#f97316;margin-bottom:0.5rem;">
                Dataset Not Found
            </div>
            <div style="color:#64748b;font-size:0.9rem;">
                Run your notebook to generate <code>attrition_risk_scored.csv</code> then reload.
            </div>
        </div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Dashboard error: {e}")