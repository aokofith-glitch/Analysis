# 📊 Vantage PDF 파일 종합 분석 보고서

**분석 날짜**: 2025-12-05  
**분석 파일 수**: 4개  
**제공처**: S&P Global Commodity Insights (Vantage)

---

## 📑 1. 파일 개요

| 파일명 | 타입 | 페이지 | 자수 | 대상 |
|--------|------|--------|------|------|
| Vantage_Cepu PSC_AssetReport_2025-12-04.pdf | Asset Report | 50 | 92,463 | Cepu PSC (Indonesia) |
| Vantage_Peudawa_AssetReport_2025-12-04.pdf | Asset Report | 10 | 17,230 | Peudawa (Indonesia) |
| Vantage_Fatimah_FieldReport_2025-12-04.pdf | Field Report | 16 | 14,878 | Fatimah (Malaysia) |
| Vantage_Lawang_FieldReport_2025-12-04.pdf | Field Report | 22 | 20,280 | Lawang (Malaysia) |

---

## 🎯 2. 문서 타입별 특징

### 📘 Asset Report (자산 보고서)
**목적**: 자산 전체에 대한 경제성, 투자, 밸류에이션 분석

**특징**:
- 평균 **30페이지** (더 방대함)
- **다중 필드** 포함 가능 (예: Cepu PSC는 Banyu Urip, Kedung Keris 등 포함)
- **경제/재무 중심** 분석

**주요 섹션**:
1. **Asset Summary** - 자산 요약
2. **Asset Overview** - 자산 개요
3. **Investment** - 투자 분석 (CAPEX, OPEX, Decommissioning)
4. **Valuation** - 가치평가 (NPV @ 10% discount rate)
5. **Emissions** - 배출량 데이터 및 강도
6. **Economic Scenarios** - 경제 시나리오 (Base, High, Low)
7. **Production** - 생산 프로필 및 예측
8. **Resources** - 자원량 (Remaining, Initial)
9. **Cost Analysis** - BOE당 비용 분석
10. **Participation History** - 지분 변동 이력

**데이터 중심**:
- F&D Cost (Finding & Development)
- Operating Cost per BOE
- NPV 계산
- IRR (Internal Rate of Return)
- Economic forward production profiles
- Emissions intensity metrics

---

### 📗 Field Report (필드 보고서)
**목적**: 단일 필드에 대한 지질학적, 기술적 상세 분석

**특징**:
- 평균 **19페이지** (더 집중적)
- **단일 필드** 집중
- **지질학/엔지니어링 중심** 분석

**주요 섹션**:
1. **Field Summary Report** - 필드 요약
2. **General Field Data** - 일반 필드 데이터
3. **Location** - 위치 (좌표 포함)
4. **Ownership Details** - 소유권 상세
5. **Discovery and Drilling History** - 발견 및 시추 이력
6. **Well Statistics** - 시추공 통계
7. **Well Tests** - 시추공 테스트 데이터
8. **Events** - 주요 이벤트 타임라인
9. **Field Development** - 필드 개발 계획
10. **Cumulative Production** - 누적 생산량
11. **Reserves History** - 매장량 변동 이력
12. **Reservoirs** - 저류층 분석
13. **Main Reservoir Structure** - 주 저류층 구조
14. **Reservoir Traps** - 트랩 유형
15. **Reservoir Seal** - 실링 메커니즘
16. **Source Rocks** - 근원암 분석
17. **Oil/Gas Analysis** - 유체 분석
18. **Images** - 지도 및 다이어그램
19. **Field Bibliography** - 참고문헌

**데이터 중심**:
- 저류층 특성 (lithology, depth, porosity, permeability)
- 좌표 (lat/long)
- 수심 (offshore인 경우)
- 지층 연대 (stratigraphic age)
- 시추공별 상세 데이터
- 생산 테스트 결과

---

## 🔍 3. 공통 데이터 필드 (모든 PDF 공통)

### ✅ 모든 문서에 포함된 필수 필드:

| 필드명 | 설명 | 예시 |
|--------|------|------|
| **Asset/Field Name** | 자산 또는 필드 이름 | Cepu PSC, Fatimah |
| **Country** | 국가 | Indonesia, Malaysia |
| **Basin** | 분지 | Cepu Sub-basin, Baram Delta |
| **Operator** | 운영사 | ExxonMobil, EnQuest |
| **Status** | 생산 상태 | Producing, Developing, Shut-in |
| **Year Discovered** | 발견 연도 | 1904, 1980, 1991, 1998 |
| **HC Type** | 탄화수소 타입 | Oil, Gas, Oil,gas |
| **Remaining Oil Resources** | 남은 석유 자원 (MMbbl) | 273.52, 34.00 |
| **Remaining Gas Resources** | 남은 가스 자원 (Bcf/MMscf) | 274.47, 177,000 |

### 📊 Asset Report 전용 필드:

- **Investment**: CAPEX, OPEX, Decommissioning costs
- **Valuation**: NPV (at various discount rates)
- **Emissions**: CO2 intensity, total emissions
- **F&D Cost**: Finding & Development cost per BOE
- **Economic Scenarios**: Base, High, Low case projections

### 🌍 Field Report 전용 필드:

- **Coordinates**: Latitude/Longitude (정확한 좌표)
- **Water Depth**: 수심 (offshore)
- **Reservoir Depth**: 저류층 깊이
- **Lithology**: 암상 (sandstone, limestone, carbonate)
- **Well Count**: 시추공 개수
- **Reservoir Properties**: Porosity, permeability, net pay
- **Trap Type**: 트랩 유형 (Structural, Stratigraphic)

---

## 📐 4. 문서 구조 패턴

### 공통 구조 (모든 PDF):

```
1. 표지/제목 페이지
   - 자산/필드명
   - 생성일자
   - 위치 정보
   - 주요 수치 요약

2. 요약 섹션 (Summary)
   - 핵심 데이터 박스
   - 주요 지표

3. 상세 섹션
   [Asset Report]
   - Investment & Economics
   - Valuation
   - Production profiles
   - Emissions
   
   [Field Report]
   - Geology & Reservoirs
   - Wells & History
   - Development plans
   - Images & Maps

4. 데이터 테이블
   - 연도별 생산/투자 데이터
   - 시나리오별 비교
   - 히스토리 테이블

5. 부록/참고자료
   - 지도
   - 그래프
   - 참고문헌
```

---

## 🔑 5. 주요 발견 사항

### 📌 데이터 일관성:
- **표준화된 형식**: 모든 Vantage 문서는 동일한 템플릿 사용
- **일관된 단위**: MMbbl, Bcf, MMboe, boe/d 등 표준 석유 단위
- **구조화된 데이터**: Key-Value 쌍으로 정보 제공

### 📌 문서 목적:
- **Asset Report**: 투자자/경영진 대상 (경제성 분석)
- **Field Report**: 기술자/지질학자 대상 (기술적 분석)

### 📌 데이터 품질 표시:
- "Poor estimate", "Estimate within 50%" 등 신뢰도 표시
- 데이터 출처 명시 (EDIN, Vantage)

### 📌 시간적 범위:
- **과거 데이터**: Discovery부터 현재까지 이력
- **현재 데이터**: 현재 생산/자원 상태
- **미래 예측**: 생산 프로필, 투자 계획

---

## 🎨 6. 데이터 추출 가능성 분석

### ✅ 쉽게 추출 가능한 데이터:

1. **메타데이터**
   - Asset/Field 이름
   - 위치 (국가, 분지)
   - 운영사
   - 발견 연도
   - 생산 상태

2. **자원량 데이터**
   - Remaining/Initial recoverable resources
   - Oil (MMbbl)
   - Gas (Bcf)
   - BOE equivalents

3. **경제 데이터** (Asset Report)
   - CAPEX, OPEX
   - NPV
   - Cost per BOE

4. **생산 데이터**
   - 생산 개시일
   - 누적 생산량
   - 현재 생산율

### ⚠️ 추출이 어려운 데이터:

1. **표 형식 데이터**
   - 연도별 상세 데이터 (표로 구성)
   - PDF에서 표 파싱이 필요

2. **그래프/차트**
   - 이미지로 embedded
   - OCR이나 이미지 처리 필요

3. **복잡한 계층 구조**
   - 다중 필드 자산의 개별 필드 데이터
   - 여러 시나리오의 개별 값

---

## 💡 7. 활용 방안

### 현재 프로젝트 (Asset Analysis) 활용:

1. **RAG 시스템에 통합**
   - 4개 PDF를 vector store에 저장
   - 자산/필드별 질의응답 가능
   - "Cepu PSC의 remaining oil은?" → "273.52 MMbbl"

2. **데이터베이스 보강**
   - 기존 Rystad 데이터와 교차 검증
   - 자산별 상세 정보 추가
   - 운영사, 지분 정보 보완

3. **경제 분석 강화**
   - Investment 데이터로 경제성 분석
   - NPV, IRR 데이터 활용
   - 시나리오 분석 가능

4. **Production Forecasting**
   - Historical production + forecast 데이터
   - 생산 감퇴율 분석
   - Field life 예측

### 추가 가능한 기능:

1. **자산 비교 분석**
   - 4개 자산 간 경제성 비교
   - 지역별 특성 분석
   - 운영사별 성과 비교

2. **자동 보고서 생성**
   - PDF에서 핵심 데이터 추출
   - 요약 리포트 자동 생성
   - 대시보드 데이터 피드

3. **트렌드 분석**
   - 발견 → 개발 → 생산 → 감퇴 life cycle
   - 투자 패턴 분석
   - 기술 발전 추적

---

## 📋 8. 데이터 구조 요약

### Asset Report 핵심 구조:
```
Asset Report
├── Metadata
│   ├── Asset Name
│   ├── Operator
│   ├── Location (Country, Basin)
│   ├── Status
│   └── Discovery Year
├── Resources
│   ├── Remaining (Oil, Gas)
│   ├── Initial (Oil, Gas)
│   └── Recovery Factor
├── Investment
│   ├── CAPEX
│   ├── OPEX
│   ├── Decommissioning
│   └── Total Costs
├── Valuation
│   ├── NPV (10% discount)
│   ├── IRR
│   └── Economic Scenarios
├── Production
│   ├── Historical
│   ├── Current
│   └── Forecast
└── Emissions
    ├── Total CO2
    └── Intensity (kg CO2/boe)
```

### Field Report 핵심 구조:
```
Field Report
├── Metadata
│   ├── Field Name
│   ├── Operator
│   ├── Location (Coordinates)
│   ├── Status
│   └── Discovery Date
├── Resources
│   ├── Recoverable (Oil, Gas)
│   └── Cumulative Production
├── Geology
│   ├── Basin & Structure
│   ├── Reservoir Characteristics
│   ├── Lithology
│   ├── Depth
│   └── Trap Type
├── Wells
│   ├── Discovery Well
│   ├── Well Statistics
│   ├── Well Tests
│   └── Drilling History
├── Development
│   ├── Field Development Plan
│   ├── Facilities
│   └── Infrastructure
└── History
    ├── Ownership Changes
    ├── Major Events
    └── Production History
```

---

## 🎯 9. 핵심 인사이트

### 문서 품질:
- ✅ **매우 구조화됨**: 파싱하기 좋은 형식
- ✅ **데이터 풍부**: 다양한 기술/경제 데이터
- ✅ **표준화됨**: Vantage 표준 템플릿 사용
- ⚠️ **일부 표 데이터**: 복잡한 파싱 필요

### 활용 가능성:
- 🟢 **즉시 활용 가능**: 메타데이터, 자원량, 기본 경제 데이터
- 🟡 **일부 처리 필요**: 표 형식 데이터, 시계열 데이터
- 🔴 **추가 처리 필요**: 그래프, 이미지, 복잡한 레이아웃

### 프로젝트 통합:
현재 `pdf_reader_node.py`를 통해 이러한 PDF를 파싱하고,
RAG 시스템에 통합하여 사용자 질의에 답변할 수 있습니다.

---

## 📊 10. 통계 요약

| 항목 | 값 |
|------|-----|
| **총 페이지 수** | 98 페이지 |
| **총 문자 수** | 144,851 자 |
| **평균 페이지/문서** | 24.5 페이지 |
| **Asset Report 평균** | 30 페이지 |
| **Field Report 평균** | 19 페이지 |
| **가장 큰 문서** | Cepu PSC (50페이지) |
| **가장 작은 문서** | Peudawa (10페이지) |

### 데이터 커버리지:
- 🌏 **국가**: 2개 (Indonesia, Malaysia)
- 🏢 **운영사**: 4개 (ExxonMobil, Dialog Resources, EnQuest, Unlicensed)
- 🛢️ **자산 상태**: Producing (2), Developing (1), Shut-in (1)
- 📅 **발견 연도 범위**: 1904~1998 (94년 span)
- 💰 **총 잔여 자원**: ~307 MMbbl oil, ~476 Bcf gas

---

**분석 완료일**: 2025-12-05  
**분석 도구**: PyPDF2, Python 3.x  
**분석자**: AI Assistant

