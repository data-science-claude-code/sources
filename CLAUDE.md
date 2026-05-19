# CLAUDE.md

번호가 매겨진 디렉토리로 구성된 단계별 데이터 사이언스 실습 프로젝트입니다.

## 실행 방법

빌드 시스템 없음. 모든 태스크는 독립 실행형 Jupyter 노트북 또는 Python 스크립트입니다.

```powershell
# 노트북 실행 — 결과를 노트북 파일에 저장
& "F:\Anaconda3\envs\agent_env\Scripts\jupyter.exe" nbconvert --to notebook --execute --inplace workflows\<notebook>.ipynb
```

**Python 환경**: `F:\Anaconda3\envs\agent_env\python.exe` (Python 3.10.0)

## 태스크 시작 전 데이터 탐색

노트북 작성 전, `resources/` 의 입력 데이터를 반드시 먼저 읽고 파악한다.
pandas dataframe로 출력한다.

```python
df.shape          # 행/열 수
df.dtypes         # 컬럼 타입
df.isnull().sum() # 결측값 현황
df.describe()     # 기초 통계
df.head()         # 샘플 확인
```

탐색 결과를 바탕으로 타입 변환 필요 여부, 결측/이상값 처리 방향을 파악한 뒤 분석 코드를 작성한다.

## 프로젝트 구조 및 출력 규칙

각 태스크 디렉토리는 아래 구조를 따릅니다:

```
<task_dir>/
  resources/   ← 입력 데이터 (CSV, XLSX 등)
  workflows/   ← 노트북(.ipynb), 소스 코드, ML 모델(.pkl)
  output/      ← 차트(PNG), 보고서(HTML/PPTX/MD)
```

## 코드 스타일

- 소스 코드의 중요 부분에 이해하기 쉽고 간결한 주석 추가
- 한글 출력 시 Malgun Gothic 폰트 적용 필수

```python
import matplotlib.font_manager as fm
font_prop = fm.FontProperties(fname=r'C:\Windows\Fonts\malgun.ttf')
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
```

## 라이브러리 스택

| 용도 | 라이브러리 |
|------|-----------|
| 데이터 처리 | pandas, numpy |
| 시각화 | matplotlib, seaborn |
| 머신러닝 | scikit-learn, xgboost, lightgbm |
| 웹 앱 | streamlit |
| 파일 출력 | openpyxl (Excel), python-pptx (PowerPoint) |

## 태스크 현황

| Dir | Task | Status | Input | Output |
|-----|------|--------|-------|--------|
| 01_Full_EDA/ | Exploratory Data Analysis | ✅ 완료 | `ecommerce_sales.csv` | `.ipynb` + 5× PNG + `.xlsx` |
| 02_Data_Cleaning/ | Data Cleaning & Standardization | ✅ 완료 | `messy_customer_data.csv` | `.ipynb` + `cleaned_customer_data.csv` |
| 03_Visualization_Slide_Deck/ | Visualization + PowerPoint | ✅ 완료 | `monthly_revenue.csv` | `.ipynb` + 4× PNG + `.pptx` |
| 04_Plain_SQL/ | SQL from CSVs (SQLite) | ✅ 완료 | `customers.csv`, `orders.csv`, `products.csv` | `.ipynb` + 5× PNG |
| 05_API_Data_Pull/ | API Data Pull | ✅ 완료 | — | `.ipynb` + `stock_data.csv` + 1× PNG |
| 06_Web_Scraping/ | Web Scraping | ✅ 완료 | — | `.ipynb` + `largest_companies_scraped.csv` + 3× PNG |
| 07_Feature_Engineering/ | Feature Engineering for ML | ✅ 완료 | `customer_churn_raw.csv` | `.ipynb` + `customer_churn_engineered.csv` + 3× PNG |
| 08_Hypothesis/ | A/B Testing & Statistics | ✅ 완료 | `ab_test_results.csv` | `.ipynb` + 5× PNG + `executive_summary.md` |
| 09_ML_Pipeline/ | ML Model Training | ✅ 완료 | `customer_churn_engineered.csv` | `.ipynb` + `churn_model.pkl` + 3× PNG |
| 10_Streamlit_App/ | Interactive Web App | ✅ 완료 | (09 모델 활용) | `churn_predictor_app.py` |
| 11_BMI_ML/ | BMI Classification ML | ✅ 완료 | `bmi_dataset.csv` | `.ipynb` + `bmi_model.pkl` + 9× PNG |
| 12_Titanic_ML/ | Titanic Survival ML | ✅ 완료 | `titanic.csv` | `.ipynb` + `titanic_model.pkl` + 4× PNG |
| 13_IRIS_ML/ | IRIS Classification & EDA + Streamlit App | ✅ 완료 | `iris.csv` | `.ipynb` + `iris_app.py` + 8× PNG |
| 14_Boston_Housing_ML/ | Boston Housing Regression | ✅ 완료 | `boston_housing.csv` | `.ipynb` + `boston_model.pkl` + 4× PNG |
| 15_Basecamp_Brew_Analysis/ | Basecamp Brew 비즈니스 분석 | ✅ 완료 | `sales-data.xlsx` | `.ipynb` + `final_report.html` + 11× PNG |
| 16_TEP_Fault_ML/ | TEP 공정 고장 탐지 ML | ✅ 완료 | TEP CSV 4개 (5.5GB) | `.ipynb` + `tep_model.pkl` + 4× PNG + `performance_study.md` |

## 주요 데이터 스키마

**04/customers.csv**: `customer_id, name, email, signup_date, region, tier` (tier: Silver/Bronze/Gold)  
**04/orders.csv**: `order_id, customer_id, product_id, order_date, amount, status, quantity`  
**04/products.csv**: `product_id, product_name, category, price, cost`  
**07/customer_churn_raw.csv**: `customer_id, age, tenure_months, monthly_spend, num_products, num_support_tickets, last_login_days_ago, contract_type, payment_method, region, churned`  
**08/ab_test_results.csv**: `user_id, group(control/treatment), converted, revenue, session_duration_seconds, pages_viewed, device, signup_date`  
**13/iris.csv**: `sepal_length, sepal_width, petal_length, petal_width, species` (Iris-setosa/versicolor/virginica, 150행)
