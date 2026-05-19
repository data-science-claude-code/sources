import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

warnings.filterwarnings('ignore')

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="IRIS 붓꽃 분류기",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 한글 폰트 설정 (matplotlib) ───────────────────────────────
@st.cache_resource
def get_font():
    font_path = r"C:\Windows\Fonts\malgun.ttf"
    if Path(font_path).exists():
        fp = fm.FontProperties(fname=font_path)
        plt.rcParams["font.family"] = fp.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    return fm.FontProperties(fname=font_path) if Path(font_path).exists() else None

font_prop = get_font()

def fp(size=10):
    """폰트 프로퍼티 헬퍼"""
    if font_prop:
        return fm.FontProperties(fname=r"C:\Windows\Fonts\malgun.ttf", size=size)
    return None

# ── 데이터 로드 & 모델 학습 (캐시) ───────────────────────────
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "iris.csv"
    return pd.read_csv(data_path)

@st.cache_resource
def train_models(df):
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X = df[features].values
    le = LabelEncoder()
    y = le.fit_transform(df["species"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    model_defs = {
        "로지스틱 회귀":     (LogisticRegression(max_iter=200, random_state=42), True),
        "KNN (k=5)":        (KNeighborsClassifier(n_neighbors=5), True),
        "SVM (RBF)":        (SVC(kernel="rbf", probability=True, random_state=42), True),
        "결정 트리":         (DecisionTreeClassifier(random_state=42), False),
        "랜덤 포레스트":     (RandomForestClassifier(n_estimators=100, random_state=42), False),
        "그래디언트 부스팅": (GradientBoostingClassifier(n_estimators=100, random_state=42), False),
    }

    trained, test_scores, cv_scores = {}, {}, {}
    for name, (model, use_sc) in model_defs.items():
        Xtr = X_train_sc if use_sc else X_train
        Xte = X_test_sc  if use_sc else X_test
        model.fit(Xtr, y_train)
        test_scores[name] = accuracy_score(y_test, model.predict(Xte))
        cv_scores[name]   = cross_val_score(model, Xtr, y_train, cv=5).mean()
        trained[name]     = (model, use_sc)

    return trained, scaler, le, test_scores, cv_scores, X_train, X_test, y_train, y_test

# ── 상수 ─────────────────────────────────────────────────────
FEATURES    = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
LABELS_KO   = ["꽃받침 길이", "꽃받침 너비", "꽃잎 길이", "꽃잎 너비"]
SPECIES_KO  = {"Iris-setosa": "세토사", "Iris-versicolor": "버시컬러", "Iris-virginica": "버지니카"}
SPECIES_EMO = {"Iris-setosa": "🌷", "Iris-versicolor": "🌺", "Iris-virginica": "🌸"}
COLORS      = ["#4C72B0", "#55A868", "#C44E52"]
SPECIES_ALL = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

# ── 데이터 & 모델 준비 ────────────────────────────────────────
df = load_data()
models, scaler, le, test_scores, cv_scores, X_train, X_test, y_train, y_test = train_models(df)

# ══════════════════════════════════════════════════════════════
#  사이드바
# ══════════════════════════════════════════════════════════════
st.sidebar.title("🌸 IRIS 분류기")
st.sidebar.markdown("꽃 크기를 입력하면 AI가 품종을 예측합니다.")
st.sidebar.divider()

# 모델 선택
st.sidebar.subheader("⚙️ 모델 선택")
selected = st.sidebar.selectbox(
    "예측 모델",
    list(models.keys()),
    index=2,
    help="테스트 정확도가 가장 높은 모델을 추천합니다",
)
best_model_name = max(test_scores, key=test_scores.get)
st.sidebar.caption(
    f"✅ 정확도 `{test_scores[selected]:.1%}` "
    f"| CV `{cv_scores[selected]:.1%}`"
)

st.sidebar.divider()

# 슬라이더 입력
st.sidebar.subheader("📏 꽃 크기 입력 (cm)")

def make_slider(label, col):
    lo  = float(df[col].min())
    hi  = float(df[col].max())
    avg = float(df[col].mean())
    return st.sidebar.slider(label, lo, hi, avg, 0.1, format="%.1f cm")

sl = make_slider("꽃받침 길이", "sepal_length")
sw = make_slider("꽃받침 너비", "sepal_width")
pl = make_slider("꽃잎 길이",   "petal_length")
pw = make_slider("꽃잎 너비",   "petal_width")

input_arr = np.array([[sl, sw, pl, pw]])

# ── 예측 ─────────────────────────────────────────────────────
model, use_sc = models[selected]
X_pred   = scaler.transform(input_arr) if use_sc else input_arr
pred_idx = int(model.predict(X_pred)[0])
pred_sp  = le.inverse_transform([pred_idx])[0]
proba    = model.predict_proba(X_pred)[0]
confidence = proba[pred_idx]

# ══════════════════════════════════════════════════════════════
#  메인 영역
# ══════════════════════════════════════════════════════════════
st.title("🌸 IRIS 붓꽃 품종 분류기")
st.caption("Iris Dataset · 6가지 머신러닝 모델 비교")
st.divider()

# ── 결과 카드 ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("예측 품종", f"{SPECIES_EMO[pred_sp]} {SPECIES_KO[pred_sp]}")
c2.metric("신뢰도", f"{confidence:.1%}")
c3.metric("사용 모델", selected)
c4.metric("테스트 정확도", f"{test_scores[selected]:.1%}")

st.divider()

# ── 상단 2열: 확률 막대 + 산점도 ────────────────────────────
col_left, col_right = st.columns([1, 1])

# 확률 막대
with col_left:
    st.subheader("📊 품종별 예측 확률")
    species_ko_list = ["세토사 🌷", "버시컬러 🌺", "버지니카 🌸"]
    bar_colors = [
        "#E74C3C" if i == pred_idx else COLORS[i]
        for i in range(3)
    ]

    fig1, ax1 = plt.subplots(figsize=(5, 2.8))
    bars = ax1.barh(species_ko_list, proba, color=bar_colors, height=0.45, edgecolor="white")
    ax1.set_xlim(0, 1.12)
    ax1.axvline(0.5, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    for bar, val in zip(bars, proba):
        ax1.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1%}", va="center", fontsize=11, fontweight="bold",
                 **({"fontproperties": fp(11)} if fp() else {}))
    ax1.set_xlabel("확률", **({"fontproperties": fp(10)} if fp() else {}))
    ax1.set_yticklabels(species_ko_list, **({"fontproperties": fp(11)} if fp() else {}))
    ax1.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig1)

# 꽃잎 기준 산점도
with col_right:
    st.subheader("📍 꽃잎 기준 위치")

    fig2, ax2 = plt.subplots(figsize=(5, 2.8))
    for sp, color in zip(SPECIES_ALL, COLORS):
        sub = df[df["species"] == sp]
        ax2.scatter(sub["petal_length"], sub["petal_width"],
                    c=color, label=SPECIES_KO[sp], alpha=0.55, s=35, edgecolors="none")

    ax2.scatter(pl, pw, c="red", s=220, marker="*",
                zorder=10, label="입력값", edgecolors="darkred", linewidths=0.8)
    ax2.set_xlabel("꽃잎 길이 (cm)", **({"fontproperties": fp(10)} if fp() else {}))
    ax2.set_ylabel("꽃잎 너비 (cm)", **({"fontproperties": fp(10)} if fp() else {}))
    legend = ax2.legend(fontsize=8, framealpha=0.7)
    if fp():
        for text in legend.get_texts():
            text.set_fontproperties(fp(8))
    ax2.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# ── 하단 2열: 특성 비교 + 꽃받침 산점도 ──────────────────────
col_a, col_b = st.columns([1, 1])

# 품종 평균과 입력값 비교
with col_a:
    st.subheader("📏 품종 평균과 내 입력값 비교")
    species_mean = df.groupby("species")[FEATURES].mean()
    input_vals   = [sl, sw, pl, pw]
    x = np.arange(len(FEATURES))
    width = 0.2

    fig3, ax3 = plt.subplots(figsize=(5, 3.2))
    for i, (sp, color) in enumerate(zip(SPECIES_ALL, COLORS)):
        ax3.bar(x + (i - 1) * width, species_mean.loc[sp], width=width,
                color=color, alpha=0.65, label=SPECIES_KO[sp])

    ax3.plot(x, input_vals, "r*-", markersize=13, linewidth=1.5,
             label="내 입력값", zorder=5)

    ax3.set_xticks(x)
    xt_labels = ["꽃받침\n길이", "꽃받침\n너비", "꽃잎\n길이", "꽃잎\n너비"]
    ax3.set_xticklabels(xt_labels, fontsize=9,
                        **({"fontproperties": fp(9)} if fp() else {}))
    ax3.set_ylabel("크기 (cm)", **({"fontproperties": fp(10)} if fp() else {}))
    legend3 = ax3.legend(fontsize=8, loc="upper left")
    if fp():
        for text in legend3.get_texts():
            text.set_fontproperties(fp(8))
    ax3.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig3)

# 꽃받침 기준 산점도
with col_b:
    st.subheader("📍 꽃받침 기준 위치")

    fig4, ax4 = plt.subplots(figsize=(5, 3.2))
    for sp, color in zip(SPECIES_ALL, COLORS):
        sub = df[df["species"] == sp]
        ax4.scatter(sub["sepal_length"], sub["sepal_width"],
                    c=color, label=SPECIES_KO[sp], alpha=0.55, s=35, edgecolors="none")

    ax4.scatter(sl, sw, c="red", s=220, marker="*",
                zorder=10, label="입력값", edgecolors="darkred", linewidths=0.8)
    ax4.set_xlabel("꽃받침 길이 (cm)", **({"fontproperties": fp(10)} if fp() else {}))
    ax4.set_ylabel("꽃받침 너비 (cm)", **({"fontproperties": fp(10)} if fp() else {}))
    legend4 = ax4.legend(fontsize=8)
    if fp():
        for text in legend4.get_texts():
            text.set_fontproperties(fp(8))
    ax4.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig4)

st.divider()

# ── 모델 성능 비교 (접기/펼치기) ─────────────────────────────
with st.expander("🔬 전체 모델 성능 비교", expanded=False):
    perf_df = pd.DataFrame({
        "모델": list(test_scores.keys()),
        "테스트 정확도": [f"{v:.1%}" for v in test_scores.values()],
        "CV 평균 정확도": [f"{v:.1%}" for v in cv_scores.values()],
    }).sort_values("테스트 정확도", ascending=False).reset_index(drop=True)
    perf_df.index += 1
    st.dataframe(perf_df, use_container_width=True)

# ── 입력값 요약 (접기/펼치기) ─────────────────────────────────
with st.expander("📋 현재 입력값 요약", expanded=False):
    summary = pd.DataFrame({
        "특성": LABELS_KO,
        "입력값 (cm)": [sl, sw, pl, pw],
        "전체 평균 (cm)": [round(df[f].mean(), 2) for f in FEATURES],
        f"{SPECIES_KO[pred_sp]} 평균 (cm)": [
            round(df[df["species"] == pred_sp][f].mean(), 2) for f in FEATURES
        ],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)

st.caption("IRIS Dataset · UCI Machine Learning Repository · Streamlit Demo")
