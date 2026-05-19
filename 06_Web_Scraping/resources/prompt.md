# 웹 스크래핑 프롬프트

## 주요 실습 — 위키피디아 (매출 기준 세계 최대 기업 목록)

아래 위키피디아 페이지를 스크래핑하세요:
https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue

기업명, 순위, 매출, 영업이익, 직원 수, 산업, 국가가 포함된 메인 테이블을 추출합니다.

이후 아래 작업을 수행하세요:
1. 데이터를 깔끔한 pandas DataFrame으로 불러오기
2. 매출 기준 상위 10개 기업 출력
3. 매출 기준 상위 15개 기업 막대 차트 생성
4. 국가별 그룹화 — 어느 나라가 목록을 지배하는가?
5. 산업별 그룹화 — 어느 산업이 가장 높은 총매출을 기록하는가?
6. 정제된 데이터를 largest_companies_scraped.csv로 저장

숫자의 서식 문제(쉼표, 통화 기호 등)를 처리하세요.

---

## 대안 옵션 1 — Basketball Reference (NBA 통계)

아래 페이지에서 2023-24 NBA 선수 경기당 스탯 테이블을 스크래핑하세요:
https://www.basketball-reference.com/leagues/NBA_2024_per_game.html

선수명, 팀, 포지션, 경기당 득점, 어시스트, 리바운드, 슈팅 %를 추출합니다.
데이터를 정제하고, 득점 상위 20명을 찾아 막대 차트를 그리세요. nba_stats.csv로 저장합니다.

---

## 대안 옵션 2 — Books to Scrape (스크래핑 연습용 사이트)

https://books.toscrape.com 의 모든 페이지(페이지네이션 필요)에서 전체 도서를 스크래핑하세요.
모든 책의 제목, 가격, 평점, 재고 여부를 추출합니다.
평점 상위 10권 도서, 평점별 평균 가격을 구하고, books_scraped.csv로 저장합니다.
페이지네이션 처리 방법을 보여주기에 적합합니다.

---

## 대안 옵션 3 — Worldometers (국가별 인구 통계)

아래 페이지에서 세계 인구 테이블을 스크래핑하세요:
https://www.worldometers.info/world-population/population-by-country/

국가, 인구, 연간 변화율(%), 순변화, 인구 밀도, 국토 면적을 추출합니다.
인구 상위 20개국을 찾아 막대 차트를 그리고, population_data.csv로 저장합니다.

---

## 촬영 참고 사항
- 위키피디아가 가장 깔끔한 실습 — 구조화된 HTML 테이블, JS 렌더링 문제 없음, 즉각적인 결과
- Basketball Reference는 데이터 사이언스 수강생에게 가장 흥미로운 데이터
- Books to Scrape는 카메라 앞에서 페이지네이션 처리를 보여주고 싶을 때 최적
- 봇 차단이 강한 사이트 스크래핑 지양 (Reddit, LinkedIn, Amazon 상품 페이지 등)
