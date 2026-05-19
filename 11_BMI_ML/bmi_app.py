import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="BMI 분류 AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 스타일 ───────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 배경 */
.stApp { background-color: #F7F9FC; }

/* 카드 컴포넌트 */
.card {
    background: white;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 16px;
}

/* 결과 배지 */
.badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* 메트릭 박스 */
.metric-box {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-value { font-size: 28px; font-weight: 700; margin: 4px 0; }
.metric-label { font-size: 13px; color: #6B7280; }

/* 사이드바 */
section[data-testid="stSidebar"] > div {
    background: linear-gradient(160deg, #1E3A5F 0%, #2563EB 100%);
    padding-top: 20px;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label { color: #CBD5E1 !important; }

/* 탭 */
button[data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: 600 !important;
}

/* 헤더 */
h1 { color: #1E3A5F !important; }
h2 { color: #1E40AF !important; }
h3 { color: #374151 !important; }

/* 구분선 */
hr { border-color: #E5E7EB; }
</style>
""", unsafe_allow_html=True)

# ── 상수 ──────────────────────────────────────────────────────
INDEX_INFO = {
    0: {"name": "극저체중",    "en": "Extremely Weak", "bmi": "~16",       "color": "#60A5FA", "bg": "#EFF6FF", "advice": "심각한 영양 부족 상태입니다. 즉시 전문의 상담이 필요합니다."},
    1: {"name": "저체중",      "en": "Weak",           "bmi": "16~18.5",   "color": "#34D399", "bg": "#ECFDF5", "advice": "체중이 부족합니다. 균형 잡힌 식단과 근력 운동을 권장합니다."},
    2: {"name": "정상",        "en": "Normal",         "bmi": "18.5~24.9", "color": "#10B981", "bg": "#D1FAE5", "advice": "건강한 체중 범위입니다. 현재 생활습관을 유지하세요."},
    3: {"name": "과체중",      "en": "Overweight",     "bmi": "25~29.9",   "color": "#FBBF24", "bg": "#FFFBEB", "advice": "체중 관리가 필요합니다. 유산소 운동과 식단 조절을 시작하세요."},
    4: {"name": "비만",        "en": "Obesity",        "bmi": "30~39.9",   "color": "#F97316", "bg": "#FFF7ED", "advice": "비만 상태입니다. 생활습관 개선과 전문가 상담을 권장합니다."},
    5: {"name": "고도비만",    "en": "Extreme Obesity","bmi": "40~",       "color": "#EF4444", "bg": "#FEF2F2", "advice": "고도비만입니다. 심혈관·대사 질환 위험이 높습니다. 전문의 상담이 필요합니다."},
}

# ── 데이터/모델 로드 ─────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("bmi_model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    return pd.read_csv("bmi_dataset.csv")

model_obj = load_model()
df = load_data()
model   = model_obj["model"]
scaler  = model_obj["scaler"]

# ── 예측 함수 ─────────────────────────────────────────────────
def predict(gender: str, height: int, weight: int):
    gender_enc = 1 if gender == "Male" else 0
    X = np.array([[gender_enc, height, weight]], dtype=float)
    if scaler:
        X = scaler.transform(X)
    idx = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0] if hasattr(model, "predict_proba") else None
    bmi_val = weight / (height / 100) ** 2
    return idx, proba, bmi_val

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚖️ BMI 분류 AI")
    st.markdown("---")
    st.markdown("### 모델 정보")
    st.markdown(f"**알고리즘** : {model_obj['model_name']}")
    st.markdown(f"**Test F1** : `{model_obj['test_f1_macro']:.4f}`")
    st.markdown(f"**CV F1**   : `{model_obj['cv_f1_macro']:.4f}`")
    st.markdown("---")
    st.markdown("### 분류 기준")
    for i, info in INDEX_INFO.items():
        st.markdown(
            f"<span style='color:{info['color']};font-weight:700'>■</span> "
            f"**{info['name']}** (BMI {info['bmi']})",
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.caption("데이터: 500명 | 피처: Gender · Height · Weight")

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("# ⚖️ BMI 비만도 분류 AI")
st.markdown("키와 몸무게를 입력하면 AI가 비만 단계를 예측합니다.")
st.markdown("---")

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 BMI 예측", "📊 데이터 탐색", "🏆 모델 성능"])


# ════════════════════════════════════════════════════════════
# TAB 1 — BMI 예측
# ════════════════════════════════════════════════════════════
with tab1:
    col_in, col_out = st.columns([1, 1.6], gap="large")

    # ── 입력 패널 ────────────────────────────────────────────
    with col_in:
        st.markdown("### 신체 정보 입력")
        gender = st.radio("성별", ["Male", "Female"],
                          horizontal=True, index=0)
        height = st.slider("키 (cm)", 140, 199, 170, step=1)
        weight = st.slider("몸무게 (kg)", 50, 160, 70, step=1)

        # 실시간 BMI 계산
        bmi_live = weight / (height / 100) ** 2
        st.markdown(f"""
        <div class="card" style="background:#F0F9FF;border-left:4px solid #2563EB;padding:14px 20px;">
            <div style="font-size:13px;color:#6B7280;">참고 BMI (공식 계산)</div>
            <div style="font-size:32px;font-weight:800;color:#1E40AF;">{bmi_live:.1f}</div>
            <div style="font-size:12px;color:#9CA3AF;">Weight(kg) ÷ Height(m)²</div>
        </div>
        """, unsafe_allow_html=True)

        predict_btn = st.button("🤖 AI 예측하기", use_container_width=True, type="primary")

    # ── 결과 패널 ────────────────────────────────────────────
    with col_out:
        st.markdown("### 예측 결과")

        if predict_btn:
            idx, proba, bmi_val = predict(gender, height, weight)
            info = INDEX_INFO[idx]

            # 결과 카드
            st.markdown(f"""
            <div class="card" style="background:{info['bg']};border-left:5px solid {info['color']};">
                <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">예측 결과</div>
                <div style="font-size:36px;font-weight:800;color:{info['color']};">
                    {info['name']} <span style="font-size:18px;">({info['en']})</span>
                </div>
                <div style="font-size:14px;color:#374151;margin-top:10px;">
                    📌 BMI 범위: <b>{info['bmi']}</b> &nbsp;|&nbsp; 계산 BMI: <b>{bmi_val:.1f}</b>
                </div>
                <hr style="margin:12px 0;border-color:#E5E7EB;">
                <div style="font-size:14px;color:#4B5563;">💡 {info['advice']}</div>
            </div>
            """, unsafe_allow_html=True)

            # BMI 게이지 차트
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=bmi_val,
                number={"suffix": "", "font": {"size": 36, "color": info["color"]}},
                gauge={
                    "axis": {"range": [10, 60], "tickwidth": 1},
                    "bar":  {"color": info["color"], "thickness": 0.25},
                    "steps": [
                        {"range": [10, 16],   "color": "#DBEAFE"},
                        {"range": [16, 18.5], "color": "#D1FAE5"},
                        {"range": [18.5, 25], "color": "#A7F3D0"},
                        {"range": [25, 30],   "color": "#FEF3C7"},
                        {"range": [30, 40],   "color": "#FFEDD5"},
                        {"range": [40, 60],   "color": "#FEE2E2"},
                    ],
                    "threshold": {
                        "line": {"color": info["color"], "width": 4},
                        "thickness": 0.8,
                        "value": bmi_val,
                    },
                },
                title={"text": "BMI 게이지", "font": {"size": 16}},
            ))
            fig_gauge.update_layout(
                height=240, margin=dict(t=40, b=10, l=30, r=30),
                paper_bgcolor="white", font_color="#374151",
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # 확률 분포 막대차트
            if proba is not None:
                labels = [INDEX_INFO[i]["name"] for i in range(6)]
                colors = [INFO["color"] for INFO in INDEX_INFO.values()]
                fig_prob = go.Figure(go.Bar(
                    x=labels, y=proba * 100,
                    marker_color=colors,
                    text=[f"{p*100:.1f}%" for p in proba],
                    textposition="outside",
                ))
                fig_prob.update_layout(
                    title="클래스별 예측 확률",
                    yaxis_title="확률 (%)",
                    yaxis_range=[0, 115],
                    height=300,
                    margin=dict(t=50, b=10, l=10, r=10),
                    paper_bgcolor="white",
                    plot_bgcolor="#F9FAFB",
                    font_color="#374151",
                    showlegend=False,
                )
                # 예측 클래스 강조
                opacities = [1.0 if i == idx else 0.35 for i in range(6)]
                fig_prob.data[0].marker.opacity = opacities
                st.plotly_chart(fig_prob, use_container_width=True)

        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:60px 20px;color:#9CA3AF;">
                <div style="font-size:48px;">🤖</div>
                <div style="font-size:16px;margin-top:12px;">왼쪽에서 신체 정보를 입력하고<br><b>AI 예측하기</b> 버튼을 눌러주세요.</div>
            </div>
            """, unsafe_allow_html=True)

    # ── BMI 단계 안내표 ──────────────────────────────────────
    st.markdown("---")
    st.markdown("### BMI 단계별 기준표")
    cols = st.columns(6)
    for i, (col, info) in enumerate(zip(cols, INDEX_INFO.values())):
        with col:
            st.markdown(f"""
            <div style="background:{info['bg']};border-radius:12px;padding:14px 10px;
                        text-align:center;border-top:4px solid {info['color']};">
                <div style="font-size:20px;">{'🟦' if i==0 else '🟩' if i==1 else '✅' if i==2 else '🟨' if i==3 else '🟧' if i==4 else '🟥'}</div>
                <div style="font-size:14px;font-weight:700;color:{info['color']};margin:6px 0;">{info['name']}</div>
                <div style="font-size:12px;color:#6B7280;">BMI {info['bmi']}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 — 데이터 탐색
# ════════════════════════════════════════════════════════════
with tab2:
    # 요약 지표
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("전체 샘플", f"{len(df):,}명", "#2563EB"),
        ("피처 수",   "3개",             "#10B981"),
        ("클래스 수", "6단계",           "#F97316"),
        ("결측치",    "없음 ✓",          "#6B7280"),
    ]
    for col, (label, value, color) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # 차트 행 1
    c1, c2 = st.columns(2)

    with c1:
        # 클래스 분포
        counts = df["Index"].value_counts().sort_index()
        labels = [INDEX_INFO[i]["name"] for i in counts.index]
        colors = [INDEX_INFO[i]["color"] for i in counts.index]
        fig = go.Figure(go.Bar(
            x=labels, y=counts.values,
            marker_color=colors,
            text=[f"{v}명<br>({v/len(df)*100:.1f}%)" for v in counts.values],
            textposition="outside",
        ))
        fig.update_layout(
            title="비만 단계 분포", yaxis_title="샘플 수",
            yaxis_range=[0, 230], height=360,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="white", plot_bgcolor="#F9FAFB",
            font_color="#374151", showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # 성별 도넛
        gc = df["Gender"].value_counts()
        fig = go.Figure(go.Pie(
            labels=gc.index, values=gc.values,
            hole=0.55,
            marker_colors=["#2563EB", "#F43F5E"],
            textinfo="label+percent",
            textfont_size=14,
        ))
        fig.update_layout(
            title="성별 분포", height=360,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="white", font_color="#374151",
        )
        st.plotly_chart(fig, use_container_width=True)

    # 차트 행 2
    c3, c4 = st.columns(2)

    with c3:
        # Height 박스플롯 by Index
        fig = go.Figure()
        for i in range(6):
            fig.add_trace(go.Box(
                y=df[df["Index"]==i]["Height"],
                name=INDEX_INFO[i]["name"],
                marker_color=INDEX_INFO[i]["color"],
                boxmean=True,
            ))
        fig.update_layout(
            title="Index별 Height 분포", yaxis_title="Height (cm)",
            height=380, showlegend=False,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="white", plot_bgcolor="#F9FAFB", font_color="#374151",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # Weight 박스플롯 by Index
        fig = go.Figure()
        for i in range(6):
            fig.add_trace(go.Box(
                y=df[df["Index"]==i]["Weight"],
                name=INDEX_INFO[i]["name"],
                marker_color=INDEX_INFO[i]["color"],
                boxmean=True,
            ))
        fig.update_layout(
            title="Index별 Weight 분포", yaxis_title="Weight (kg)",
            height=380, showlegend=False,
            margin=dict(t=50, b=10, l=10, r=10),
            paper_bgcolor="white", plot_bgcolor="#F9FAFB", font_color="#374151",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Height vs Weight 산점도
    df_plot = df.copy()
    df_plot["비만단계"] = df_plot["Index"].map(lambda i: INDEX_INFO[i]["name"])
    color_map = {INDEX_INFO[i]["name"]: INDEX_INFO[i]["color"] for i in range(6)}
    fig = px.scatter(
        df_plot, x="Height", y="Weight", color="비만단계",
        color_discrete_map=color_map,
        symbol="Gender",
        opacity=0.7, size_max=8,
        title="Height vs Weight 산점도 (비만단계 · 성별 구분)",
        labels={"Height": "키 (cm)", "Weight": "몸무게 (kg)"},
        height=480,
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="#F9FAFB",
        font_color="#374151", legend_title="비만 단계",
        margin=dict(t=60, b=10, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # 원본 데이터 미리보기
    with st.expander("📋 원본 데이터 미리보기"):
        st.dataframe(df, use_container_width=True, height=320)


# ════════════════════════════════════════════════════════════
# TAB 3 — 모델 성능
# ════════════════════════════════════════════════════════════
with tab3:
    # 모델 성능 요약 지표
    st.markdown("### 최적 모델 성능 요약")
    ma, mb, mc, md = st.columns(4)
    perf = [
        ("알고리즘",      model_obj["model_name"], "#2563EB"),
        ("Test Accuracy", "91.0%",                 "#10B981"),
        ("Test F1 (macro)", f"{model_obj['test_f1_macro']:.3f}", "#F97316"),
        ("CV F1 (macro)",   f"{model_obj['cv_f1_macro']:.3f}",  "#8B5CF6"),
    ]
    for col, (label, value, color) in zip([ma, mb, mc, md], perf):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color};font-size:22px;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # 모델 비교 차트
    model_names  = ["Logistic\nRegression", "Decision\nTree", "Random\nForest",
                    "Gradient\nBoosting", "SVM\n(RBF)", "KNN"]
    test_f1      = [0.7601, 0.7522, 0.7685, 0.8007, 0.8918, 0.5886]
    cv_f1        = [0.7173, 0.8003, 0.8125, 0.7920, 0.8692, 0.7622]
    test_acc     = [0.8700, 0.8300, 0.8200, 0.8300, 0.9100, 0.8200]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Test F1 (macro)",    x=model_names, y=test_f1,
                         marker_color="#3B82F6", opacity=0.85))
    fig.add_trace(go.Bar(name="CV F1 (macro)",      x=model_names, y=cv_f1,
                         marker_color="#10B981", opacity=0.85))
    fig.add_trace(go.Bar(name="Test Accuracy",      x=model_names, y=test_acc,
                         marker_color="#F97316", opacity=0.85))
    fig.add_hline(y=0.8, line_dash="dash", line_color="#6B7280",
                  annotation_text="기준선 0.8", annotation_position="top right")
    fig.update_layout(
        barmode="group",
        title="6개 모델 성능 비교",
        yaxis_title="Score", yaxis_range=[0, 1.05],
        height=420,
        margin=dict(t=60, b=10, l=10, r=10),
        paper_bgcolor="white", plot_bgcolor="#F9FAFB",
        font_color="#374151", legend=dict(orientation="h", y=1.08),
    )
    st.plotly_chart(fig, use_container_width=True)

    # 클래스별 성능
    st.markdown("### 클래스별 정밀도 / 재현율 / F1")
    class_names = ["Extremely Weak","Weak","Normal","Overweight","Obesity","Extreme Obesity"]
    precision   = [1.00, 0.67, 0.91, 0.81, 0.92, 0.97]
    recall      = [1.00, 1.00, 0.71, 0.93, 0.92, 0.95]
    f1_scores   = [1.00, 0.80, 0.80, 0.87, 0.92, 0.96]
    support     = [3, 4, 14, 14, 26, 39]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Precision", x=class_names, y=precision,
                         marker_color="#3B82F6", opacity=0.85))
    fig.add_trace(go.Bar(name="Recall",    x=class_names, y=recall,
                         marker_color="#10B981", opacity=0.85))
    fig.add_trace(go.Bar(name="F1",        x=class_names, y=f1_scores,
                         marker_color="#F97316", opacity=0.85))
    fig.update_layout(
        barmode="group",
        yaxis_title="Score", yaxis_range=[0, 1.15],
        height=380,
        margin=dict(t=20, b=10, l=10, r=10),
        paper_bgcolor="white", plot_bgcolor="#F9FAFB",
        font_color="#374151", legend=dict(orientation="h", y=1.05),
    )
    st.plotly_chart(fig, use_container_width=True)

    # 저장된 PNG 이미지 표시
    st.markdown("### 분석 차트 갤러리")
    import os
    png_files = sorted([f for f in os.listdir("output") if f.endswith(".png")])
    titles = {
        "01_eda_distribution.png": "EDA — 기본 분포",
        "02_eda_boxplot.png":      "EDA — Index별 박스플롯",
        "03_eda_scatter.png":      "EDA — 산점도",
        "04_model_comparison.png": "모델 성능 비교",
        "05_cv_scores.png":        "5-Fold CV 분포",
        "06_confusion_matrix.png": "Confusion Matrix",
        "07_class_metrics.png":    "클래스별 지표",
        "08_feature_importance.png":"피처 중요도",
        "09_learning_curve.png":   "학습 곡선",
    }
    for i in range(0, len(png_files), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(png_files):
                fname = png_files[i + j]
                with col:
                    st.markdown(f"**{titles.get(fname, fname)}**")
                    st.image(f"output/{fname}", use_container_width=True)
