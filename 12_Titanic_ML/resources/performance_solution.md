# Titanic ML 예측 성능 향상 방법

## 1. Feature Engineering (가장 효과 큼)

현재 모델에서 버린 정보를 유용한 변수로 재활용합니다.

```python
# Name에서 호칭(Title) 추출
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.')
# Mr, Mrs, Miss, Master 등 → 성별+나이+결혼여부를 동시에 반영

# 가족 규모 (SibSp + Parch + 본인)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

# 나이대 구간화
df['AgeGroup'] = pd.cut(df['Age'], bins=[0,12,18,35,60,100], labels=[1,2,3,4,5])

# 요금 구간화
df['FareBand'] = pd.qcut(df['Fare'], 4, labels=[1,2,3,4])

# Cabin 앞글자 (구조 위치 반영)
df['Deck'] = df['Cabin'].str[0].fillna('U')  # A~G, U=Unknown
```

---

## 2. 결측값 처리 개선

```python
# 현재: Age를 전체 중앙값으로 채움 (단순)
# 개선: 성별 + 객실등급 조합별 중앙값으로 채움
df['Age'] = df.groupby(['Sex','Pclass'])['Age'].transform(
    lambda x: x.fillna(x.median())
)
```

---

## 3. 더 강력한 모델 사용

| 모델 | 특징 |
|------|------|
| XGBoost | 현재 Titanic 리더보드 상위권 모델 |
| LightGBM | 빠르고 정확도 높음 |
| 앙상블(Voting) | 여러 모델 예측을 다수결로 합침 |

```python
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(estimators=[
    ('rf', RandomForestClassifier()),
    ('xgb', XGBClassifier()),
    ('lr', LogisticRegression())
], voting='soft')  # 확률 평균으로 투표
```

---

## 4. 스케일링 추가 (로지스틱 회귀 성능 향상)

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
# 로지스틱 회귀는 변수 크기에 민감 → 스케일링 필수
```

---

## 5. GridSearchCV 범위 확장

```python
# 현재보다 넓은 파라미터 탐색
param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}
```

---

## 기대 효과 (Titanic 기준)

| 방법 | 정확도 향상 예상 |
|------|----------------|
| Title 추출 | +2~4% (효과 가장 큼) |
| FamilySize 파생 | +1~2% |
| XGBoost 도입 | +1~3% |
| 앙상블 | +1~2% |
| 스케일링 | +0.5~1% |

---

## 우선순위 추천

1순위: **Title + FamilySize Feature Engineering**
2순위: **XGBoost 또는 앙상블 모델**
3순위: **GridSearchCV 파라미터 범위 확장**

> Feature Engineering이 모델 교체보다 훨씬 효과적입니다.
> Titanic에서 Name 컬럼을 버리지 않고 Title로 변환하는 것만으로도 정확도가 크게 올라갑니다.