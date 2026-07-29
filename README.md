# python-restaurant-recommend-project

## 광운대학교 제2회 파이썬 SW 활용 경진대회

학교 주변 데이터 분석을 통한 맞춤형 음식점 추천 플랫폼 개발

본 플랫폼은 광운대학교 주변 음식점 데이터를 수집·분석하고, 사용자의 상황과
선호도를 입력받아 가장 적합한 음식점을 추천하는 맞춤형 음식점 추천 플랫폼입니다.

---

# 업데이트 내역

- 26.07.26. 첫 번째 릴리즈
- 26.07.27. 추천 음식점 지도 표시 기능 추가
- 26.07.29. 최종 릴리즈

---

# 프로젝트 소개

본 프로젝트는 단순한 음식점 검색 프로그램을 넘어, 사용자의 조건을 분석하여 개인 맞춤형
식사 선택을 지원하는 것을 목표로 한다.

- 학교 주변 음식점 정보를 통합하여 데이터베이스 구축
- 음식점의 가격, 거리, 음식 종류, 평점 등의 데이터 수집 및 전처리
- 사용자의 선호 조건을 반영한 맞춤형 추천 알고리즘 구현
- Python을 활용한 데이터 분석 및 AI 추천 시스템 개발
- 학생들이 실제로 사용할 수 있는 실용적인 프로그램 구현

---

# UI

## 입력
<img width="1351" height="737" alt="UI_1" src="https://github.com/user-attachments/assets/2a9d123c-14ed-41f3-a00e-7e7eb681012f" />

## 음식점 추천 결과
<img width="1350" height="776" alt="UI_2" src="https://github.com/user-attachments/assets/511a6a10-268e-486c-8dd5-24c3c8a91569" />

## 지도 표시
<img width="1350" height="668" alt="UI_3" src="https://github.com/user-attachments/assets/f58fa8ad-b7d8-4ac0-a7b6-0d9e3692e853" />

---

# 사용법

### 바로 접속
사이트 URL

### 로컬 실행
1. 가상환경을 만들고 활성화합니다.
2. `pip install -r requirements.txt` 실행해서 필요 패키지 설치   <!-- 영문 자판으로 바꾸고 백틱 안에 코드 입력 -->
3. crawler.py를 실행해서 restaurant.csv를 생성합니다.
4. menu_collector.py를 실행해서 restaurant_menu.csv를 생성합니다.
5. `streamlit run app.py`를 실행하면 브라우저에서 작동됩니다.

---

# 주요 기능

## 음식점 추천 기능
- app.py에서 음식점 조건을 입력하면 recommend.py에서 추천 알고리즘이 작동돼 음식점을 5순위까지 출력

## 지도 표시 기능
- 추천 음식점의 위치를 지도 위에 마커로 표시
- 오류 수정 중

---

# 기술 스택

| 분야 | 기술 |
|---|---|
| Language | Python |
| Framework | Streamlit |
| Database | CSV |
| Version Control | Git & GitHub |
| Smart Analysis | Self AI Model |

---

# 시스템 구조

### 실행 구조
<img width="1920" height="1080" alt="project_structure" src="https://github.com/user-attachments/assets/706aa4bf-b893-48e6-ab28-e273d47e2151" />

### 화면 설명

| 화면 | 역할 |
|--------|--------|
| Input | 음식 카테고리, 최대 소요 시간 입력 가능 |
| 음식점 추천 | 5순위까지 제공 |
| 음식점 지도 | 추천 음식점 위치 제공 |
