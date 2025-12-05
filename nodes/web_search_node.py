# ---------------------------------------------------------
# Web Search Node
# ---------------------------------------------------------
# 최신 정보 검색 (운영사 변경, 개발 진행 현황 등)
# 1-2년 이내 정보 중심, 제목과 링크만 간결하게 제공

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime


def web_search_node(state, search_tool, llm):
    """
    웹 검색을 수행하고 결과를 기반으로 답변 생성
    - 운영사 변경 현황
    - 개발 진행 현황
    - Field/Block 관련 최신 뉴스
    - 1-2년 이내 정보 중심
    
    Args:
        state: State 객체 (question 필드 포함)
        search_tool: Tavily 검색 도구
        llm: LLM 인스턴스
        
    Returns:
        dict: {"answer": str} 형태의 결과
    """
    print("웹검색 노드 실행 중...")
    
    question = state["question"]
    current_year = datetime.now().year
    
    # 검색 쿼리 개선 (최근 정보 중심)
    enhanced_query = f"{question} 2023 2024 2025 news update development"
    
    try:
        # 검색 결과
        result = search_tool.invoke(enhanced_query)
        
        # 검색 결과를 구조화
        if isinstance(result, list):
            # 리스트 형태로 반환되는 경우
            search_results = result
        elif isinstance(result, dict) and 'results' in result:
            # 딕셔너리에 results 키가 있는 경우
            search_results = result['results']
        else:
            # 원본 그대로 사용
            search_results = result
        
        print(f"검색 결과: {len(search_results) if isinstance(search_results, list) else 'unknown'} 개")
        
    except Exception as e:
        print(f"검색 오류: {e}")
        search_results = []
    
    # 검색 결과 기반 답변 생성
    prompt = ChatPromptTemplate.from_template(
        """
        당신은 Oil & Gas 산업 정보 조사 전문가입니다.
        웹 검색 결과를 바탕으로 질문에 답변하세요.
        
        특히 다음 정보에 집중하세요:
        - Operator(운영사) 변경 현황
        - Field/Block 개발 진행 상황
        - FID(Final Investment Decision) 관련 소식
        - 생산 시작/중단 소식
        - 계약 체결/변경 소식
        - 최근 1-2년 이내의 정보 우선
        
        --- 웹 검색 결과 ---
        {web_result}
        
        --- 질문 ---
        {question}
        
        답변 형식:
        1. 간단한 요약 (2-3줄)
        2. 주요 소식들을 다음 형식으로 나열:
           - **[제목]**
             링크: [URL]
             (간단한 설명 1줄)
        
        최신 정보부터 나열하고, 관련성 높은 순서로 정리하세요.
        검색 결과가 없거나 관련 정보가 없으면 솔직하게 "관련 최신 정보를 찾을 수 없습니다"라고 답변하세요.
        """
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "web_result": search_results,
        "question": question
    })

    return {"answer": answer}

