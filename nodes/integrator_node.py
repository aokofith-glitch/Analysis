# ---------------------------------------------------------
# Manager: Integrator1 (결과 취합)
# ---------------------------------------------------------

from langchain_core.messages import HumanMessage


def integrator1(state, llm):
    """
    각 Agent의 결과를 취합하는 Manager
    - Economic Agent 결과 그대로 표시
    - Production Agent 결과 그대로 표시
    - PDF Reader Agent 결과 그대로 표시
    - Web Search 결과 그대로 표시
    - 위 모든 결과를 종합한 전문가 수준의 최종 평가 추가
    
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
    pdf_result = state.get("pdf_result", "")  # PDF Reader 결과 추가
    websearch_result = state.get("websearch_result", "")
    
    # 디버깅 출력
    print(f"  economic_result 길이: {len(economic_result) if economic_result else 0}")
    print(f"  production_result 길이: {len(production_result) if production_result else 0}")
    print(f"  pdf_result 길이: {len(pdf_result) if pdf_result else 0}")
    print(f"  websearch_result 길이: {len(websearch_result) if websearch_result else 0}")
    
    # answer 필드가 있으면 그것을 사용 (단일 Agent 실행 시)
    if answer and not economic_result and not production_result and not pdf_result and not websearch_result:
        # route 정보를 활용하여 판단
        route = state.get("route", "")
        
        if route == "vector_rag":
            economic_result = answer
        elif route == "vector_rag2":
            production_result = answer
        elif route == "pdf_reader":
            pdf_result = answer
        elif route == "web_search":
            websearch_result = answer
        else:
            # route 정보가 없으면 내용으로 판단
            if "ECONOMIC ANALYSIS" in answer or "Breakeven" in answer or "IRR" in answer:
                economic_result = answer
            elif "PRODUCTION ANALYSIS" in answer or "생산량" in answer or "매장량" in answer:
                production_result = answer
            elif "PDF ANALYSIS REPORT" in answer or "DOCUMENT OVERVIEW" in answer:
                pdf_result = answer
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
    
    # 3. PDF 분석 (새로 추가)
    if pdf_result:
        report_sections.append("=" * 80)
        report_sections.append("[PDF DOCUMENT ANALYSIS]")
        report_sections.append("=" * 80)
        report_sections.append(pdf_result)
        report_sections.append("")
    
    # 4. 최신 동향
    if websearch_result:
        report_sections.append("=" * 80)
        report_sections.append("[LATEST TRENDS & NEWS]")
        report_sections.append("=" * 80)
        report_sections.append(websearch_result)
        report_sections.append("")
    
    # 결과가 하나라도 있으면 최종 평가 생성
    if report_sections:
        combined_info = "\n".join(report_sections)
        
        # 향상된 최종 평가 프롬프트 (전문가 수준)
        final_prompt = f"""
당신은 Oil & Gas 산업의 시니어 M&A 어드바이저이자 자산 평가 전문가입니다.
20년 이상의 경험을 바탕으로 아래 분석 결과들을 종합하여 상세하고 전문적인 최종 의견을 제시하세요.

===================================================================================
분석 데이터
===================================================================================

{combined_info}

===================================================================================
최종 전문가 의견 작성 가이드
===================================================================================

**반드시 아래 구조를 따라 상세하게 작성하세요:**

**1. EXECUTIVE SUMMARY (경영진 요약)**
   - 3-4문장으로 핵심 결론 제시
   - 투자 권고 수준 명시 (Strong Buy/Buy/Hold/Sell)
   - 목표 가치 범위 또는 Fair Value 제시 (가능한 경우)

**2. INTEGRATED ASSET VALUATION (통합 자산 가치평가)**
   
   [2.1 Economic Fundamentals]
   - Economic 데이터 기반 가치 평가
   - NPV, IRR, Breakeven Price 해석
   - Cost Structure 분석 (CAPEX, OPEX, Total Cost/BOE)
   - Fiscal Terms의 매력도
   - 경제성 경쟁력 (동일 지역/유사 자산 대비)
   
   [2.2 Production & Reserve Quality]
   - Production 데이터 기반 자산 품질 평가
   - Remaining Reserves와 Reserve Life 분석
   - Recovery Factor 및 생산 효율성
   - Production Decline Rate 및 Plateau 기간
   - 2P/3P Reserves의 신뢰도
   
   [2.3 Technical & Operational Assessment] (PDF 데이터 활용)
   - 지질학적 리스크 평가 (Reservoir 특성, Trap Type 등)
   - Infrastructure 및 Facility 현황
   - Operatorship Quality 및 Track Record
   - Development 계획의 실현 가능성
   - Technical Risk Factors

**3. CROSS-VALIDATION & CONSISTENCY CHECK**
   - Economic vs Production 데이터 일관성 검증
   - PDF Report vs Database 수치 비교
   - 불일치 사항 및 해석
   - 데이터 신뢰도 평가 (High/Medium/Low)

**4. STRATEGIC VALUE DRIVERS**
   - Portfolio Fit: 어떤 투자자에게 적합한가?
   - Geographic Advantage: 지정학적 이점
   - Infrastructure Synergy: 인근 자산과의 시너지
   - Growth Optionality: 추가 탐사 잠재력
   - ESG Considerations: 환경 규제 및 배출량 이슈

**5. RISK MATRIX (상세 리스크 분석)**
   
   [5.1 High Risk Items] (치명적 리스크)
   - [구체적으로 나열]
   
   [5.2 Medium Risk Items] (관리 가능한 리스크)
   - [구체적으로 나열]
   
   [5.3 Low Risk Items] (경미한 리스크)
   - [구체적으로 나열]
   
   [5.4 Risk Mitigation Strategies]
   - 각 리스크에 대한 완화 방안

**6. VALUATION SCENARIOS**
   
   [6.1 Base Case]
   - 현재 데이터 기반 가치 평가
   - 주요 가정 및 전제조건
   
   [6.2 Bull Case] (낙관적 시나리오)
   - 상승 요인 (유가 상승, 생산 증대, 비용 절감 등)
   - Upside Potential
   
   [6.3 Bear Case] (비관적 시나리오)
   - 하락 요인 (유가 하락, 생산 차질, 비용 증가 등)
   - Downside Risk

**7. COMPARABLE ANALYSIS**
   - 유사 자산 대비 상대적 매력도
   - Peer Group 내 위치 (Top Quartile/Median/Bottom Quartile)
   - Valuation Multiples 비교 (가능한 경우)

**8. DEAL STRUCTURE CONSIDERATIONS**
   - 적정 지분율 (Minority/Majority/100%)
   - Earnout/Contingent Payment 고려 사항
   - Working Interest vs Royalty Interest
   - JV Structure 제안

**9. TIMELINE & CATALYSTS**
   - 단기 가치 창출 요인 (0-12개월)
   - 중기 개발 마일스톤 (1-3년)
   - 장기 자산 가치 변화 (3-5년+)

**10. FINAL RECOMMENDATION**
   - 명확한 투자 의견 (Strong Buy/Buy/Hold/Sell/Strong Sell)
   - Target Valuation Range (Million USD)
   - Key Action Items (Due Diligence 체크리스트)
   - Decision Timeline 제안

===================================================================================

**작성 원칙:**
- 구체적인 수치와 데이터를 인용하여 논리적으로 설명
- 모호한 표현 지양, 명확한 판단 제시
- 장점과 단점을 균형있게 평가
- 실행 가능한 권고사항 제시
- 최소 15-20문장 이상의 상세한 분석

최종 전문가 의견을 작성하세요:
"""
        
        response = llm.invoke([HumanMessage(content=final_prompt)])
        final_evaluation = response.content
        
        # 최종 평가 추가
        report_sections.append("=" * 80)
        report_sections.append("[FINAL EXPERT OPINION - COMPREHENSIVE ASSESSMENT]")
        report_sections.append("=" * 80)
        report_sections.append(final_evaluation)
        report_sections.append("")
        
        final_report = "\n".join(report_sections)
        
    else:
        # 결과가 없는 경우
        final_report = "분석 결과가 없습니다."
    
    print(f"통합 보고서 생성 완료 (PDF 분석 포함)")

    return {"answer": final_report}

