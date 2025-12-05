# ---------------------------------------------------------
# Simple Query Node
# ---------------------------------------------------------
# 단순 메타데이터 조회 전용 노드
# Economic/Production 분석 없이 빠른 정보 조회

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sqlite3
import pandas as pd


def simple_query_node(state, llm, economic_db="economic_data.db", production_db="production_data.db"):
    """
    단순 메타데이터 조회를 위한 노드
    - Operator, License-Block, Asset 등 기본 정보 조회
    - 리스트, 카운트 등 단순 통계
    - LLM을 최소한으로 사용
    
    Args:
        state: State 객체 (question 필드 포함)
        llm: LLM 인스턴스
        economic_db: Economic 데이터베이스 경로
        production_db: Production 데이터베이스 경로
        
    Returns:
        dict: {"answer": str} 형태의 결과
    """
    print("Simple Query Node 실행 중...")
    
    question = state["question"]
    
    # 두 데이터베이스에서 모두 조회
    all_data = []
    
    try:
        # Economic DB 조회
        conn_eco = sqlite3.connect(economic_db)
        df_eco = pd.read_sql_query("SELECT * FROM economic_data LIMIT 1000", conn_eco)
        df_eco['source_db'] = 'Economic'
        conn_eco.close()
        all_data.append(df_eco)
        print(f"Economic DB: {len(df_eco)} 행 조회")
    except Exception as e:
        print(f"Economic DB 조회 오류: {e}")
    
    try:
        # Production DB 조회
        conn_prod = sqlite3.connect(production_db)
        df_prod = pd.read_sql_query("SELECT * FROM production_data LIMIT 1000", conn_prod)
        df_prod['source_db'] = 'Production'
        conn_prod.close()
        all_data.append(df_prod)
        print(f"Production DB: {len(df_prod)} 행 조회")
    except Exception as e:
        print(f"Production DB 조회 오류: {e}")
    
    # 데이터 통합
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 질문에서 키워드 추출하여 필터링
        question_lower = question.lower()
        filtered_df = combined_df.copy()
        
        # 국가 필터링
        countries = ['indonesia', 'malaysia', 'vietnam', 'thailand', 'philippines', 
                    'brunei', 'myanmar', 'cambodia', 'singapore']
        for country in countries:
            if country in question_lower:
                filtered_df = filtered_df[filtered_df['Country'].str.contains(country, case=False, na=False)]
                break
        
        # Operator 필터링 (질문에 회사명이 있을 경우)
        if 'operator' in filtered_df.columns:
            operators = filtered_df['Operator'].unique()
            for op in operators:
                if op and str(op).lower() in question_lower:
                    filtered_df = filtered_df[filtered_df['Operator'].str.contains(op, case=False, na=False)]
                    break
        
        # License-Block 필터링 (질문에서 블록 키워드 추출)
        if 'License-Block' in filtered_df.columns:
            # 질문에서 블록 관련 단어 추출 (block, cepu, 등)
            import re
            # 블록 이름으로 보이는 단어 추출 (대문자로 시작하거나 특수문자 포함)
            potential_blocks = re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z0-9/-]+\b', question)
            
            for block_keyword in potential_blocks:
                if block_keyword and len(block_keyword) > 2:  # 너무 짧은 단어 제외
                    mask = filtered_df['License-Block'].str.contains(block_keyword, case=False, na=False)
                    if mask.any():
                        filtered_df = filtered_df[mask]
                        print(f"License-Block 필터 적용: {block_keyword}")
                        break
        
        # Asset 필터링
        if 'Asset' in filtered_df.columns:
            assets = filtered_df['Asset'].unique()
            for asset in assets:
                if asset and str(asset).lower() in question_lower:
                    filtered_df = filtered_df[filtered_df['Asset'].str.contains(asset, case=False, na=False)]
                    break
        
        # 결과가 너무 많으면 제한
        if len(filtered_df) > 100:
            filtered_df = filtered_df.head(100)
        
        # 데이터를 텍스트로 변환
        if len(filtered_df) > 0:
            # 중요 컬럼만 선택
            important_cols = ['Country', 'Operator', 'License-Block', 'Asset', 
                            'Start-up Year', 'Contract Expiry Date', 'Commerciality']
            available_cols = [col for col in important_cols if col in filtered_df.columns]
            
            docs_text = filtered_df[available_cols].drop_duplicates().to_string()
            print(f"필터링된 데이터: {len(filtered_df)} 행")
        else:
            docs_text = "검색 조건에 맞는 데이터를 찾을 수 없습니다."
    else:
        docs_text = "데이터베이스 조회에 실패했습니다."
    
    # 간단한 프롬프트로 답변 생성
    prompt = ChatPromptTemplate.from_template(
        """
        당신은 데이터베이스 정보 조회 도우미입니다.
        아래 데이터에서 질문에 대한 답을 찾아 간결하게 답변하세요.
        
        질문이 다음과 같은 유형이면 해당 방식으로 답변하세요:
        - "누구", "운영사", "Operator" → Operator 이름 나열
        - "블록", "License-Block" → License-Block 이름 나열
        - "자산", "Asset" → Asset 이름 나열
        - "개수", "몇 개" → 개수 세기
        - "리스트", "목록" → 리스트 형태로 나열
        - "계약 만료일", "언제" → 날짜 정보 제공
        
        --- 데이터 ---
        {context}
        
        --- 질문 ---
        {question}
        
        답변은 간결하고 명확하게 작성하세요.
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "context": docs_text,
        "question": question
    })
    
    return {"answer": answer}

