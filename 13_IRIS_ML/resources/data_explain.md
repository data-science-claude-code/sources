# IRIS 데이터셋 설명

## 기본 정보

| 항목 | 내용 |
|------|------|
| 파일명 | `iris.csv` |
| 행 수 | 150개 |
| 열 수 | 5개 |
| 결측치 | 없음 |
| 태스크 유형 | 다중 분류 (Multi-class Classification) |

---

## 컬럼 설명

| 컬럼 | 타입 | 단위 | 설명 |
|------|------|------|------|
| `sepal_length` | float | cm | 꽃받침(sepal) 길이 |
| `sepal_width` | float | cm | 꽃받침(sepal) 너비 |
| `petal_length` | float | cm | 꽃잎(petal) 길이 |
| `petal_width` | float | cm | 꽃잎(petal) 너비 |
| `species` | object | — | 붓꽃 품종 (타겟 변수) |

---

## 타겟 변수 `species` 분포

| 품종 | 샘플 수 | 비율 |
|------|--------|------|
| Iris-setosa | 50 | 33.3% |
| Iris-versicolor | 50 | 33.3% |
| Iris-virginica | 50 | 33.3% |

> 3개 클래스가 완벽하게 균등 분포(각 50개)되어 있어 클래스 불균형 없음.

---

## 수치 통계 요약

| | sepal_length | sepal_width | petal_length | petal_width |
|---|---|---|---|---|
| 평균 | 5.843 | 3.054 | 3.759 | 1.199 |
| 표준편차 | 0.828 | 0.434 | 1.764 | 0.763 |
| 최솟값 | 4.300 | 2.000 | 1.000 | 0.100 |
| 중앙값 | 5.800 | 3.000 | 4.350 | 1.300 |
| 최댓값 | 7.900 | 4.400 | 6.900 | 2.500 |

---

## 피처 간 상관관계

| | sepal_length | sepal_width | petal_length | petal_width |
|---|---|---|---|---|
| sepal_length | 1.000 | -0.109 | **0.872** | **0.818** |
| sepal_width | -0.109 | 1.000 | -0.421 | -0.357 |
| petal_length | **0.872** | -0.421 | 1.000 | **0.963** |
| petal_width | **0.818** | -0.357 | **0.963** | 1.000 |

**주요 인사이트:**
- `petal_length` ↔ `petal_width` 상관계수 **0.963** — 매우 강한 양의 상관
- `sepal_length` ↔ `petal_length` 상관계수 **0.872** — 강한 양의 상관
- `sepal_width`는 다른 피처들과 상관관계가 낮아 독립적인 정보 제공

---

## 품종별 특징

| 품종 | 특징 |
|------|------|
| **Iris-setosa** | 꽃잎(petal)이 매우 작고 짧아 다른 두 품종과 명확히 구분됨 |
| **Iris-versicolor** | 중간 크기의 꽃잎, setosa와 virginica 사이에 위치 |
| **Iris-virginica** | 꽃잎이 가장 크고 긺, versicolor와 일부 겹침 |

---

## 태스크 목표

`sepal_length`, `sepal_width`, `petal_length`, `petal_width` 4개 피처로 붓꽃 품종(`species`)을 분류하는 **3-class 분류 모델** 구축.

- setosa는 선형 분리 가능(linearly separable)
- versicolor ↔ virginica 간 경계가 불분명하여 더 복잡한 모델이 유리
- 피처 스케일링 후 SVM, KNN, Random Forest, Logistic Regression 등 다양한 알고리즘 비교 권장
