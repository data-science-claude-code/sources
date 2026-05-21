import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic 생존 예측",
    page_icon="🚢",
    layout="centered",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    .block-container { padding-top: 2rem; max-width: 720px; }

    .title-box {
        text-align: center;
        padding: 2rem 1rem 1.4rem;
        background: linear-gradient(135deg, #e8f0fe, #dce8ff);
        border-radius: 16px;
        border: 1px solid #c5d5f5;
        margin-bottom: 2rem;
    }
    .title-box h1 { font-size: 2.2rem; margin: 0; color: #1a237e; }
    .title-box p  { color: #5c6bc0; margin: 0.4rem 0 0; font-size: 0.95rem; }

    .section-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #7986cb;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .result-survived {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 1px solid #a5d6a7;
        border-radius: 16px;
        margin-top: 1.5rem;
    }
    .result-died {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #fce4ec, #fff3e0);
        border: 1px solid #ef9a9a;
        border-radius: 16px;
        margin-top: 1.5rem;
    }
    .result-emoji  { font-size: 3.5rem; margin-bottom: 0.4rem; }
    .result-title  { font-size: 1.6rem; font-weight: 700; margin: 0.2rem 0; }
    .result-sub    { font-size: 0.9rem; color: #78909c; margin-top: 0.3rem; }

    div[data-testid="stButton"] button {
        width: 100%;
        height: 3.2rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 10px;
        background: linear-gradient(135deg, #3f51b5, #1a237e);
        color: white;
        border: none;
        margin-top: 1rem;
        transition: opacity 0.2s;
    }
    div[data-testid="stButton"] button:hover { opacity: 0.88; }
</style>
""", unsafe_allow_html=True)

# ── 모델 로드 ─────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("titanic_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── 헤더 ──────────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>🚢 Titanic 생존 예측</h1>
    <p>승객 정보를 입력하면 AI가 생존 가능성을 예측합니다</p>
</div>
""", unsafe_allow_html=True)

# ── 입력 폼 ───────────────────────────────────────────────────
st.markdown('<p class="section-label">승객 기본 정보</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    pclass = st.selectbox("객실 등급", ["1등석", "2등석", "3등석"])
    pclass_val = int(pclass[0])
with col2:
    sex = st.radio("성별", ["여성", "남성"], horizontal=True)
    sex_val = 1 if sex == "남성" else 0
with col3:
    age = st.number_input("나이", min_value=0, max_value=100, value=30, step=1)

st.markdown('<p class="section-label" style="margin-top:1.2rem">동승자 및 요금</p>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    sibsp = st.slider("형제자매 / 배우자 수", 0, 8, 0)
with col5:
    parch = st.slider("부모 / 자녀 수", 0, 6, 0)
with col6:
    fare = st.number_input("운임 요금 ($)", min_value=0.0, max_value=600.0, value=32.0, step=0.5)

st.markdown('<p class="section-label" style="margin-top:1.2rem">탑승 항구</p>', unsafe_allow_html=True)
embarked = st.radio(
    "탑승 항구",
    ["Southampton (S)", "Cherbourg (C)", "Queenstown (Q)"],
    horizontal=True,
)
embarked_code = embarked.split("(")[1].rstrip(")")
embarked_q = 1 if embarked_code == "Q" else 0
embarked_s = 1 if embarked_code == "S" else 0

# ── 예측 ──────────────────────────────────────────────────────
if st.button("생존 가능성 예측하기"):
    input_data = pd.DataFrame([[pclass_val, sex_val, age, sibsp, parch, fare, embarked_q, embarked_s]],
                               columns=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked_Q", "Embarked_S"])

    prob = model.predict_proba(input_data)[0]
    survived_prob = prob[1]
    died_prob = prob[0]

    if survived_prob >= 0.5:
        st.markdown(f"""
        <div class="result-survived">
            <div class="result-emoji">✅</div>
            <div class="result-title" style="color:#2e7d32">생존 가능성 높음</div>
            <div class="result-sub">생존 확률 <strong style="color:#388e3c;font-size:1.3rem">{survived_prob:.1%}</strong></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-died">
            <div class="result-emoji">❌</div>
            <div class="result-title" style="color:#c62828">생존 가능성 낮음</div>
            <div class="result-sub">생존 확률 <strong style="color:#d32f2f;font-size:1.3rem">{survived_prob:.1%}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    # 확률 게이지
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("생존 확률", f"{survived_prob:.1%}")
        st.progress(float(survived_prob))
    with col_b:
        st.metric("사망 확률", f"{died_prob:.1%}")
        st.progress(float(died_prob))

    # 입력 요약
    with st.expander("입력 정보 확인"):
        summary = {
            "객실 등급": pclass,
            "성별": sex,
            "나이": f"{age}세",
            "형제자매/배우자": f"{sibsp}명",
            "부모/자녀": f"{parch}명",
            "운임 요금": f"${fare:.1f}",
            "탑승 항구": embarked,
        }
        st.table(pd.DataFrame(summary.items(), columns=["항목", "값"]).set_index("항목"))

# ── 푸터 ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.caption("모델: RandomForestClassifier (GridSearchCV 최적화) | 데이터: Titanic Dataset (891명)")
