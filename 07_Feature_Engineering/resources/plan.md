# 고객 이탈 예측 성능 향상 계획

## Context

`07_Feature_Engineering/resources/customer_churn_raw.csv` 단일 데이터셋(100행, 11컬럼)만을 사용해 이탈 예측 모델의 성능을 극대화한다.

**데이터 핵심 특성 (EDA 결과):**
- 행 수: 100개 (소규모 → 과적합 위험, CV 전략 중요)
- 타겟 분포: 이탈 51 / 유지 49 (균형 잡힌 편)
- 결측치: 없음
- **핵심 발견: `contract_type`이 타겟을 완벽하게 분리** (Monthly=이탈률 100%, Annual=0%)
- 수치형 상관관계: `num_support_tickets`(+0.867), `last_login_days_ago`(+0.867), `tenure_months`(-0.876), `monthly_spend`(-0.845), `num_products`(-0.809)
- 범주형: `contract_type`(Monthly/Annual), `payment_method`(3종), `region`(4방향)

**성능 향상 전략:**  
소규모 데이터에서 성능을 높이는 핵심은 (1) 풍부한 파생 피처, (2) 안정적인 평가 프레임, (3) 여러 모델 비교 및 앙상블이다.

---

## 구현 계획

### 새 작업 디렉토리
```
09_01_Customer_Churn_ML/
  resources/   ← customer_churn_raw.csv 심볼릭 링크 또는 복사
  workflows/   ← churn_prediction.ipynb
  output/      ← feature_importance.png, roc_curve.png, model_report.md
```

---

### Step 1 — 데이터 준비 및 기본 전처리
```python
# customer_id 제거 (식별자)
# 범주형 인코딩
contract_type  → is_monthly (binary: Monthly=1, Annual=0)
payment_method → OHE (3열)
region         → OHE (4열)
```

---

### Step 2 — Feature Engineering (성능 향상의 핵심 레버)

#### A. 비율 / 복합 점수

| 파생 피처 | 수식 | 의미 |
|-----------|------|------|
| `spend_per_product` | `monthly_spend / num_products` | 제품당 지출 |
| `spend_per_tenure` | `monthly_spend / (tenure_months + 1)` | 이용 기간당 지출 |
| `support_intensity` | `num_support_tickets / (tenure_months + 1)` | 이용 기간 대비 문의 빈도 |
| `support_per_product` | `num_support_tickets / num_products` | 제품당 문의 수 |
| `inactivity_ratio` | `last_login_days_ago / (tenure_months * 30)` | 이용 기간 대비 비활성 비율 |
| `tenure_age_ratio` | `tenure_months / age` | 나이 대비 서비스 기간 |
| `total_revenue_est` | `monthly_spend * tenure_months` | 누적 매출 추정 |

#### B. 복합 위험 점수

| 파생 피처 | 수식 | 의미 |
|-----------|------|------|
| `churn_risk_score` | `last_login_days_ago * num_support_tickets / (tenure_months + 1)` | 비활성·문의·기간 복합 이탈 위험 |
| `engagement_score` | `num_products * tenure_months / (last_login_days_ago + 1)` | 활성도 기반 참여도 |
| `value_score` | `monthly_spend * num_products / (num_support_tickets + 1)` | 고객 가치 복합 점수 |

#### C. 교호작용 (Interaction)

| 파생 피처 | 수식 | 의미 |
|-----------|------|------|
| `is_monthly_x_inactive` | `is_monthly × last_login_days_ago` | 월 계약 + 비활성 복합 위험 |
| `is_monthly_x_support` | `is_monthly × num_support_tickets` | 월 계약 + 높은 문의 |
| `inactive_x_support` | `last_login_days_ago × num_support_tickets` | 비활성 + 높은 문의 (이중 위험) |
| `tenure_x_spend` | `tenure_months × monthly_spend` | 장기 고지출 고객 식별 |

#### D. 이진 플래그

| 파생 피처 | 조건 | 의미 |
|-----------|------|------|
| `is_new_customer` | `tenure_months <= 6` | 신규 고객 여부 |
| `is_inactive_long` | `last_login_days_ago >= 30` | 장기 비활성 여부 |
| `is_high_spender` | `monthly_spend >= 300` | 고지출 고객 |
| `high_support` | `num_support_tickets >= 5` | 고위험 문의 고객 |

#### E. 구간화 (Binning)

| 파생 피처 | 구간 | 의미 |
|-----------|------|------|
| `age_group` | 25-34 / 35-44 / 45-52 | 연령대 |
| `tenure_segment` | 0-12(신규) / 13-36(중기) / 37-60(장기) | 이용 기간 단계 |
| `spend_tier` | ~150(저) / 151-300(중) / 301+(고) | 지출 등급 |

#### F. 타겟 인코딩 (EDA 기반 이탈률 매핑)

| 파생 피처 | 매핑 | 주의 |
|-----------|------|------|
| `region_risk` | East=0.20, North=0.48, South=0.64, West=0.72 | CV 내부에서만 적용 (리크 방지) |
| `payment_risk` | Bank Transfer=0.35, Credit Card=0.58, PayPal=0.59 | CV 내부에서만 적용 (리크 방지) |

**원칙:** RFECV(Step 5)로 최종 피처 선택 — 전체 후보를 만들고 모델이 중요한 것만 고른다.

---

### Step 3 — 평가 프레임워크

100행에서 단순 train/test split(80/20 = 20행 테스트)은 분산이 크다.

```python
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
# → 50회 폴드, 안정적인 ROC-AUC/F1 추정
```

**주요 지표:** ROC-AUC (임계값 독립), F1-Score

---

### Step 4 — 모델 비교

| 모델 | 소규모 데이터 특성 |
|------|--------------------|
| Logistic Regression (L1/L2) | 기준선, 해석 용이 |
| Random Forest | 배깅으로 분산 감소 |
| LightGBM | 작은 트리, 정규화 내장 |
| SVM (RBF) | 소규모 데이터에 강인 |
| GradientBoosting (sklearn) | 느리지만 안정적 |

같은 CV 프레임으로 모두 평가 후 상위 3개 선택.

---

### Step 5 — 피처 선택

파생 피처 추가 후 과적합 방지:
```python
from sklearn.feature_selection import RFECV

selector = RFECV(estimator=LogisticRegression(C=0.1), 
                 cv=StratifiedKFold(5), scoring='roc_auc')
selector.fit(X_engineered, y)
# → 최적 피처 수와 최적 피처셋 도출
```

---

### Step 6 — 하이퍼파라미터 튜닝

상위 2개 모델에 대해 GridSearchCV 적용:
```python
# LightGBM 예시
param_grid = {
    'num_leaves': [7, 15, 31],
    'learning_rate': [0.05, 0.1],
    'n_estimators': [50, 100, 200],
    'reg_alpha': [0, 0.1, 1.0],  # L1 정규화
}
```

---

### Step 7 — 앙상블

최종 상위 3개 모델을 Soft Voting으로 결합:
```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(
    estimators=[('lr', best_lr), ('lgbm', best_lgbm), ('rf', best_rf)],
    voting='soft'
)
```

---

### Step 8 — 결과 시각화 및 해석

1. `feature_importance.png` — 피처 중요도 (LightGBM / RFECV 기준)
2. `roc_curve.png` — 모델별 ROC 곡선 비교
3. `confusion_matrix.png` — 최종 모델 혼동 행렬
4. `model_report.md` — 모델별 CV 점수 표, 최종 모델 선택 근거

---

## 파일 구조

```
17_Customer_Churn_ML/
  resources/customer_churn_raw.csv   ← 원본 복사
  workflows/churn_prediction.ipynb   ← 메인 노트북
  output/
    feature_importance.png
    roc_curve.png
    model_report.md
```

---

## 검증 방법

1. `conda run -n ds_env jupyter nbconvert --to notebook --execute --inplace workflows/churn_prediction.ipynb`
2. 노트북 출력에서 RepeatedStratifiedKFold ROC-AUC 확인 (목표: ≥ 0.95)
3. `output/` 디렉토리에 시각화 파일 생성 확인
4. 모델별 CV 점수 비교표 출력 확인
