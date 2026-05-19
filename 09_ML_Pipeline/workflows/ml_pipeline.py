"""
09_ML_Pipeline — 고객 이탈 예측 (데이터 누수 제거 버전)

[핵심 설계 원칙]
- 원본 raw 데이터 사용 (contract_type 제외 — 합성 데이터의 완벽한 예측자)
- 파생 피쳐 생성은 파이프라인 밖에서 적용 (pickle 복원 호환성 보장)
- 전처리(스케일링/인코딩)만 Pipeline에 포함
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import warnings
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, ConfusionMatrixDisplay
)
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

# 한글 폰트 설정
font_path = r'C:\Windows\Fonts\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

BASE = Path(__file__).parent.parent
RAW_DATA = BASE.parent / '07_Feature_Engineering' / 'resources' / 'customer_churn_raw.csv'
OUTPUT = BASE / 'output'
OUTPUT.mkdir(exist_ok=True)


def add_behavioral_features(X: pd.DataFrame) -> pd.DataFrame:
    """순수 행동 기반 파생 피쳐 생성 — 타겟(churned) 미참조"""
    X = X.copy()
    X['spend_per_product']     = X['monthly_spend'] / X['num_products']
    X['support_rate']          = X['num_support_tickets'] / (X['tenure_months'] + 1)
    X['relative_inactivity']   = X['last_login_days_ago'] / (X['tenure_months'] + 1)
    X['age_tenure_interaction']= X['age'] * X['tenure_months']
    X['engagement_score']      = X['num_products'] / (X['last_login_days_ago'] + 1)
    X['lifetime_value_proxy']  = X['tenure_months'] * X['monthly_spend']
    return X


# ──────────────────────────────────────────────
# 1. 데이터 로드 및 피쳐 선택
# ──────────────────────────────────────────────
print("=" * 55)
print("1. 데이터 로드 및 피쳐 선택")
print("=" * 55)

df = pd.read_csv(RAW_DATA)
print(f'원본 데이터: {df.shape}')

# contract_type 제외: 합성 데이터에서 Annual=0%, Monthly=100% 이탈 — 완벽한 예측자
X = df.drop(columns=['customer_id', 'churned', 'contract_type'])
y = df['churned']
print(f'입력 피쳐 ({len(X.columns)}개): {X.columns.tolist()}')
print(f'이탈 비율: {y.mean():.2%}')

# ──────────────────────────────────────────────
# 2. 학습/테스트 분할 → 파생 피쳐 생성
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("2. 분할 후 파생 피쳐 생성 (누수 방지)")
print("=" * 55)

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 분할 이후 파생 피쳐 적용 — 테스트 셋 정보가 학습에 영향 없음
X_train = add_behavioral_features(X_train_raw)
X_test  = add_behavioral_features(X_test_raw)

print(f'학습: {X_train.shape}  테스트: {X_test.shape}')
print(f'학습 이탈 비율: {y_train.mean():.2%}  테스트 이탈 비율: {y_test.mean():.2%}')

# ──────────────────────────────────────────────
# 3. 전처리 파이프라인 구성
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("3. 전처리 파이프라인 구성")
print("=" * 55)

num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()
print(f'수치형 {len(num_cols)}개: {num_cols}')
print(f'범주형 {len(cat_cols)}개: {cat_cols}')

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])
print('전처리 파이프라인 구성 완료')

# ──────────────────────────────────────────────
# 4. 모델 학습 및 평가
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("4. 모델 학습 및 평가 (5-겹 교차 검증 포함)")
print("=" * 55)

def evaluate_model(name, pipeline, X_tr, y_tr, X_te, y_te):
    """학습 → 5가지 지표 + 5-겹 CV AUC 반환"""
    pipeline.fit(X_tr, y_tr)
    y_pred = pipeline.predict(X_te)
    y_prob = pipeline.predict_proba(X_te)[:, 1]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_auc = cross_val_score(pipeline, X_tr, y_tr, cv=cv, scoring='roc_auc')
    return {
        'Model': name,
        'Accuracy':      accuracy_score(y_te, y_pred),
        'Precision':     precision_score(y_te, y_pred),
        'Recall':        recall_score(y_te, y_pred),
        'F1':            f1_score(y_te, y_pred),
        'AUC-ROC':       roc_auc_score(y_te, y_prob),
        'CV AUC (mean)': cv_auc.mean(),
        'CV AUC (std)':  cv_auc.std(),
        '_pipeline':     pipeline
    }

models = {
    '로지스틱 회귀': LogisticRegression(max_iter=1000, random_state=42),
    '랜덤 포레스트': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost':      XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
}

results, pipelines = [], {}
for name, model in models.items():
    pipe = Pipeline([('prep', preprocessor), ('model', model)])
    res  = evaluate_model(name, pipe, X_train, y_train, X_test, y_test)
    pipelines[name] = res.pop('_pipeline')
    results.append(res)
    print(f'{name}: Accuracy={res["Accuracy"]:.3f}, AUC={res["AUC-ROC"]:.3f}, '
          f'CV AUC={res["CV AUC (mean)"]:.3f}±{res["CV AUC (std)"]:.3f}')

results_df = pd.DataFrame(results).set_index('Model')
metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC-ROC']
print('\n모델 성능 비교:')
print(results_df[metrics].round(4).to_string())

# ──────────────────────────────────────────────
# 5. 최적 모델 GridSearchCV 튜닝
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("5. GridSearchCV 하이퍼파라미터 튜닝")
print("=" * 55)

best_name = results_df['AUC-ROC'].idxmax()
print(f'선택된 모델: {best_name} (AUC={results_df.loc[best_name, "AUC-ROC"]:.4f})')

param_grids = {
    '로지스틱 회귀': {'model__C': [0.01, 0.1, 1, 10], 'model__solver': ['lbfgs', 'liblinear']},
    '랜덤 포레스트': {'model__n_estimators': [100, 200], 'model__max_depth': [None, 5, 10],
                    'model__min_samples_split': [2, 5]},
    'XGBoost':      {'model__n_estimators': [100, 200], 'model__max_depth': [3, 5, 7],
                    'model__learning_rate': [0.05, 0.1, 0.2]}
}

grid_search = GridSearchCV(
    pipelines[best_name], param_grids[best_name],
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='roc_auc', n_jobs=-1, verbose=1
)
grid_search.fit(X_train, y_train)
print(f'\n최적 파라미터: {grid_search.best_params_}')
print(f'최적 CV AUC:   {grid_search.best_score_:.4f}')

best_tuned   = grid_search.best_estimator_
y_pred_best  = best_tuned.predict(X_test)
y_prob_best  = best_tuned.predict_proba(X_test)[:, 1]

print('\n=== 튜닝 후 최종 성능 ===')
for label, fn in [('Accuracy', accuracy_score), ('Precision', precision_score),
                  ('Recall', recall_score), ('F1', f1_score)]:
    print(f'{label:<10}: {fn(y_test, y_pred_best):.4f}')
print(f'{"AUC-ROC":<10}: {roc_auc_score(y_test, y_prob_best):.4f}')

# ──────────────────────────────────────────────
# 6. 혼동 행렬 & ROC 곡선
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("6. 혼동 행렬 & ROC 곡선 시각화")
print("=" * 55)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

cm = confusion_matrix(y_test, y_pred_best)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['유지', '이탈'])
disp.plot(ax=axes[0], colorbar=False, cmap='Blues')
axes[0].set_title(f'혼동 행렬 — {best_name} (튜닝)', fontproperties=font_prop)
axes[0].set_xlabel('예측값', fontproperties=font_prop)
axes[0].set_ylabel('실제값', fontproperties=font_prop)
for text in disp.text_.ravel():
    text.set_fontsize(14)

for name, pipe in pipelines.items():
    fpr, tpr, _ = roc_curve(y_test, pipe.predict_proba(X_test)[:, 1])
    auc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
    axes[1].plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})')
fpr_t, tpr_t, _ = roc_curve(y_test, y_prob_best)
axes[1].plot(fpr_t, tpr_t, 'k--',
             label=f'{best_name} 튜닝 (AUC={roc_auc_score(y_test, y_prob_best):.3f})')
axes[1].plot([0, 1], [0, 1], 'gray', linestyle=':', label='Random')
axes[1].set_xlabel('False Positive Rate', fontproperties=font_prop)
axes[1].set_ylabel('True Positive Rate', fontproperties=font_prop)
axes[1].set_title('ROC 곡선 비교', fontproperties=font_prop)
axes[1].legend(prop=font_prop, fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT / 'confusion_roc.png', dpi=150, bbox_inches='tight')
plt.close()
print('confusion_roc.png 저장 완료')

# ──────────────────────────────────────────────
# 7. 피쳐 중요도 Top 10
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("7. 피쳐 중요도 Top 10")
print("=" * 55)

prep_step  = best_tuned.named_steps['prep']
ohe_cols   = prep_step.named_transformers_['cat']['encoder'] \
             .get_feature_names_out(cat_cols).tolist()
feat_names = num_cols + ohe_cols

model_step = best_tuned.named_steps['model']
if hasattr(model_step, 'feature_importances_'):
    importances = model_step.feature_importances_
elif hasattr(model_step, 'coef_'):
    importances = np.abs(model_step.coef_[0])
else:
    importances = np.zeros(len(feat_names))

feat_df = (pd.DataFrame({'feature': feat_names, 'importance': importances})
           .nlargest(10, 'importance'))

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=feat_df, x='importance', y='feature', palette='viridis', ax=ax)
ax.set_title(f'피쳐 중요도 Top 10 — {best_name}', fontproperties=font_prop)
ax.set_xlabel('중요도', fontproperties=font_prop)
ax.set_ylabel('피쳐', fontproperties=font_prop)
plt.tight_layout()
plt.savefig(OUTPUT / 'feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print('feature_importance.png 저장 완료')
print(feat_df.to_string(index=False))

# ──────────────────────────────────────────────
# 8. 모델 성능 비교 차트
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("8. 모델 성능 비교 차트")
print("=" * 55)

x, width = np.arange(len(metrics)), 0.25
fig, ax = plt.subplots(figsize=(12, 5))
for i, (mname, row) in enumerate(results_df.iterrows()):
    ax.bar(x + i*width, [row[m] for m in metrics], width,
           label=mname, color=['#4C72B0','#55A868','#C44E52'][i], alpha=0.85)
ax.set_xticks(x + width)
ax.set_xticklabels(metrics, fontproperties=font_prop)
ax.set_ylim(0, 1.1)
ax.set_ylabel('점수', fontproperties=font_prop)
ax.set_title('모델별 성능 비교', fontproperties=font_prop)
ax.legend(prop=font_prop)
ax.axhline(0.8, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(OUTPUT / 'model_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print('model_comparison.png 저장 완료')

# ──────────────────────────────────────────────
# 9. 모델 저장 (Streamlit 앱용)
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("9. 모델 저장")
print("=" * 55)

model_path = OUTPUT / 'churn_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(best_tuned, f)
print(f'저장: {model_path}')
print(f'모델 타입: {type(best_tuned.named_steps["model"]).__name__}')
print(f'입력 피쳐 (파생 포함): {feat_names}')

# ──────────────────────────────────────────────
# 결론
# ──────────────────────────────────────────────
print("\n" + "=" * 55)
print("결론")
print("=" * 55)
print(f'\n최적 모델 : {best_name}')
print(f'AUC-ROC  : {roc_auc_score(y_test, y_prob_best):.4f}')
print(f'F1 Score : {f1_score(y_test, y_pred_best):.4f}')
print()
print(results_df[metrics].round(4).to_string())
print("\n완료!")
