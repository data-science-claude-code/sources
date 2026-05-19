# 데이터 정제 프롬프트

messy_customer_data.csv라는 지저분한 고객 데이터셋이 있습니다. 다음 항목들을 완전히 정제해 주세요:
- customer_name을 Title Case(단어 첫 글자 대문자)로 통일
- 이메일 형식을 수정 및 검증하고, 유효하지 않은 항목에 플래그 표시
- 전화번호를 (XXX) XXX-XXXX 형식으로 통일
- 모든 signup_date 값을 YYYY-MM-DD 형식으로 통일
- Annual_Revenue 정제 — $ 기호와 쉼표 제거 후 float으로 변환
- Country를 국가 전체 이름으로 통일
- Age 수정 — 불가능한 값(0 미만 또는 120 초과) 제거 후 정수로 변환
- is_active를 불리언 True/False로 통일
- 중복 행 제거

정제 전/후 비교를 보여주고, 정제된 데이터를 cleaned_customer_data.csv로 저장해 주세요

코드를 ipynb(주피터노트북 형식)으로 생성해라
