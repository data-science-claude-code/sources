import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic 생존 예측",
    page_icon="🚢",
    layout="centered",
)

# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 배경 */
.stApp { background-color: #f0f4f8; color: #1e293b; }

/* 헤더 */
.hero {
    background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
    border: 1px solid #bfdbfe;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero h1 { font-size: 2.4rem; margin: 0; color: #1e40af; }
.hero p  { color: #64748b; margin: 0.4rem 0 0; font-size: 1rem; }

/* 카드 */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.card-title {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.8rem;
}

/* 결과 박스 */
.result-survived {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border: 1px solid #10b981;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
}
.result-dead {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border: 1px solid #ef4444;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
}
.result-title { font-size: 1.8rem; font-weight: 700; margin: 0; color: #1e293b; }
.result-sub   { color: #475569; font-size: 0.95rem; margin-top: 0.3rem; }

/* 확률 바 */
.prob-bar-bg {
    background: #e2e8f0;
    border-radius: 999px;
    height: 12px;
    margin: 0.4rem 0 1rem;
    overflow: hidden;
}
.prob-bar-fill-green {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #10b981, #34d399);
    transition: width 0.5s ease;
}
.prob-bar-fill-red {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ef4444, #f87171);
    transition: width 0.5s ease;
}

/* 입력 레이블 */
label { color: #374151 !important; font-size: 0.9rem !important; }

/* 버튼 */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

/* 구분선 */
hr { border-color: #e2e8f0; }

/* selectbox, slider 배경 */
.stSelectbox > div > div,
.stSlider { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── 모델 로드 ────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load(
        r"G:\내 드라이브\강의자료\Vibe_Coding\Datascience\Test\12_Titanic_ML\output\titanic_model.pkl"
    )

model = load_model()

# 한글 폰트 설정
font_path = r"C:\Windows\Fonts\malgun.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🚢 Titanic 생존 예측</h1>
  <p>승객 정보를 입력하면 AI가 생존 확률을 예측합니다</p>
</div>
""", unsafe_allow_html=True)

# ── 입력 폼 ──────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">👤 승객 정보 입력</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    pclass = st.selectbox(
        "객실 등급",
        options=[1, 2, 3],
        format_func=lambda x: {1: "1등급 — 상위 클래스", 2: "2등급 — 중간 클래스", 3: "3등급 — 일반 클래스"}[x],
    )
    sex = st.selectbox(
        "성별",
        options=["여성", "남성"],
    )
    age = st.slider("나이", min_value=1, max_value=80, value=30, step=1)
    embarked = st.selectbox(
        "탑승 항구",
        options=["Southampton (S)", "Cherbourg (C)", "Queenstown (Q)"],
    )

with col2:
    sibsp = st.slider("형제/배우자 수", min_value=0, max_value=8, value=0, step=1)
    parch = st.slider("부모/자녀 수", min_value=0, max_value=6, value=0, step=1)
    fare = st.slider("티켓 요금 ($)", min_value=0, max_value=500, value=30, step=1)

    # 가족 요약 표시
    family_size = sibsp + parch + 1
    alone = "혼자 탑승" if family_size == 1 else f"가족 {family_size}명"
    st.markdown(f"""
    <div style="margin-top:1rem; padding:0.8rem 1rem;
         background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0;">
      <span style="color:#94a3b8; font-size:0.8rem;">동반 인원</span><br>
      <span style="font-size:1.1rem; font-weight:600; color:#1e293b;">{alone}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── 예측 버튼 ────────────────────────────────────────────────
predict_btn = st.button("🔍 생존 확률 예측하기")

if predict_btn:
    # 입력값 변환
    sex_enc = 0 if sex == "여성" else 1
    embarked_enc = {"Southampton (S)": 2, "Cherbourg (C)": 0, "Queenstown (Q)": 1}[embarked]

    input_df = pd.DataFrame([{
        "Pclass": pclass,
        "Sex": sex_enc,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
        "Embarked": embarked_enc,
    }])

    proba = model.predict_proba(input_df)[0]
    survive_prob = proba[1]
    dead_prob    = proba[0]
    survived     = survive_prob >= 0.5

    # ── 결과 카드 ──
    st.markdown("<hr>", unsafe_allow_html=True)

    if survived:
        st.markdown(f"""
        <div class="result-survived">
          <div class="result-title">✅ 생존 예측</div>
          <div class="result-sub">이 승객은 생존했을 가능성이 높습니다</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-dead">
          <div class="result-title">❌ 사망 예측</div>
          <div class="result-sub">이 승객은 생존하지 못했을 가능성이 높습니다</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 확률 바 ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
        <div style="color:#059669; font-weight:600;">생존 확률</div>
        <div class="prob-bar-bg">
          <div class="prob-bar-fill-green" style="width:{survive_prob*100:.1f}%"></div>
        </div>
        <div style="font-size:1.6rem; font-weight:700; color:#059669;">{survive_prob*100:.1f}%</div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div style="color:#dc2626; font-weight:600;">사망 확률</div>
        <div class="prob-bar-bg">
          <div class="prob-bar-fill-red" style="width:{dead_prob*100:.1f}%"></div>
        </div>
        <div style="font-size:1.6rem; font-weight:700; color:#dc2626;">{dead_prob*100:.1f}%</div>
        """, unsafe_allow_html=True)

    # ── 특성 중요도 차트 ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">📊 특성 중요도 (모델 기준)</div>', unsafe_allow_html=True)

    feature_names = ["객실 등급", "성별", "나이", "형제/배우자", "부모/자녀", "요금", "탑승 항구"]
    importances   = model.feature_importances_
    sorted_idx    = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    colors = ["#93c5fd" if i != sorted_idx[-1] else "#2563eb" for i in sorted_idx]
    bars = ax.barh(
        [feature_names[i] for i in sorted_idx],
        importances[sorted_idx],
        color=colors, edgecolor="none", height=0.6
    )
    for bar, val in zip(bars, importances[sorted_idx]):
        ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", color="#475569", fontsize=9)

    ax.set_xlabel("중요도", color="#94a3b8", fontsize=9)
    ax.tick_params(colors="#475569", labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.label.set_color("#94a3b8")
    ax.grid(axis="x", color="#e2e8f0", linewidth=0.5)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── 입력 요약 ──
    with st.expander("📋 입력 요약 보기"):
        summary = {
            "객실 등급": f"{pclass}등급",
            "성별": sex,
            "나이": f"{age}세",
            "탑승 항구": embarked,
            "형제/배우자 수": sibsp,
            "부모/자녀 수": parch,
            "티켓 요금": f"${fare}",
            "동반 인원": alone,
        }
        for k, v in summary.items():
            st.markdown(f"**{k}**: {v}")

# ── 푸터 ─────────────────────────────────────────────────────
st.markdown("""
<br>
<div style="text-align:center; color:#94a3b8; font-size:0.8rem;">
  Random Forest · GridSearchCV 최적화 모델 · Titanic Dataset
</div>
""", unsafe_allow_html=True)
