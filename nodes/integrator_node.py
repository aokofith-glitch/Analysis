# ---------------------------------------------------------
# Manager: Integrator1 (결과 취합)
# ---------------------------------------------------------

from langchain_core.messages import HumanMessage


def integrator1(state, llm):
    """
    각 Agent의 결과를 취합하는 Manager
    - Economic Agent 결과 그대로 표시
    - Production Agent 결과 그대로 표시
    - Web Search 결과 그대로 표시
    - 위 3개를 종합한 최종 평가 추가
    
    Args:
        state: State 객체 (answer 필드 포함)
        llm: LLM 인스턴스 (llm4)
        
    Returns:
        dict: {"answer": str} 형태의 통합 결과
    """
    question = state.get("question", "")
    answer = state.get("answer", "")
    documents = state.get("documents", [])

    print(f"=== Integrator 실행 중 ===")
    
    # 각 Agent의 결과 확인
    economic_result = state.get("economic_result", "")
    production_result = state.get("production_result", "")
    websearch_result = state.get("websearch_result", "")
    
    # 디버깅 출력
    print(f"  economic_result 길이: {len(economic_result) if economic_result else 0}")
    print(f"  production_result 길이: {len(production_result) if production_result else 0}")
    print(f"  websearch_result 길이: {len(websearch_result) if websearch_result else 0}")
    
    # answer 필드가 있으면 그것을 사용 (단일 Agent 실행 시)
    if answer and not economic_result and not production_result and not websearch_result:
        # route 정보를 활용하여 판단
        route = state.get("route", "")
        
        if route == "vector_rag":
            economic_result = answer
        elif route == "vector_rag2":
            production_result = answer
        elif route == "web_search":
            websearch_result = answer
        else:
            # route 정보가 없으면 내용으로 판단
            if "Economic" in str(documents) or "Breakeven" in answer or "IRR" in answer:
                economic_result = answer
            elif "Production" in str(documents) or "생산량" in answer or "매장량" in answer:
                production_result = answer
            else:
                # 기본값은 웹 검색으로 간주
                websearch_result = answer

    # 결과 조합
    report_sections = []
    
    # 1. Economic 평가
    if economic_result:
        report_sections.append("=" * 80)
        report_sections.append("[ECONOMIC ANALYSIS]")
        report_sections.append("=" * 80)
        report_sections.append(economic_result)
        report_sections.append("")
    
    # 2. Production 평가
    if production_result:
        report_sections.append("=" * 80)
        report_sections.append("[PRODUCTION ANALYSIS]")
        report_sections.append("=" * 80)
        report_sections.append(production_result)
        report_sections.append("")
    
    # 3. 최신 동향
    if websearch_result:
        report_sections.append("=" * 80)
        report_sections.append("[LATEST TRENDS]")
        report_sections.append("=" * 80)
        report_sections.append(websearch_result)
        report_sections.append("")
    
    # 결과가 하나라도 있으면 최종 평가 생성
    if report_sections:
        combined_info = "\n".join(report_sections)
        
        # 최종 평가 프롬프트
        final_prompt = f"""
        다음은 자산 분석 결과입니다:
        
        {combined_info}
        
        위 정보들을 종합하여 간결한 최종 평가를 작성해주세요.
        
        최종 평가 작성 가이드:
        - Economic, Production, 최신 동향 정보를 모두 고려
        - 핵심 인사이트 3-5가지
        - 투자 매력도 또는 주의사항
        - 향후 전망
        
        최종 평가는 5-7문장 이내로 간결하게 작성하세요.
        """
        
        response = llm.invoke([HumanMessage(content=final_prompt)])
        final_evaluation = response.content
        
        # 최종 평가 추가
        report_sections.append("=" * 80)
        report_sections.append("[FINAL EVALUATION]")
        report_sections.append("=" * 80)
        report_sections.append(final_evaluation)
        report_sections.append("")
        
        final_report = "\n".join(report_sections)
        
    else:
        # 결과가 없는 경우
        final_report = "분석 결과가 없습니다."
    
    print(f"통합 보고서 생성 완료")

    return {"answer": final_report}

