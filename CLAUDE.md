# CLAUDE.md

번호가 매겨진 디렉토리로 구성된 단계별 데이터 사이언스 실습 프로젝트입니다.

## 환경

- **Python**: 3.11.0 (`conda activate ds_env`)
- **직접 경로**: `/Users/jhkim/opt/anaconda3/envs/ds_env/python`

```bash
# 노트북 실행 (결과를 노트북에 저장)
conda run -n ds_env jupyter nbconvert --to notebook --execute --inplace workflows/<notebook>.ipynb

# 스크립트 직접 실행
conda run -n ds_env python <script.py>
```

> 패키지 미설치 시: `conda run -n ds_env pip install scikit-learn lightgbm streamlit optuna`

## 디렉토리 구조

```
<task_dir>/
  resources/   ← 입력 데이터 (CSV, XLSX 등)
  workflows/   ← 노트북(.ipynb), 소스 코드, ML 모델(.pkl)
  output/      ← 차트(PNG), 보고서(HTML/PPTX/MD)
```

## 작업 규칙

**1. EDA 우선** — 노트북 작성 전 `resources/` 데이터를 반드시 먼저 파악한다.
```python
df.shape; df.dtypes; df.isnull().sum(); df.describe(); df.head()
```

**2. 한글 폰트** — 시각화 시 AppleGothic 적용 필수.
```python
import matplotlib.font_manager as fm
font_prop = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/AppleGothic.ttf')
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
```

**3. 주석** — 핵심 로직에 간결한 한글 주석 추가.

## 라이브러리 스택

| 용도 | 라이브러리 |
|------|-----------|
| 데이터 처리 | pandas, numpy |
| 시각화 | matplotlib, seaborn |
| 머신러닝 | scikit-learn, xgboost, lightgbm |
| 웹 앱 | streamlit |
| 파일 출력 | openpyxl, python-pptx |

## 태스크 현황

| Dir | Task | Status |
|-----|------|--------|
| 01_Full_EDA/ | Exploratory Data Analysis | ✅ |
| 02_Data_Cleaning/ | Data Cleaning & Standardization | ✅ |
| 03_Visualization_Slide_Deck/ | Visualization + PowerPoint | ✅ |
| 04_Plain_SQL/ | SQL from CSVs (SQLite) | ✅ |
| 05_API_Data_Pull/ | API Data Pull | ✅ |
| 06_Web_Scraping/ | Web Scraping | ✅ |
| 07_Feature_Engineering/ | Feature Engineering for ML | ✅ |
| 08_Hypothesis/ | A/B Testing & Statistics | ✅ |
| 09_ML_Pipeline/ | ML Model Training | ✅ |
| 10_Streamlit_App/ | Interactive Web App | ✅ |
| 11_BMI_ML/ | BMI Classification ML | ✅ |
| 12_Titanic_ML/ | Titanic Survival ML | ✅ |
| 13_IRIS_ML/ | IRIS Classification & EDA + Streamlit App | ✅ |
| 14_Boston_Housing_ML/ | Boston Housing Regression | ✅ |
| 15_Basecamp_Brew_Analysis/ | Basecamp Brew 비즈니스 분석 | ✅ |
| 16_TEP_Fault_ML/ | TEP 공정 고장 탐지 ML | ✅ |

## 주요 데이터 스키마

| 파일 | 주요 컬럼 |
|------|----------|
| 04/customers.csv | customer_id, name, email, signup_date, region, tier |
| 04/orders.csv | order_id, customer_id, product_id, order_date, amount, status, quantity |
| 04/products.csv | product_id, product_name, category, price, cost |
| 07/customer_churn_raw.csv | customer_id, age, tenure_months, monthly_spend, num_products, num_support_tickets, last_login_days_ago, contract_type, payment_method, region, churned |
| 08/ab_test_results.csv | user_id, group, converted, revenue, session_duration_seconds, pages_viewed, device, signup_date |
| 13/iris.csv | sepal_length, sepal_width, petal_length, petal_width, species (150행) |
