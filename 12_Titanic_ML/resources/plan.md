# Titanic ML 프로젝트 계획

**목표:** titanic.csv 데이터셋으로 생존자 예측 모델 개발

---

## 데이터 개요

| 항목 | 내용 |
|------|------|
| 행 수 | 891개 |
| 컬럼 수 | 12개 |
| 타겟 | `Survived` (0=사망, 1=생존) |
| 주요 피처 | `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, `Embarked` |
| 결측값 | `Age` 177개 (~20%), `Cabin` 687개 (~77%), `Embarked` 2개 |

---

## Step 1. 데이터 살펴보기 ✅

- [x] `df.shape`, `df.dtypes`, `df.head()` 기본 확인
- [x] `df.describe()` 수치형 통계 요약
- [x] `df.isnull().sum()` 결측값 현황 파악
- [x] 타겟 클래스 분포 확인 (`Survived` 비율)

---

## Step 2. 데이터 전처리 ✅

- [x] **결측값 처리**
  - `Age`: 중앙값으로 대체
  - `Embarked`: 최빈값(S)으로 대체 (2개) — pandas 3.x CoW로 대입 방식 사용
  - `Cabin`: 결측 비율이 77%이므로 제거
- [x] **범주형 인코딩**
  - `Sex`: Label Encoding (female=0, male=1)
  - `Embarked`: One-Hot Encoding → `Embarked_Q`, `Embarked_S` (drop_first=True)
- [x] **불필요 컬럼 제거**: `PassengerId`, `Name`, `Ticket`, `Cabin`
- [x] **피처/타겟 분리**: `X`, `y` 설정
- [x] **학습/검증 분리**: `train_test_split` (test_size=0.2, random_state=42)

> **주의:** pandas 3.x에서 `fillna(inplace=True)`는 Copy-on-Write로 동작하지 않음.
> `df['col'] = df['col'].fillna(value)` 방식 사용 필요.

---

## Step 3. EDA (탐색적 데이터 분석) ✅

- [x] **생존율 시각화** (`output/01_categorical_survival.png`)
  - 성별(`Sex`) vs 생존율
  - 객실 등급(`Pclass`) vs 생존율
  - 탑승 항구(`Embarked`) vs 생존율
  - SibSp(형제자매/배우자 수) vs 생존율
- [x] **나이 분포 및 나이대별 생존율** (`output/02_age_survival.png`)

---

## Step 4. 모델 가설 ✅

**가설**
- 여성, 1등석, 낮은 나이일수록 생존 가능성이 높다
- `Sex`, `Pclass`, `Age`가 가장 중요한 피처일 것이다

**검증 방법**
- 3가지 모델 학습 후 성능 비교로 가설 검증
- 피처 중요도(Feature Importance)로 영향 피처 확인

---

## Step 5. 모델 학습 및 평가 ✅

### 5-1. 기본 모델 학습 및 비교

| 모델 | 클래스 |
|------|--------|
| 로지스틱 회귀 | `LogisticRegression` |
| 결정 트리 | `DecisionTreeClassifier` |
| 랜덤 포레스트 | `RandomForestClassifier` |

- [x] 3개 모델 각각 학습 (`fit`)
- [x] 예측 (`predict`)
- [x] 평가 지표 비교: Accuracy, Precision, Recall, F1-Score (`classification_report`)
- [x] 모델별 성능 비교 바 차트 저장 (`output/03_model_comparison.png`)

### 5-2. K-Fold 교차검증

- [x] `cross_val_score()` — 5-Fold CV로 각 모델 안정성 평가
  ```python
  cross_val_score(model, X, y, cv=5, scoring='accuracy')
  ```
- [x] CV 평균 / 표준편차 비교 출력
- [x] **교차검증 결과 시각화** — 박스플롯 + 개별 Fold 점수 산점도 (`output/05_cv_comparison.png`)

### 5-3. 하이퍼파라미터 튜닝 (GridSearchCV)

- [x] `RandomForestClassifier` 대상으로 GridSearchCV 적용
  ```python
  param_grid = {
      'n_estimators': [100, 200],
      'max_depth': [3, 5, 10, None],
      'min_samples_split': [2, 5]
  }
  ```
- [x] 최적 파라미터 출력 (`best_params_`)
- [x] 최적 모델로 최종 평가

### 5-4. 피처 중요도 (가설 검증)

- [x] Random Forest 피처 중요도 가로 바 차트 저장 (`output/04_feature_importance.png`)
- [x] 가설 검증: 중요 피처가 `Sex`, `Pclass`, `Age`인지 확인

---

## Step 6. Streamlit 앱 ✅

- [x] 최적 모델 저장 (`workflows/titanic_model.pkl`)
- [x] 승객 정보 입력 폼 (객실 등급, 성별, 나이, 동승자 수, 요금, 탑승 항구)
- [x] 생존 확률 예측 결과 카드 (생존/사망 색상 구분)
- [x] 확률 게이지 바 (생존/사망 수치)
- [x] 입력 정보 요약 expander
- [x] 밝은 톤(Light theme) UI 적용

---

## 산출물

| 파일 | 설명 |
|------|------|
| `workflows/titanic_ml.ipynb` | 전체 분석 노트북 |
| `workflows/titanic_model.pkl` | GridSearchCV 최적 모델 |
| `workflows/titanic_app.py` | Streamlit 예측 앱 |
| `output/01_categorical_survival.png` | 범주형 피처 생존율 차트 |
| `output/02_age_survival.png` | 나이 분포 생존율 차트 |
| `output/03_model_comparison.png` | 모델 성능 비교 차트 |
| `output/04_feature_importance.png` | 피처 중요도 차트 |
| `output/05_cv_comparison.png` | 교차검증 결과 박스플롯 |
