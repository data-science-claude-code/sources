# Data Science with Claude Code

Claude Code를 사용하여 Vibe Coding(No Code)으로 단계별로 구성된 데이터 사이언스 실습 프로젝트입니다. 각 태스크는 독립적인 Jupyter 노트북 또는 Python 스크립트로 구성되어 있습니다.

## 실행 환경

- **macOS**: Python 3.11.0 / `conda activate ds_env`
- **Windows 11**: Python 3.10.0 / `conda activate agent_env`

## 태스크 목록

| 디렉토리 | 태스크 | 입력 | 주요 출력 |
|----------|--------|------|----------|
| 01_Full_EDA/ | Exploratory Data Analysis | `ecommerce_sales.csv` | `.ipynb` + 5× PNG + `.xlsx` |
| 02_Data_Cleaning/ | Data Cleaning & Standardization | `messy_customer_data.csv` | `.ipynb` + `cleaned_customer_data.csv` |
| 03_Visualization_Slide_Deck/ | Visualization + PowerPoint | `monthly_revenue.csv` | `.ipynb` + 4× PNG + `.pptx` |
| 04_Plain_SQL/ | SQL from CSVs (SQLite) | `customers/orders/products.csv` | `.ipynb` |
| 05_API_Data_Pull/ | API Data Pull | — | `.ipynb` + `stock_data.csv` + PNG |
| 06_Web_Scraping/ | Web Scraping | — | `.ipynb` + `largest_companies_scraped.csv` + 3× PNG |
| 07_Feature_Engineering/ | Feature Engineering for ML | `customer_churn_raw.csv` | `.ipynb` + `customer_churn_engineered.csv` + 3× PNG |
| 08_Hypothesis/ | A/B Testing & Statistics | `ab_test_results.csv` | `.ipynb` + 5× PNG + `executive_summary.md` |
| 09_ML_Pipeline/ | ML Model Training (Churn) | `customer_churn_engineered.csv` | `.ipynb` + `churn_model.pkl` + 3× PNG |
| 10_Streamlit_App/ | Interactive Web App | (09 모델 활용) | `churn_predictor_app.py` |
| 11_BMI_ML/ | BMI Classification ML | `bmi_dataset.csv` | `.ipynb` + `bmi_model.pkl` + 9× PNG |
| 12_Titanic_ML/ | Titanic Survival ML + Streamlit App | `titanic.csv` | `.ipynb` + `titanic_model.pkl` + 5× PNG + `titanic_app.py` |
| 13_IRIS_ML/ | IRIS Classification & EDA + Streamlit App | `iris.csv` | `.ipynb` + `iris_app.py` + 8× PNG |
| 14_Boston_Housing_ML/ | Boston Housing Regression | `boston_housing.csv` | `.ipynb` + `boston_model.pkl` + 4× PNG |
| 15_Basecamp_Brew_Analysis/ | Basecamp Brew 비즈니스 분석 | `sales-data.xlsx` | `.ipynb` + `final_report.html` + 11× PNG |
| 16_TEP_Fault_ML/ | TEP 공정 고장 탐지 ML | TEP CSV 4개 (5.5GB) | `.ipynb` + `tep_model.pkl` + 4× PNG + `performance_study.md` |

## 라이브러리 스택

| 분류 | 라이브러리 |
|------|-----------|
| 데이터 처리 | pandas, numpy |
| 시각화 | matplotlib, seaborn |
| 머신러닝 | scikit-learn, regression, Random Forest, xgboost, lightgbm |
| 웹 앱 | streamlit |
| 문서 | openpyxl, python-pptx |

## 프로젝트 구조

```
<task_dir>/
├── resources/   # 입력 데이터 및 참고 문서
├── workflows/   # 분석 노트북, 스크립트, 모델(.pkl)
└── output/      # 결과물 (PNG, CSV 등)
```

## 한글 폰트 설정

**macOS**
```python
import matplotlib.font_manager as fm
font_prop = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/AppleGothic.ttf')
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
```

**Windows**
```python
import matplotlib.font_manager as fm
font_prop = fm.FontProperties(fname='C:/Windows/Fonts/malgun.ttf')
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
```
