# Asset Analysis AI

지능형 자산 분석 및 보고서 생성 시스템

## 프로젝트 구조

```
Asset Analysis/
├── nodes/                      # 노드별 로직 파일
│   ├── __init__.py
│   ├── router_node.py         # 질문 분류 노드
│   ├── web_search_node.py     # 웹 검색 노드
│   ├── rag_node.py            # RAG 노드 (DB1)
│   ├── rag_node2.py           # RAG 노드 (DB2)
│   ├── integrator_node.py     # 결과 통합 노드
│   └── tool_node.py           # 도구 실행 노드
│
├── templates/                  # Flask 템플릿
│   └── index.html             # 웹 인터페이스
│
├── state.py                    # State 정의
├── config.py                   # 설정 파일 (LLM, DB, API 키 등)
├── workflow.py                 # Workflow 정의
├── app.py                      # Flask 웹 서버
├── main.py                     # 통합 실행 파일 (레거시)
├── .env                        # 환경 변수 (API 키)
└── company_data.db             # SQLite 데이터베이스

```

## 각 노드 설명

### 1. router_node.py
- 사용자 질문을 분석하여 적절한 노드로 라우팅
- simple_query, web_search, vector_rag, vector_rag2, both 중 선택

### 2. simple_query_node.py ⚡ **NEW**
- 단순 메타데이터 조회 전용 노드
- Operator, License-Block, Asset 등 기본 정보 조회
- 리스트, 카운트 등 단순 통계
- **Integrator를 거치지 않고 바로 END로** (빠른 응답)

### 3. web_search_node.py
- Tavily를 사용한 웹 검색
- 최신 정보가 필요한 질문 처리

### 4. rag_node.py (Economic 분석 Agent)
- Economic 데이터베이스에서 데이터 검색 및 분석
- 44,930행의 데이터 (9개국)
- Breakeven Price, IRR, 재정 체제 등 경제 지표 분석

### 5. rag_node2.py (Production 분석 Agent)
- Production 데이터베이스에서 데이터 검색 및 분석
- 31,860행의 데이터 (9개국)
- 생산량 데이터 분석

### 6. integrator_node.py
- 검색 결과를 통합하여 보고서 생성
- 7가지 섹션으로 구성된 보고서 출력

### 7. tool_node.py
- 추가 도구 실행 (워드 파일 생성 등)

## 노드 수정 방법

각 노드는 독립적인 파일로 분리되어 있어 쉽게 수정 가능합니다:

1. `nodes/` 폴더에서 수정하고 싶은 노드 파일 열기
2. 함수 내부 로직 수정
3. 저장 후 서버 재시작

## 실행 방법

1. 환경 변수 설정 (.env 파일)
```
OPENAI_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

2. 웹 서버 실행
```bash
python app.py
```

3. 브라우저에서 접속
```
http://localhost:5000
```

## 데이터베이스 설정

### Economic 데이터베이스 생성
```bash
python setup_economic_db.py
```
- 9개 Economic CSV 파일 → `economic_data.db`
- 총 44,930행

### Production 데이터베이스 생성
```bash
python setup_production_db.py
```
- 11개 Production CSV 파일 → `production_data.db`
- 총 31,860행

### 포함 국가
Indonesia, Malaysia, Vietnam, Thailand, Philippines, Brunei, Myanmar, Cambodia, Singapore

