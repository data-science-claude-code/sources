---
description: 재사용 가능한 데이터 분석 워크플로우 실행
argument-hint: "[파일명 또는 경로]"
---

# /analyze

데이터 파일을 지정하면 품질 검사 → 심층 분석 → 시각화 → Top 3 권고까지 자동 진행합니다.

---

## Step 1: 명확화 질문 (항상 먼저 실행)

분석 전에 다음 4가지를 확인합니다:

1. 이 데이터로 가장 파악하고 싶은 것은 무엇인가요?
   - 채널별 성과 / 제품 수익성 / 고객 세분화 / 계절성 트렌드
2. 가장 중요한 지표는 무엇인가요?
   - 매출(Revenue) / 이익(Profit) / 주문 수량 / 고객 수
3. 특정 기간에 집중해야 하나요?
   - 전체 기간 / 특정 분기 / 최근 N개월
4. `customers.xlsx`와 교차 분석이 필요한가요?

---

## Step 2: 데이터 품질 확인

```powershell
F:\Anaconda3\python.exe workflows\analysis_helper.py <데이터파일경로>
```

- 결측값, 중복 행, IQR 이상치, 음수값 자동 탐지
- 문제 발견 시 사용자에게 보고 후 처리 방향 확인

---

## Step 3: 노트북 Parameters 업데이트 후 실행

`workflows/basecamp_brew_analysis.ipynb` **Cell 2** (Parameters 셀)를
Step 1 답변에 맞게 업데이트한 뒤 전체 실행:

```powershell
jupyter nbconvert --to notebook --execute `
  workflows\basecamp_brew_analysis.ipynb `
  --output workflows\basecamp_brew_analysis.ipynb `
  --ExecutePreprocessor.timeout=120
```

생성 차트 (output/ 폴더):
- `01_monthly_trend.png` — 12개월 매출·이익 추이
- `02_channel_performance.png` — 채널별 매출·객단가
- `03_product_heatmap.png` — 카테고리×제품 매출 히트맵
- `04_customer_channels.png` — 고객 유입 채널·재구매율

---

## Step 4: 결과 전달

분석 완료 후 다음을 보고합니다:

1. **핵심 지표 요약** — 총 매출, 총 이익, 평균 마진율 ($X,XXX.XX 형식)
2. **주요 발견** — 최고/최저 채널·제품·월, 이상 주문 건수
3. **차트 파일 목록** — output/ 폴더의 PNG 경로
4. **Top 3 비즈니스 액션 아이템** — 실제 수치 근거 포함

---

## 다른 데이터에 재사용하기

Cell 2 (Parameters)에서 경로와 목표만 변경하면 됩니다:

```python
SALES_FILE     = r'새_데이터_파일_경로.xlsx'
CUSTOMERS_FILE = None          # 고객 파일 없으면 None
ANALYSIS_GOAL  = "분석 목표 설명"
```
