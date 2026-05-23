# customer_churn_engineered.csv 설명

`customer_churn_raw.csv`에 피처 엔지니어링을 적용해 생성한 데이터셋입니다. 총 100행, 27개 컬럼.

---

## 원본 피처 (7개)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `age` | int | 고객 나이 |
| `tenure_months` | int | 서비스 이용 기간(월) |
| `monthly_spend` | float | 월 결제 금액($) |
| `num_products` | int | 구독 중인 상품 수 |
| `num_support_tickets` | int | 지원 티켓 발행 수 |
| `last_login_days_ago` | int | 마지막 로그인 이후 경과 일수 |
| `churned` | int | 이탈 여부 (1=이탈, 0=유지) — 타겟 변수 |

---

## 파생 피처 (수치형, 8개)

| 컬럼 | 계산식 | 의미 |
|------|--------|------|
| `spend_per_product` | `monthly_spend / num_products` | 상품당 지출. 낮을수록 번들 활용이 낮아 이탈 위험 상승 |
| `support_rate` | `num_support_tickets / tenure_months` | 월별 티켓 발생률. 높을수록 불만 누적 → 이탈 가능성 ↑ |
| `relative_inactivity` | `last_login_days_ago / tenure_months` | 재직 기간 대비 비활성 정도. 이 값이 클수록 최근에 급격히 이탈한 패턴 |
| `age_tenure_interaction` | `age * tenure_months` | 나이와 재직기간 상호작용. 젊고 재직기간이 짧으면 낮게, 장기 고령 고객은 높게 나옴 |
| `engagement_score` | `num_products / (num_support_tickets + 1) * (1 / (last_login_days_ago + 1)) * tenure_months` | 복합 참여도 지표. 제품 사용은 많고, 티켓·비활성이 낮을수록 높음 |
| `lifetime_value_proxy` | `monthly_spend * tenure_months` | 누적 기대 매출(LTV 근사). 장기 고지출 고객일수록 큰 값 |

---

## 파생 피처 (이진 플래그, 4개)

| 컬럼 | 기준 | 의미 |
|------|------|------|
| `high_support_flag` | `num_support_tickets >= 5` | 고빈도 지원 요청 고객 (불만 집중) |
| `inactive_flag` | `last_login_days_ago >= 30` | 30일 이상 미접속 (비활성 고객) |
| `low_tenure_flag` | `tenure_months <= 6` | 신규 고객 (6개월 이하, 조기 이탈 위험) |
| `monthly_contract_flag` | 계약 유형이 Monthly | 월간 계약 고객 (연간 대비 이탈 장벽 낮음) |

---

## 종합 위험 점수

| 컬럼 | 계산식 | 의미 |
|------|--------|------|
| `risk_score` | `high_support_flag + inactive_flag + low_tenure_flag + monthly_contract_flag` | 4개 플래그 합산 (0~4). 4점이면 최고 위험 고객 |

---

## 원-핫 인코딩 피처 (10개)

### contract_type (2개)
| 컬럼 | 원본값 |
|------|--------|
| `contract_type_Annual` | Annual |
| `contract_type_Monthly` | Monthly |

### payment_method (3개)
| 컬럼 | 원본값 |
|------|--------|
| `payment_method_Bank Transfer` | Bank Transfer |
| `payment_method_Credit Card` | Credit Card |
| `payment_method_PayPal` | PayPal |

### region (4개)
| 컬럼 | 원본값 |
|------|--------|
| `region_East` | East |
| `region_North` | North |
| `region_South` | South |
| `region_West` | West |

---

## 이탈(churned=1) 고객의 공통 패턴

데이터를 보면 이탈 고객은 다음 특징이 겹친다:
- `risk_score` = 3~4 (플래그 대부분 해당)
- `support_rate` > 0.5 (월평균 0.5건 이상 티켓)
- `relative_inactivity` > 5 (재직기간 대비 오래 미접속)
- `contract_type_Monthly = True` (월간 계약)
- `tenure_months` ≤ 12 (단기 고객)

반대로 유지 고객은 `risk_score = 0`, `engagement_score` 높음, Annual 계약 비율이 높다.

---

## 관련 파일

| 파일 | 설명 |
|------|------|
| `customer_churn_raw.csv` | 원본 데이터 |
| `customer_churn_raw_explain.md` | 원본 데이터 설명 |
| `prompt.md` | 피처 엔지니어링 작업 요건 |
| `파생_피처.md` | 파생 피처 일반론 정리 |
