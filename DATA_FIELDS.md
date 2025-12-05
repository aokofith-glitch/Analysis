# 데이터 필드 설명

## 공통 필드 (Economic & Production 공통)

| 필드 | 설명 |
|------|------|
| **Country** | 국가 |
| **Operator** | 운영사 |
| **License-Block** | 라이선스 블록 |
| **Asset** | 자산 |
| **Start-up Year** | 시작 연도 |
| **Contract Expiry Date** | 계약 만료일 |
| **Commerciality** | 상업성 |

---

## Economic 데이터 중요 지표

### rag_node (Economic Agent)에서 분석

| 지표 | 설명 |
|------|------|
| **Breakeven Oil Price** | 손익분기 유가 - 프로젝트가 손익분기점에 도달하는 유가 |
| **Breakeven Gas Price** | 손익분기 가스가 - 프로젝트가 손익분기점에 도달하는 가스가 |
| **Internal Rate Of Return (IRR)** | 내부수익률 - 투자 수익성 지표 |
| **Payback Years** | 회수 기간 - 투자 회수에 걸리는 연수 |
| **Fiscal Regime Group** | 재정 체제 그룹 - PSC, Concession 등 |

**데이터베이스**: `economic_data.db`
**총 데이터**: 44,930행 (9개국)

---

## Production 데이터 중요 지표

### rag_node2 (Production Agent)에서 분석

| 지표 | 설명 |
|------|------|
| **Original Gas In Place** | 원시 가스 부존량 - 유전에 원래 존재하는 가스의 총량 |
| **Field recovery factor** | 유전 회수율 - 회수 가능한 비율 (%) |
| **Technical recoverable resources** | 기술적 회수 가능 자원 - 기술적으로 회수 가능한 자원량 |
| **2P Reserves** | 2P 매장량 - Proved + Probable 매장량 |
| **Discovered Resources** | 발견된 자원 - 발견된 자원량 |
| **Production** | 생산량 - 실제 생산된 양 |

**데이터베이스**: `production_data.db`
**총 데이터**: 31,860행 (9개국)

---

## 데이터 구조

각 데이터는 다음과 같은 형식으로 저장됩니다:

```
Country, Operator, License-Block, Asset, Start-up Year, Contract Expiry Date, 
Commerciality, [Data Values], Sum
```

- **[Data Values]**: 측정 지표 이름 (예: "Breakeven Oil Price", "Production")
- **Sum**: 해당 지표의 실제 값

---

## 포함 국가 (9개국)

1. Indonesia (인도네시아)
2. Malaysia (말레이시아)
3. Vietnam (베트남)
4. Thailand (태국)
5. Philippines (필리핀)
6. Brunei (브루나이)
7. Myanmar (미얀마)
8. Cambodia (캄보디아)
9. Singapore (싱가포르)

---

## Agent별 역할

### 1. Router (llm)
- 질문을 분류하여 적절한 Agent로 라우팅
- Economic/Production/Web Search 중 선택

### 2. Economic Agent (llm1, rag_node)
- Economic 지표 분석
- 손익분기점, 수익률, 재정 체제 등 경제성 분석

### 3. Production Agent (llm2, rag_node2)
- Production 데이터 분석
- 생산량, 매장량, 회수율 등 생산 관련 분석

### 4. Web Search Agent (llm3)
- 최신 정보 검색
- 인터넷 실시간 데이터 조회

### 5. Integrator (llm4)
- 모든 Agent의 결과를 통합
- 종합 보고서 생성

