# ---------------------------------------------------------
# PDF Reader Node
# ---------------------------------------------------------
# 업로드된 PDF 파일을 읽고 분석하는 Agent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
import PyPDF2
import os


def pdf_reader_node(state, llm):
    """
    업로드된 PDF 파일을 읽고 내용을 분석
    
    Args:
        state: State 객체 (question, pdf_path 필드 포함)
        llm: LLM 인스턴스
        
    Returns:
        dict: {"pdf_result": str, "pdf_content": str} 형태의 결과
    """
    print("PDF Reader Agent 실행 중...")
    
    question = state.get("question", "")
    pdf_path = state.get("pdf_path", None)
    
    # PDF 경로가 없는 경우
    if not pdf_path:
        print("  경고: PDF 파일 경로가 제공되지 않았습니다.")
        return {
            "pdf_result": "PDF 파일이 업로드되지 않았습니다.",
            "pdf_content": ""
        }
    
    # PDF 파일 존재 여부 확인
    if not os.path.exists(pdf_path):
        print(f"  오류: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return {
            "pdf_result": f"PDF 파일을 찾을 수 없습니다: {pdf_path}",
            "pdf_content": ""
        }
    
    try:
        # PDF 파일 읽기
        pdf_content = extract_text_from_pdf(pdf_path)
        
        if not pdf_content.strip():
            print("  경고: PDF에서 텍스트를 추출할 수 없습니다.")
            return {
                "pdf_result": "PDF에서 텍스트를 추출할 수 없습니다. 이미지 기반 PDF일 수 있습니다.",
                "pdf_content": ""
            }
        
        print(f"  PDF 텍스트 추출 완료 (길이: {len(pdf_content)} 자)")
        
        # LLM을 사용하여 PDF 내용 분석
        analysis_result = analyze_pdf_content(pdf_content, question, llm)
        
        print("  PDF 분석 완료")
        
        return {
            "pdf_result": analysis_result,
            "pdf_content": pdf_content
        }
        
    except Exception as e:
        error_msg = f"PDF 처리 중 오류 발생: {str(e)}"
        print(f"  오류: {error_msg}")
        return {
            "pdf_result": error_msg,
            "pdf_content": ""
        }


def extract_text_from_pdf(pdf_path):
    """
    PDF 파일에서 텍스트 추출
    
    Args:
        pdf_path: PDF 파일 경로
        
    Returns:
        str: 추출된 텍스트
    """
    text_content = []
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            print(f"  PDF 페이지 수: {total_pages}")
            
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if text.strip():
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            return "\n".join(text_content)
            
    except Exception as e:
        raise Exception(f"PDF 텍스트 추출 실패: {str(e)}")


def analyze_pdf_content(pdf_content, question, llm):
    """
    추출된 PDF 내용을 LLM을 사용하여 분석
    
    Args:
        pdf_content: PDF에서 추출된 텍스트
        question: 사용자 질문
        llm: LLM 인스턴스
        
    Returns:
        str: 분석 결과
    """
    # PDF 내용이 너무 긴 경우 청킹 전략 사용
    max_content_length = 50000  # 최대 문자 수 증가
    
    truncated = False
    if len(pdf_content) > max_content_length:
        print(f"  PDF 내용이 깁니다. 주요 부분 추출 중... ({len(pdf_content)} -> {max_content_length} 자)")
        # 처음과 중간 부분을 포함하여 더 많은 정보 유지
        first_part = pdf_content[:int(max_content_length * 0.6)]
        middle_part = pdf_content[int(len(pdf_content) * 0.4):int(len(pdf_content) * 0.4) + int(max_content_length * 0.4)]
        pdf_content = first_part + "\n\n... (중간 내용 생략) ...\n\n" + middle_part
        truncated = True
    
    # 분석 프롬프트 (Vantage Asset/Field Report 전문 분석)
    analysis_prompt = f"""
당신은 Oil & Gas 산업의 M&A 및 자산 평가 전문가입니다.
다음 PDF 문서는 Vantage(S&P Global)에서 제공하는 Asset Report 또는 Field Report입니다.

사용자 질문: {question}

PDF 내용:
{pdf_content}

{'(참고: PDF가 길어서 일부 내용이 생략되었습니다. 주요 섹션을 중심으로 분석합니다.)' if truncated else ''}

===================================================================================
PDF 분석 프로토콜 (Vantage Asset/Field Report 표준)
===================================================================================

**1단계: 문서 타입 및 메타데이터 식별**

[필수 추출 항목]
- Document Type: Asset Report or Field Report
- Asset/Field Name: 자산명 또는 필드명
- Country/Region: 국가 및 지역
- Basin: 분지명
- Operator: 운영사
- Working Interest (%): 지분율
- Status: Producing/Developing/Shut-in/Planned
- Year Discovered: 발견 연도
- Production Start: 생산 개시일
- HC Type: Oil/Gas/Oil,gas
- Location Type: Onshore/Offshore/Shelf/Deepwater
- Water Depth: 수심 (해상인 경우)

**2단계: 자원량 데이터 추출**

[Asset Report 중점]
- Remaining Recoverable Oil Resources (MMbbl)
- Remaining Recoverable Gas Resources (Bcf)
- Initial Recoverable Oil Resources (MMbbl)
- Initial Recoverable Gas Resources (Bcf)
- Total Remaining Resources (MMboe)

[Field Report 중점]
- Ultimate Recoverable Reserves (Oil: MMbbl, Gas: MMscf)
- Cumulative Production (Oil: MMbbl, Gas: MMscf)
- Reserves in Place (Original in place)
- Recovery Factor (%)
- 2P Reserves (MMboe)

**3단계: 경제성 지표 추출 (Asset Report 전용)**

[투자 분석]
- Capital Total (inc E&A) (Million USD)
- Decommissioning Total (Million USD)
- F&D Cost per BOE (USD/boe)
- Operating Cost per BOE (USD/boe)
- Total Cost per BOE (USD/boe)

[가치평가]
- NPV @ 10% Discount Rate (Million USD)
- IRR (Internal Rate of Return) (%)
- Payback Period (years)
- Breakeven Oil Price (USD/bbl)
- Breakeven Gas Price (USD/mcf)

[배출량]
- Total CO2 Emissions (tonnes)
- Emissions Intensity (kg CO2/boe)

**4단계: 기술 정보 추출 (Field Report 전용)**

[지질 및 저류층]
- Reservoir Depth (m)
- Lithology: sandstone/limestone/carbonate
- Trap Type: Structural/Stratigraphic
- Seal Type: 실링 메커니즘
- Source Rock: 근원암 정보
- Reservoir Age: Miocene/Oligocene 등

[시추 정보]
- Total Wells: 총 시추공 수
- Discovery Well: 발견정 이름
- Well Tests: 테스트 결과 (bbl/d, mmcf/d)
- Drilling History: 주요 시추 이력

**5단계: 개발 현황 및 이력**

[개발 계획]
- Development Concept: 개발 방식
- Facilities: 시설물 정보
- Infrastructure: 인프라 현황
- Recent Updates: 최근 업데이트 사항

[참여사 이력]
- Participation History: 지분 변동 이력
- Contract Expiry: 계약 만료일
- Farm-in/Farm-out: 지분 거래 이력

**6단계: 종합 분석 및 평가**

아래 형식으로 상세하고 전문적인 분석을 제공하세요:

===================================================================================
[PDF ANALYSIS REPORT]
===================================================================================

**1. DOCUMENT OVERVIEW**
- Document Type: 
- Asset/Field Name:
- Country & Basin:
- Operator & Ownership:
- Status & Discovery Date:

**2. RESOURCE SUMMARY**
- Oil Resources: (MMbbl)
- Gas Resources: (Bcf)
- Total BOE:
- Remaining vs Initial:
- Reserve Category: (2P, 3P 등)

**3. ECONOMIC INDICATORS** (Asset Report인 경우)
- NPV @ 10%: (Million USD)
- IRR: (%)
- Breakeven Oil: (USD/bbl)
- Breakeven Gas: (USD/mcf)
- F&D Cost: (USD/boe)
- OPEX: (USD/boe)
- Total Investment: (Million USD)

**4. TECHNICAL CHARACTERISTICS** (Field Report인 경우)
- Reservoir Depth & Lithology:
- Trap Type & Structure:
- Well Count & Tests:
- Production Performance:
- Recovery Factor:

**5. DEVELOPMENT STATUS**
- Current Phase: (Exploration/Development/Production)
- Key Infrastructure:
- Recent Activities:
- Future Plans:

**6. KEY INSIGHTS & OBSERVATIONS**
(3-5개의 핵심 인사이트)
- [Insight 1]
- [Insight 2]
- [Insight 3]

**7. RISKS & CONSIDERATIONS**
- Technical Risks:
- Commercial Risks:
- Regulatory/Contractual:

**8. M&A PERSPECTIVE**
- Attractiveness: (High/Medium/Low)
- Key Value Drivers:
- Red Flags:
- Valuation Considerations:

**9. EXECUTIVE SUMMARY**
(5-7문장의 종합 의견)

===================================================================================

주의사항:
- 수치는 정확하게 인용하고 단위를 명시하세요
- PDF에 없는 정보는 "N/A" 또는 "문서에 명시되지 않음"으로 표시
- 모든 분석은 PDF 내용에 근거해야 하며, 추측을 피하세요
- 전문 용어를 정확하게 사용하세요

분석을 시작하세요:
"""
    
    try:
        response = llm.invoke([HumanMessage(content=analysis_prompt)])
        return response.content
        
    except Exception as e:
        return f"PDF 분석 중 오류 발생: {str(e)}"


def pdf_reader_node_simple(state):
    """
    PDF 내용만 추출하는 간단한 버전 (LLM 없이)
    
    Args:
        state: State 객체 (pdf_path 필드 포함)
        
    Returns:
        dict: {"pdf_content": str} 형태의 결과
    """
    pdf_path = state.get("pdf_path", None)
    
    if not pdf_path or not os.path.exists(pdf_path):
        return {"pdf_content": ""}
    
    try:
        pdf_content = extract_text_from_pdf(pdf_path)
        return {"pdf_content": pdf_content}
    except:
        return {"pdf_content": ""}

