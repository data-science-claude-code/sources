# 03_model_comparison.png 설명

**회귀 모델 성능 비교** 차트로, 7개 모델을 두 가지 지표(RMSE, R²)로 비교합니다.

---

## 왼쪽: RMSE 비교 (낮을수록 좋음)

각 모델당 **막대 2개가 나란히** 있는 구조입니다. 

- **왼쪽 막대 (CV RMSE)**: 교차검증(5-fold 등)으로 측정한 평균 오차. 오차 막대(error bar)가 붙어 있어 폴드 간 성능 편차를 보여줌
- **오른쪽 막대 (Test RMSE)**: 테스트셋에서 실제로 측정한 오차. 숫자 레이블(4.93, 5.07 등)이 이 값을 표시

실용적으로 볼 때 중요한 것은 **숫자 레이블(Test RMSE)** 과 **오차 막대의 크기**입니다.

- 오차 막대가 작을수록 → 교차검증 폴드마다 성능이 일정한 안정적인 모델
- Decision Tree는 오차 막대가 크게 보여 → 데이터에 따라 성능이 불안정

### 모델별 Test RMSE

| 모델 | Test RMSE |
|------|-----------|
| Linear Regression | 4.93 |
| Ridge | 4.93 |
| Lasso | 5.07 |
| ElasticNet | 5.02 |
| Decision Tree | 2.92 |
| Random Forest | 2.81 |
| **Gradient Boosting** | **2.49** ← 최우수 |

선형 계열 4개 모델(Linear~ElasticNet)이 RMSE 4.9~5.1로 비슷하게 묶이고, 트리 계열 3개가 2~3대로 확연히 낮습니다.

---

## 오른쪽: R² 비교 (높을수록 좋음)

R²는 모델이 주택가격의 분산을 얼마나 설명하는지를 나타냅니다.

| 모델 | R² |
|------|-----|
| Linear Regression | 0.669 |
| Ridge | 0.668 |
| Lasso | 0.650 |
| ElasticNet | 0.656 |
| Decision Tree | 0.883 |
| Random Forest | 0.892 |
| **Gradient Boosting** | **0.915** ← 최우수 (빨간색 강조) |

---

## 핵심 인사이트

- **선형 모델의 한계**: Linear/Ridge/Lasso/ElasticNet 모두 R² 0.65~0.67 수준으로, Boston Housing 데이터의 비선형 관계를 충분히 포착하지 못함
- **트리 계열의 압도적 우세**: 비선형 관계를 자동으로 포착하는 트리 기반 모델이 선형 모델 대비 R² 기준 약 0.22~0.25 높음
- **Decision Tree 불안정성**: RMSE 오차 막대가 커서 데이터 분할에 따라 성능 편차가 큼
- **최적 모델 Gradient Boosting** (빨간색 강조): RMSE 2.49, R² 0.915로 모든 모델 중 가장 우수하며, Random Forest(RMSE 2.81)보다도 한 단계 더 개선된 성능
