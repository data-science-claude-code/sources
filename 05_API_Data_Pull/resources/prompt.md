# API 데이터 수집 프롬프트

## 주요 실습 — yfinance (야후 파이낸스)

yfinance 라이브러리를 사용하여 다음 5개 기업의 최근 1년간 일별 주가 데이터를 수집하세요: Apple (AAPL), Microsoft (MSFT), Google (GOOGL), Amazon (AMZN), Tesla (TSLA).

이후 아래 작업을 수행하세요:
1. 모든 데이터를 ticker 컬럼이 포함된 단일 pandas DataFrame으로 불러오기
2. 각 주식의 요약 통계(종가의 평균, 최솟값, 최댓값) 출력
3. 각 주식의 30일 이동평균 종가 계산
4. 전체 기간 동안 5개 종목의 종가를 나타내는 꺾은선 차트 생성
5. 해당 기간 동안 가장 높은 수익률(%)을 기록한 종목 찾기
6. 원본 데이터를 stock_data.csv로 저장

필요한 경우 yfinance 설치: pip install yfinance

---

## 대안 옵션 1 — CoinGecko (암호화폐, API 키 불필요)

CoinGecko API에서 시가총액 기준 상위 20개 암호화폐 데이터를 수집하세요.
엔드포인트: https://api.coingecko.com/api/v3/coins/markets
파라미터: vs_currency=usd&order=market_cap_desc&per_page=20&page=1

DataFrame으로 불러온 후, 시가총액 막대 차트를 생성하고 crypto_data.csv로 저장하세요.

---

## 대안 옵션 2 — 세계은행 (경제 지표, API 키 불필요)

미국, 중국, 영국, 독일, 인도의 최근 10년간 1인당 GDP 데이터를 수집하세요.
엔드포인트: https://api.worldbank.org/v2/country/{국가코드}/indicator/NY.GDP.PCAP.CD?format=json&date=2014:2024

DataFrame으로 불러온 후, 국가별 GDP 추이를 그래프로 시각화하고 gdp_data.csv로 저장하세요.

---

## 대안 옵션 3 — NASA 근지구 천체 (api.nasa.gov에서 무료 API 키 발급)

최근 7일간의 근지구 소행성 데이터를 수집하세요.
엔드포인트: https://api.nasa.gov/neo/rest/v1/feed?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&api_key=YOUR_KEY

소행성 이름, 크기, 속도, 지구 접근 거리를 표시하는 DataFrame을 생성하고, 잠재적으로 위험한 소행성을 표시하세요.

---

## 대안 옵션 4 — Open-Meteo 과거 날씨 데이터 (API 키 불필요)

과거 데이터 엔드포인트: https://archive-api.open-meteo.com/v1/archive
다음 도시들의 최근 30일간 일별 최고기온, 최저기온, 강수량, 풍속 데이터를 수집하세요:
- 뉴욕: lat=40.7128, lon=-74.0060
- 로스앤젤레스: lat=34.0522, lon=-118.2437
- 시카고: lat=41.8781, lon=-87.6298
- 휴스턴: lat=29.7604, lon=-95.3698
- 마이애미: lat=25.7617, lon=-80.1918
