"""고객 이탈 위험 예측기 — Streamlit 앱"""
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st
from pathlib import Path

# ── 한글 폰트 설정 ──────────────────────────────────────────────────────────
font_path = r'C:\Windows\Fonts\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ── 모델 로드 ──────────────────────────────────────────────────────────────
MODEL_PATH = Path(__file__).parent.parent / '09_ML_Pipeline' / 'output' / 'churn_model.pkl'

@st.cache_resource
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

# 파이프라인 입력 전 파생 피처 생성 (ml_pipeline.py와 동일한 로직)
def add_behavioral_features(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    X['spend_per_product']      = X['monthly_spend'] / X['num_products']
    X['support_rate']           = X['num_support_tickets'] / (X['tenure_months'] + 1)
    X['relative_inactivity']    = X['last_login_days_ago'] / (X['tenure_months'] + 1)
    X['age_tenure_interaction'] = X['age'] * X['tenure_months']
    X['engagement_score']       = X['num_products'] / (X['last_login_days_ago'] + 1)
    X['lifetime_value_proxy']   = X['tenure_months'] * X['monthly_spend']
    return X

# ── 페이지 설정 ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="고객 이탈 위험 예측기",
    page_icon="📊",
    layout="wide"
)

# ── 사이드바: 사용 안내 ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("📘 사용 방법")
    st.markdown("""
    **단계별 안내:**

    1. 오른쪽 슬라이더와 드롭다운으로 고객 정보를 입력하세요
    2. **이탈 위험 예측** 버튼을 클릭하세요
    3. 위험 수준과 이탈 확률을 확인하세요
    4. **주요 영향 요인 Top 5** 차트에서 예측 근거를 확인하세요

    ---

    **위험 수준 기준:**
    - 🟢 **저위험** — 이탈 확률 50% 미만
    - 🔴 **고위험** — 이탈 확률 50% 이상

    ---

    **피처 설명:**

    | 피처 | 설명 |
    |------|------|
    | 나이 | 고객 나이 (세) |
    | 가입 기간 | 서비스 이용 기간 (개월) |
    | 월 지출 | 평균 월 결제 금액 ($) |
    | 상품 수 | 구독 중인 상품 수 |
    | 문의 건수 | 누적 고객 지원 요청 횟수 |
    | 마지막 로그인 | 마지막 로그인 후 경과 일수 |
    | 결제 수단 | 주요 결제 방법 |
    | 지역 | 고객 소재 지역 |

    ---
    *모델: 행동 데이터 기반 로지스틱 회귀*
    """)

# ── 메인 헤더 ───────────────────────────────────────────────────────────────
st.title("📊 고객 이탈 위험 예측기")
st.markdown(
    "고객 정보를 입력하면 이탈 가능성을 예측합니다. "
    "모델은 **지출 패턴, 서비스 참여도, 고객 지원 이력** 등 행동 데이터를 분석하여 이탈 위험도를 산출합니다."
)
st.divider()

# ── 입력 폼 ────────────────────────────────────────────────────────────────
st.subheader("🧑 고객 프로필 입력")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**인구통계**")
    age = st.slider("나이", min_value=18, max_value=80, value=35, step=1)
    tenure_months = st.slider("가입 기간 (개월)", min_value=1, max_value=72, value=24, step=1)

with col2:
    st.markdown("**이용 현황**")
    monthly_spend = st.slider("월 지출 ($)", min_value=40, max_value=500, value=200, step=5)
    num_products = st.slider("상품 수", min_value=1, max_value=8, value=3, step=1)
    num_support_tickets = st.slider("고객 지원 문의 건수", min_value=0, max_value=15, value=2, step=1)
    last_login_days_ago = st.slider("마지막 로그인 후 경과 일수", min_value=1, max_value=90, value=10, step=1)

with col3:
    st.markdown("**계정 정보**")
    payment_method = st.selectbox(
        "결제 수단",
        options=["Bank Transfer", "Credit Card", "PayPal"]
    )
    region = st.selectbox(
        "지역",
        options=["East", "North", "South", "West"]
    )

st.divider()

# ── 예측 버튼 ───────────────────────────────────────────────────────────────
predict_clicked = st.button("🔍 이탈 위험 예측", type="primary", use_container_width=True)

if predict_clicked:
    model = load_model()

    # 원본 입력 → 파생 피처 추가 → 파이프라인 예측
    raw_input = pd.DataFrame([{
        'age':                  age,
        'tenure_months':        tenure_months,
        'monthly_spend':        monthly_spend,
        'num_products':         num_products,
        'num_support_tickets':  num_support_tickets,
        'last_login_days_ago':  last_login_days_ago,
        'payment_method':       payment_method,
        'region':               region
    }])
    X_input = add_behavioral_features(raw_input)

    churn_prob   = model.predict_proba(X_input)[0][1]
    is_high_risk = churn_prob >= 0.5

    st.subheader("📋 예측 결과")
    res_col1, res_col2 = st.columns([1, 1])

    # 결과 카드
    with res_col1:
        if is_high_risk:
            st.markdown(f"""
            <div style="background:#ffe0e0; padding:24px; border-radius:12px;
                        border-left:6px solid #e53935; text-align:center;">
                <h1 style="color:#e53935; margin:0;">⚠️ 고위험</h1>
                <h2 style="color:#c62828; margin:8px 0 0 0;">
                    이탈 확률: {churn_prob:.1%}
                </h2>
                <p style="color:#555; margin-top:10px;">
                    이 고객은 강한 이탈 신호를 보이고 있습니다.<br>
                    즉각적인 고객 유지 조치가 필요합니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#e0f5e9; padding:24px; border-radius:12px;
                        border-left:6px solid #2e7d32; text-align:center;">
                <h1 style="color:#2e7d32; margin:0;">✅ 저위험</h1>
                <h2 style="color:#1b5e20; margin:8px 0 0 0;">
                    이탈 확률: {churn_prob:.1%}
                </h2>
                <p style="color:#555; margin-top:10px;">
                    이 고객은 안정적인 상태입니다.<br>
                    표준 참여 전략을 유지하세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 확률 게이지
    with res_col2:
        st.markdown("**이탈 위험 확률 게이지**")
        fig_gauge, ax = plt.subplots(figsize=(5, 1.2))
        ax.barh([''], [1], color='#e0e0e0', height=0.5)
        bar_color = '#e53935' if is_high_risk else '#2e7d32'
        ax.barh([''], [churn_prob], color=bar_color, height=0.5)
        ax.axvline(0.5, color='#888', linewidth=1.5, linestyle='--')
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax.set_yticks([])
        ax.set_title(f'이탈 확률: {churn_prob:.1%}', fontsize=11, pad=8)
        ax.spines[['top', 'right', 'left']].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig_gauge)
        plt.close()

        # 요약 지표
        st.markdown(f"""
        | 지표 | 값 |
        |------|----|
        | 이탈 확률 | **{churn_prob:.1%}** |
        | 유지 확률 | **{1-churn_prob:.1%}** |
        | 위험 수준 | **{'고위험 ⚠️' if is_high_risk else '저위험 ✅'}** |
        """)

    st.divider()

    # ── 피처 기여도 Top 5 ───────────────────────────────────────────────────
    st.subheader("🔍 예측에 영향을 준 주요 요인 Top 5")

    prep_step  = model.named_steps['prep']
    model_step = model.named_steps['model']

    num_cols_model = prep_step.transformers[0][2]
    cat_cols_model = prep_step.transformers[1][2]
    ohe_feat = prep_step.named_transformers_['cat']['encoder'] \
               .get_feature_names_out(cat_cols_model).tolist()
    all_feat_names = list(num_cols_model) + ohe_feat

    X_transformed = prep_step.transform(X_input)

    # 로지스틱 회귀: coef × 변환값 → 각 피처의 예측 기여도
    if hasattr(model_step, 'coef_'):
        contributions = np.abs(model_step.coef_[0] * X_transformed[0])
    elif hasattr(model_step, 'feature_importances_'):
        contributions = model_step.feature_importances_
    else:
        contributions = np.ones(len(all_feat_names))

    contrib_df = (pd.DataFrame({'피처': all_feat_names, '기여도': contributions})
                  .nlargest(5, '기여도'))

    # 사람이 읽기 쉬운 피처 이름으로 변환
    rename_map = {
        'age': '나이', 'tenure_months': '가입 기간 (개월)',
        'monthly_spend': '월 지출', 'num_products': '상품 수',
        'num_support_tickets': '고객 지원 문의', 'last_login_days_ago': '마지막 로그인 경과일',
        'spend_per_product': '상품당 지출', 'support_rate': '지원 문의 비율',
        'relative_inactivity': '상대적 비활성도', 'age_tenure_interaction': '나이 × 가입기간',
        'engagement_score': '참여 점수', 'lifetime_value_proxy': '예상 생애 가치',
    }
    contrib_df['피처'] = contrib_df['피처'].apply(
        lambda x: rename_map.get(x, x.replace('_', ' ').title())
    )

    fig_imp, ax = plt.subplots(figsize=(8, 3.5))
    bar_color = '#e53935' if is_high_risk else '#2e7d32'
    ax.barh(contrib_df['피처'], contrib_df['기여도'], color=bar_color, alpha=0.82)
    ax.set_xlabel('예측 기여도')
    ax.set_title('주요 영향 요인 Top 5', fontsize=12, pad=10)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig_imp)
    plt.close()

    # 피처 기여도 설명 텍스트
    top_factor = contrib_df.iloc[0]['피처']
    st.info(
        f"💡 **{top_factor}** 이(가) 이 고객의 이탈 위험에 가장 큰 영향을 미치고 있습니다. "
        f"고객 유지 전략 수립 시 이 지표를 우선적으로 검토하세요."
    )
