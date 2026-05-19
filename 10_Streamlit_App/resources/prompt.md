이전 세션(09_ML_Pipeline)에서 훈련된 고객 이탈 예측 모델이 churn_model.pkl로 저장되어 있습니다.

모델 입력 피처 (총 14개):
- 원본 피처 (8개): age, tenure_months, monthly_spend, num_products, num_support_tickets, last_login_days_ago, payment_method, region
- 파생 피처 (6개, 앱 내에서 자동 계산): spend_per_product, support_rate, relative_inactivity, age_tenure_interaction, engagement_score, lifetime_value_proxy

※ contract_type은 target(churned)과 완전 상관관계(데이터 누수)로 인해 학습 및 앱에서 제외됨
※ 모델: Logistic Regression (sklearn Pipeline — ColumnTransformer + StandardScaler + OneHotEncoder)

churn_predictor_app.py라는 이름의 Streamlit 앱을 만들어 주세요. 조건은 다음과 같습니다:

1. 앱의 기능을 설명하는 깔끔한 제목과 설명을 포함할 것
2. 원본 피처 8개에 대한 입력 필드를 제공할 것 (숫자형은 슬라이더, 범주형은 드롭다운 사용)
   - 파생 피처 6개는 입력값으로부터 앱 내부에서 자동 계산
3. "Predict Churn Risk" 버튼을 포함할 것
4. 예측 결과를 명확한 시각적 표시로 보여줄 것 (초록색 = 저위험, 빨간색 = 고위험)
5. 이탈 확률을 퍼센트(%)로 표시할 것
6. 해당 고객의 예측에 영향을 준 상위 5개 요인을 막대 차트로 보여줄 것
7. 앱 사용 방법을 간략히 안내하는 사이드바를 포함할 것

비기술직 이해관계자도 쉽게 사용할 수 있도록 단순하고 직관적인 디자인으로 제작해 주세요.
