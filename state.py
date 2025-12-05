# ---------------------------------------------------------
# State Definition
# ---------------------------------------------------------
# State는 LangGraph에서 노드 간 데이터를 전달하는 구조입니다.
# 아래 구조는 모든 노드가 공통으로 접근할 수 있는 형태입니다.
# ---------------------------------------------------------

from typing import TypedDict, List, Optional, Any, Dict
from langchain_core.messages import BaseMessage


class State(TypedDict):
    question: str                          # 사용자 질문
    documents: Optional[List[str]]         # RAG 문서 저장용
    answer: str                            # 최종 생성 답변
    
    # Routing 정보
    route: Optional[str]                   # 라우팅 경로
    
    # RAG 결과
    economic_result: Optional[str]         # Economic Agent 결과
    production_result: Optional[str]       # Production Agent 결과
    websearch_result: Optional[str]        # Web Search 결과
    rag1_result: Optional[Dict[str, Any]]  # Economic Agent 상세 결과
    rag2_result: Optional[Dict[str, Any]]  # Production Agent 상세 결과
    
    # PDF Reader 결과
    pdf_path: Optional[str]                # PDF 파일 경로
    pdf_result: Optional[str]              # PDF 분석 결과
    pdf_content: Optional[str]             # PDF 추출 텍스트
    
    # Integrator용 필드들
    subject: Optional[str]                 # 주제
    websearch: Optional[str]               # 웹 검색 결과
    dbsearch: Optional[str]                # DB 검색 결과
    
    # Tool Node용 필드들
    messages: Optional[List[BaseMessage]]  # 메시지 리스트
    contents_word: Optional[str]           # 워드 문서 내용
    answer_word: Optional[str]             # 워드 생성 결과
    word_file_path: Optional[str]          # 생성된 Word 파일 경로

