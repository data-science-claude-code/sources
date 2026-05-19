# Basecamp Brew Co. -- 비즈니스 분석 프로젝트

## 프로젝트 개요

Basecamp Brew Co.는 소규모 수제 커피 회사로, 이 워크스페이스는 해당 비즈니스 분석을 위한 공간입니다. 12개월간의 판매 및 고객 데이터를 분석하여 트렌드, 문제점, 기회 요인을 파악합니다.

## 비즈니스 소개

Basecamp Brew Co.는 온라인 스토어, 시내 매장, 쇼핑몰 키오스크, 계절 농산물 직판장(파머스 마켓) 등 4개 채널을 통해 커피 음료, 원두, 굿즈를 판매합니다. 운영 기간은 1년입니다.

## 규칙

- 분석을 시작하기 전에 항상 명확화 질문을 먼저 합니다.
- 분석 방법론을 제시하고 무엇을 찾고 있는지 설명합니다.
- 막연한 표현 대신 데이터의 실제 수치를 사용합니다.
- 모든 금액은 달러 기호($)와 쉼표를 포함한 형식으로 표기합니다.
- 이상하거나 예상치 못한 항목은 반드시 표시합니다.
- 단순 관찰에 그치지 않고 구체적인 권고사항을 포함합니다.
- 모든 보고서는 output 폴더에 저장합니다.
- 분석 보고서에 분석 결과는 쉽게 이해할 수 있는 그래프로 시각화(matplotlib)하여 .png 화일로 넣어라.

## 출력 시 필요

```python
# 한글 폰트 설정 (matplotlib)
import matplotlib.font_manager as fm
font_path = r'C:\Windows\Fonts\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
```

## 생성 파일
ipynb(주피터 노트북) 형식으로 소스 파일을 생성한다.

## 프로젝트 구조

- resources/ -- 데이터 파일
- workflows/ -- 분석 워크플로우 파일
- output/ -- 완성된 보고서
