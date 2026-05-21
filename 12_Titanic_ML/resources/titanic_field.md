# Titanic 데이터셋 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `PassengerId` | int | 승객 고유 ID |
| `Survived` | int | 생존 여부 (0=사망, 1=생존) — **타겟** |
| `Pclass` | int | 객실 등급 (1=1등석, 2=2등석, 3=3등석) |
| `Name` | str | 승객 이름 (호칭 포함: Mr, Mrs, Miss 등) |
| `Sex` | str | 성별 (male / female) |
| `Age` | float | 나이 (결측값 있음) |
| `SibSp` | int | 함께 탑승한 형제자매/배우자 수 |
| `Parch` | int | 함께 탑승한 부모/자녀 수 |
| `Ticket` | str | 티켓 번호 |
| `Fare` | float | 운임 요금 |
| `Cabin` | str | 객실 번호 (결측값 매우 많음) |
| `Embarked` | str | 탑승 항구 (C=Cherbourg, Q=Queenstown, S=Southampton) |

## 비고

- **ML 주요 피처:** `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, `Embarked`
- **고결측 필드:** `Age` (~20%), `Cabin` (~77%)
