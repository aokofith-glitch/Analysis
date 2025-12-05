# ---------------------------------------------------------
# RAG Node (Economic 분석 Agent)
# ---------------------------------------------------------
# Economic 데이터를 검색하고 분석하는 Agent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sqlite3
import pandas as pd
import json
import re


def rag_node(state, llm, db_path="economic_data.db", table_name="economic_data"):
    """
    Economic 데이터베이스에서 데이터를 검색하고 분석 답변 생성
    
    Args:
        state: State 객체 (question 필드 포함)
        llm: LLM 인스턴스
        db_path: SQLite 데이터베이스 경로 (기본값: economic_data.db)
        table_name: 검색할 테이블 이름 (기본값: economic_data)
        
    Returns:
        dict: {"answer": str, "documents": list, "raw_data": dict} 형태의 결과
    """
    print("Economic 분석 Agent 실행 중...")

    # 질문에서 출력 모드 감지 (JSON_MODE vs REPORT_MODE)
    question_lower = state["question"].lower()
    is_json_mode = "json" in question_lower or "json_mode" in question_lower
    is_report_mode = "report" in question_lower or "report_mode" in question_lower
    
    # LLM을 사용하여 자산명 추출
    def extract_asset_name(question):
        """LLM을 사용하여 질문에서 자산명을 추출"""
        extraction_prompt = f"""
다음 질문에서 Oil & Gas 자산명(Asset/Field/Block)만 추출하세요.

질문: {question}

규칙:
1. 자산명만 출력 (괄호 안 별칭 제외)
2. 국가 코드 제외 (VN, ID, MY 등)
3. 여러 단어로 된 자산명은 전체를 하나로 출력
4. 자산명이 없으면 "NONE" 출력

예시:
- "Hac Long (Black Dragon), VN 분석해줘" → "Hac Long"
- "Block B & 48/95 조사" → "Block B & 48/95"
- "Cepu Block, ID" → "Cepu"
- "태국 자산 분석" → "NONE"

자산명:"""
        
        try:
            from langchain_core.messages import HumanMessage
            response = llm.invoke([HumanMessage(content=extraction_prompt)])
            asset_name = response.content.strip().strip('"').strip("'")
            if asset_name and asset_name != "NONE":
                print(f"  [LLM 추출] 자산명: '{asset_name}'")
                return asset_name
        except Exception as e:
            print(f"  [LLM 추출 오류] {e}")
        return None
    
    # SQLite에서 데이터 조회
    raw_rows = []
    try:
        conn = sqlite3.connect(db_path)
        
        # 자산명 추출 (간단한 패턴 매칭)
        asset_filter = ""
        country_filter = ""
        
        # 소문자 변환 전에 블록명 패턴 먼저 추출
        import re
        block_pattern = re.search(r'Block\s+[A-Z0-9\-/&]+', state["question"])
        
        # 이제 소문자 변환 (국가명 필터용)
        question = state["question"].lower()
        
        # 국가명 필터링
        countries = {
            'indonesia': ['indonesia', '인도네시아', '인니', ', id'],
            'malaysia': ['malaysia', '말레이시아', '말련', ', my'],
            'vietnam': ['vietnam', '베트남', '월남', ', vn'],
            'thailand': ['thailand', '태국', ', th'],
            'philippines': ['philippines', '필리핀', ', ph'],
            'brunei': ['brunei', '브루나이', ', bn'],
            'myanmar': ['myanmar', '미얀마', '버마', ', mm'],
            'cambodia': ['cambodia', '캄보디아', ', kh'],
            'singapore': ['singapore', '싱가포르', ', sg']
        }
        
        for country_name, keywords in countries.items():
            if any(keyword in question for keyword in keywords):
                country_filter = f"Country LIKE '%{country_name.title()}%'"
                print(f"  [인식] 국가 필터: {country_name.title()} (키워드: {[k for k in keywords if k in question]})")
                break
        
        # 자산명 키워드 추출 (Asset, License-Block 등)
        
        # 1단계: LLM으로 자산명 추출 시도
        llm_asset_name = extract_asset_name(state["question"])
        
        if llm_asset_name:
            # LLM이 자산명을 추출한 경우, 정확한 매칭 우선 시도
            asset_keywords = f"(Asset LIKE '%{llm_asset_name}%' OR \"License-Block\" LIKE '%{llm_asset_name}%')"
            if country_filter:
                asset_filter = f"({country_filter}) AND ({asset_keywords})"
            else:
                asset_filter = asset_keywords
        
        # 2단계: Block 패턴 검색 (fallback)
        elif block_pattern:
            # 블록명 전체를 하나의 키워드로 사용
            block_name = block_pattern.group().strip()
            print(f"  [인식] Block 패턴 발견: {block_name}")
            asset_keywords = f"(Asset LIKE '%{block_name}%' OR \"License-Block\" LIKE '%{block_name}%')"
            if country_filter:
                asset_filter = f"({country_filter}) AND ({asset_keywords})"
            else:
                asset_filter = asset_keywords
        
        # 3단계: 대문자 단어 추출 (fallback)
        else:
            words = state["question"].split()
            potential_assets = [w for w in words if w and w[0].isupper() and len(w) > 2]
            print(f"  [인식] 대문자 단어 추출: {potential_assets}")
            
            if potential_assets:
                asset_keywords = " OR ".join([f"(Asset LIKE '%{asset}%' OR \"License-Block\" LIKE '%{asset}%')" 
                                             for asset in potential_assets[:3]])
                if country_filter:
                    asset_filter = f"({country_filter}) AND ({asset_keywords})"
                else:
                    asset_filter = asset_keywords
            elif country_filter:
                asset_filter = country_filter
        
        # 데이터 조회
        where_clause = f" WHERE {asset_filter}" if asset_filter else ""
        query = f"SELECT * FROM {table_name}{where_clause} LIMIT 200"
        print(f"  [쿼리] {query}")
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) == 0:
            # 필터링된 결과가 없으면 전체에서 샘플링
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 100", conn)
            conn.close()
        
        # raw_rows 생성 (Integrator에게 전달할 원본 데이터)
        raw_rows = df.to_dict('records')
        
        # 데이터프레임을 텍스트로 변환
        docs_text = df.to_string()
        documents = [docs_text]
        
        print(f"검색된 데이터: {len(df)} 행")
        
    except Exception as e:
        print(f"DB 조회 오류: {e}")
        docs_text = "데이터베이스에서 정보를 가져올 수 없습니다."
        documents = []

    # 답변 생성 프롬프트 (출력 모드에 따라 분기)
    if is_json_mode:
        prompt_template = """
당신은 Economic 데이터 분석 전문가입니다.
아래 Economic 데이터를 기반으로 JSON 형식으로 분석 결과를 생성하세요.

------------------------------------------------------------
5. Unit 표준화 규칙
------------------------------------------------------------
Oil → USD/bbl  
Gas(kcf) → USD/mcf  
Cost → USD/bbl  
Present Value → Million USD  

------------------------------------------------------------
6. 분석 절차
------------------------------------------------------------
(1) 자산명 식별 (필드/블록/자산 정규화)  
(2) 관련 CSV row 자동 선택  
(3) 경제성 지표 추출 (Breakeven, IRR, Payback, Cost 등)  
(4) 경제성 해석 (특징, 투자가치, 리스크 등)  
(5) Year-by-Year Trend 분석  
(6) Raw Rows 포함 JSON 결과 생성  

------------------------------------------------------------
7. JSON_MODE 최종 출력 형식
------------------------------------------------------------
반드시 아래 형식의 JSON만 출력하세요:

{{
  "asset": "자산명",
  "summary": "자산 요약 (2-3문장)",
  "key_numbers": {{
    "breakeven_oil_usd_bbl": 0.0,
    "breakeven_gas_usd_mcf": 0.0,
    "irr_percent": 0.0,
    "payback_years": 0.0,
    "total_cost_usd_bbl": 0.0,
    "npv_million_usd": 0.0
  }},
  "trend": [
    "연도별 트렌드 인사이트 1",
    "연도별 트렌드 인사이트 2"
  ],
  "insights": [
    "핵심 인사이트 1",
    "핵심 인사이트 2",
    "핵심 인사이트 3"
  ],
  "risks": [
    "리스크 요소 1",
    "리스크 요소 2"
  ],
  "recommendation": "투자 권고사항 (1-2문장)",
  "raw_rows": []
}}

※ raw_rows는 비워두세요. 시스템에서 자동으로 채웁니다.

--- Economic 데이터 ---
{context}

--- 질문 ---
{question}

JSON만 출력하세요. 다른 텍스트는 포함하지 마세요.
"""
    elif is_report_mode:
        prompt_template = """
당신은 Economic 데이터 분석 전문가입니다.
아래 Economic 데이터를 기반으로 상세한 보고서를 작성하세요.

------------------------------------------------------------
5. Unit 표준화 규칙
------------------------------------------------------------
Oil → USD/bbl  
Gas(kcf) → USD/mcf  
Cost → USD/bbl  
Present Value → Million USD  

------------------------------------------------------------
8. REPORT_MODE 출력 형식
------------------------------------------------------------
아래 섹션들을 포함하여 작성하세요:

1. 자산 개요  
   - 자산명, 국가, 운영사, 라이선스 블록
   - 시작 연도, 계약 만료일, 상업성

2. 핵심 경제성 지표  
   - Breakeven Oil Price (USD/bbl)
   - Breakeven Gas Price (USD/mcf)
   - Internal Rate of Return (IRR, %)
   - Payback Years
   - Fiscal Regime Group

3. 비용 구조  
   - Capex (USD/bbl)
   - Opex (USD/bbl)
   - Total Cost (USD/bbl)

4. Present Value  
   - NPV (Million USD)
   - 할인율 정보 (있는 경우)

5. 종합 분석  
   - 경제성 특징
   - 투자 가치 평가
   - Year-by-Year 트렌드

6. M&A Pros/Cons  
   - 장점 (Pros)
   - 단점/리스크 (Cons)

7. Executive Summary  
   - 3-5문장으로 핵심 요약

--- Economic 데이터 ---
{context}

--- 질문 ---
{question}

상세한 보고서를 작성하세요.
"""
    else:
        # 기본 모드 (간단한 답변)
        prompt_template = """
당신은 Economic 데이터 분석 전문가입니다.
아래 Economic 데이터를 기반으로 질문에 답변하세요.

------------------------------------------------------------
Unit 표준화 규칙
------------------------------------------------------------
Oil → USD/bbl  
Gas(kcf) → USD/mcf  
Cost → USD/bbl  
Present Value → Million USD  

데이터에는 다음 정보가 포함되어 있습니다:

[공통 필드]
- Country: 국가
- Operator: 운영사
- License-Block: 라이선스 블록
- Asset: 자산
- Start-up Year: 시작 연도
- Contract Expiry Date: 계약 만료일
- Commerciality: 상업성

[중요 Economic 지표]
- Breakeven Oil Price: 손익분기 유가 (USD/bbl)
- Breakeven Gas Price: 손익분기 가스가 (USD/mcf)
- Internal Rate Of Return (IRR): 내부수익률 (%)
- Payback Years: 회수 기간 (년)
- Fiscal Regime Group: 재정 체제

--- Economic 데이터 ---
{context}

--- 질문 ---
{question}

답변 시 중요 지표(Breakeven Oil/Gas Price, IRR, Payback Years 등)를 
중심으로 구체적인 수치와 단위를 명확히 표시하여 분석해주세요.
"""

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": docs_text,
        "question": state["question"]
    })

    # JSON 모드인 경우, raw_rows를 JSON에 삽입
    if is_json_mode and raw_rows:
        try:
            # JSON 파싱
            json_match = re.search(r'\{.*\}', answer, re.DOTALL)
            if json_match:
                result_json = json.loads(json_match.group())
                result_json["raw_rows"] = raw_rows[:50]  # 최대 50개 행만 포함
                answer = json.dumps(result_json, ensure_ascii=False, indent=2)
            else:
                # JSON 파싱 실패 시 raw_rows를 별도로 추가
                print("Warning: JSON 파싱 실패, raw_rows를 별도로 전달합니다.")
        except Exception as e:
            print(f"JSON 처리 오류: {e}")

    return {
        "answer": answer,
        "documents": documents,
        "raw_rows": raw_rows,  # Integrator에게 전달할 원본 데이터
        "analysis_metadata": {
            "mode": "json" if is_json_mode else ("report" if is_report_mode else "default"),
            "total_rows": len(raw_rows),
            "data_source": table_name
        }
    }

