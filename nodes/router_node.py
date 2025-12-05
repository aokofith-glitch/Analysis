# ---------------------------------------------------------
# Router Node
# ---------------------------------------------------------
# 사용자 질문을 분석하여 다음 중 하나를 결정:
# - web_search
# - vector_rag
# - vector_rag2
# ---------------------------------------------------------

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def router(state):
    """
    기본 router 함수 (현재는 state를 그대로 반환)
    """
    return state


def route_node(state, llm):
    """
    사용자 질문을 분석하여 적절한 노드로 라우팅
    
    Args:
        state: State 객체 (question 필드 포함)
        llm: LLM 인스턴스
        
    Returns:
        str: "web_search", "vector_rag", "vector_rag2" 중 하나
    """
    input_text = state["question"]
    
    route_system_message = """
        당신은 분류기입니다.
        사용자 질문을 다음 중 하나로 분류하세요:
        - simple_query
        - web_search
        - vector_rag
        - vector_rag2
        - both

        반드시 하나만 출력하세요.
        당신은 '질문 분류 전문가'입니다.

1. "simple_query" (최우선 - 단순 정보 조회)
   - "누구", "운영사", "Operator", "who" 등의 질문
   - "블록 목록", "자산 리스트", "list" 등
   - "개수", "몇 개", "how many" 등
   - "계약 만료일", "언제", "when" 등
   - 단순 메타데이터 조회 (분석 불필요)
   예시: "L22/43의 운영사는?", "PTTEP가 운영하는 블록 목록", "태국 자산 개수"

2. "web_search" (최신 정보 우선)
   - "최신", "최신사항", "최근", "뉴스", "현황", "동향", "소식" 등의 키워드
   - "개발 진행", "운영사 변경", "FID", "계약" 등 최신 업데이트 관련
   - 시사/뉴스, 일정, 가격, 주가, 인터넷 검색이 필요한 경우
   - 예시: "Hac Long에 대한 최신사항", "Block A의 최근 개발 현황"

3. "vector_rag"
   - Economic 데이터 분석 관련 질문
   - Breakeven Price, IRR, 재정 체제 등 경제성 분석
   - 명확히 Economic 지표를 언급한 경우

4. "vector_rag2"
   - Production 데이터 분석 관련 질문
   - 생산량, 매장량, 회수율 등 생산 분석
   - 명확히 Production 지표를 언급한 경우

5. "both"
   - 자산/블록/운영사에 대한 종합 분석 요청
   - Economic과 Production 모두 필요한 경우
   - "조사", "분석", "평가", "설명", "리포트", "보고서" 등 포괄적 요청
   - 특정 자산명이 포함되고 구체적 지표를 언급하지 않은 경우
   - **단, "최신", "뉴스", "현황" 등이 있으면 web_search 우선**
   예시: "PTTEP 자산 분석", "Block A-18 조사", "Vorwata, ID의 경제성 분석"

    출력 형식:
    {{
      "route": "simple_query" 또는 "web_search" 또는 "vector_rag" 또는 "vector_rag2" 또는 "both"
    }}

    절대 다른 텍스트를 출력하지 마세요.
        """
    
    # 사용자 메시지 템플릿 정의
    route_user_message = "{question}"
    
    # 프롬프트 템플릿 생성
    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", route_system_message),  # 시스템 메시지
            ("human", route_user_message),      # 사용자 메시지
        ]
    )
    
    chain = route_prompt | llm | JsonOutputParser()
    result = chain.invoke({"question": state["question"]})
    return result["route"]

