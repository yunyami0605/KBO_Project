### 1. KBO_Project

First Mini Project of Python Data Analysis

### 2. 실행 명령어 정리

# PYTHONPATH=. streamlit run app/main.py

1. streamlit run main.py : streamlit 개발 환경 실행
2. python -m scraper.scraper_ex : 루트 기준으로 해당 스크립트 실행

---

### 3. 폴더 구조

.
├── README.md
├── app
│ ├── \__init_.py
│ ├── components
│ ├── main.py
│ └── pages
├── aseets : 리소스 폴더
├── models : 데이터 모델링
├── data : 데이터 저장소
├── requirements.txt
├── scraper : 크롤링 로직
└── libs : util 함수

### 4. 네이밍 규칙

1안

- 파일 네임, 변수, 함수 : snake_case

- 클래스: PascalCase

- 상수: ALL_CAPS

---

### 5. 커밋 메세지 prefix

- feat: 유저 로그인 기능 추가
- fix: 로그인 시 비밀번호 오류 해결
- docs: 환경설정 가이드 추가
- refactor(api): API 요청 방식 개선
- chore: 패키지 정리 및 의존성 업데이트

### 6. 브랜치명

- feature/ : 새로운 기능 설명
- fix/ : 버그 수정
- refactor/ : 코드 리팩토링 (기능 변화 없음)
- chore/ : 환경 설정, 패키지, 문서 등
- docs/ : 문서 관련 수정
