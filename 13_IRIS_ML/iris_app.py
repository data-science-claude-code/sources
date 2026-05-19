"""
IRIS 분류 예측 Streamlit 앱
저장된 모델로 실시간 붓꽃 종 예측
"""
import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 한글 폰트
font_prop = fm.FontProperties(fname=r'C:\Windows\Fonts\malgun.ttf')
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'workflows', 'iris_model.pkl')

st.set_page_config(page_title='IRIS 분류 예측기', page_icon='🌸', layout='wide')

@st.cache_resource
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

# ── 사이드바 입력 ──────────────────────────────────────
st.sidebar.header('🌸 붓꽃 측정값 입력')

sepal_length = st.sidebar.slider('꽃받침 길이 (cm)', 4.0, 8.0, 5.8, 0.1)
sepal_width  = st.sidebar.slider('꽃받침 너비 (cm)', 2.0, 4.5, 3.0, 0.1)
petal_length = st.sidebar.slider('꽃잎 길이 (cm)',   1.0, 7.0, 4.0, 0.1)
petal_width  = st.sidebar.slider('꽃잎 너비 (cm)',   0.1, 2.5, 1.2, 0.1)

# ── 메인 화면 ──────────────────────────────────────────
st.title('🌸 IRIS 붓꽃 종 분류 예측기')
st.markdown('측정값을 입력하면 AI가 붓꽃의 종을 예측합니다.')

col1, col2, col3, col4 = st.columns(4)
col1.metric('꽃받침 길이', f'{sepal_length} cm')
col2.metric('꽃받침 너비', f'{sepal_width} cm')
col3.metric('꽃잎 길이',   f'{petal_length} cm')
col4.metric('꽃잎 너비',   f'{petal_width} cm')

st.divider()

# ── 예측 ──────────────────────────────────────────────
try:
    bundle = load_model()
    model  = bundle['model']
    scaler = bundle['scaler']
    le     = bundle['label_encoder']

    X_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    X_scaled = scaler.transform(X_input)
    pred_idx  = model.predict(X_scaled)[0]
    pred_prob = model.predict_proba(X_scaled)[0]
    pred_name = le.inverse_transform([pred_idx])[0]
    species_short = pred_name.replace('Iris-', '')

    # 결과 표시
    species_emoji = {'setosa': '🔵', 'versicolor': '🟠', 'virginica': '🟢'}
    emoji = species_emoji.get(species_short, '🌸')

    st.subheader('예측 결과')
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.markdown(f'## {emoji} **{species_short.capitalize()}**')
        st.markdown(f'*{pred_name}*')
        confidence = pred_prob[pred_idx] * 100
        st.metric('신뢰도', f'{confidence:.1f}%')

    with res_col2:
        # 확률 막대 차트
        fig, ax = plt.subplots(figsize=(6, 3))
        class_names = [c.replace('Iris-', '') for c in le.classes_]
        colors_bar = ['#4C72B0', '#DD8452', '#55A868']
        bars = ax.barh(class_names, pred_prob * 100, color=colors_bar, alpha=0.85)
        ax.set_xlabel('확률 (%)', fontsize=11)
        ax.set_title('클래스별 예측 확률', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 100)
        for bar, prob in zip(bars, pred_prob):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                    f'{prob*100:.1f}%', va='center', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

    # 종 설명
    st.divider()
    st.subheader('🔍 종 특성 정보')
    info = {
        'setosa':     '꽃잎이 매우 작고 짧음. 가장 쉽게 구분되는 종.',
        'versicolor': '중간 크기의 꽃잎. 세 종 중 가장 흔한 종.',
        'virginica':  '꽃잎이 가장 크고 김. 꽃받침도 비교적 큰 편.',
    }
    for sp, desc in info.items():
        emoji_sp = species_emoji.get(sp, '')
        if sp == species_short:
            st.success(f'{emoji_sp} **{sp.capitalize()}** ← 예측된 종: {desc}')
        else:
            st.info(f'{emoji_sp} **{sp.capitalize()}**: {desc}')

except FileNotFoundError:
    st.error('모델 파일을 찾을 수 없습니다. 먼저 iris_analysis.ipynb를 실행해 주세요.')
