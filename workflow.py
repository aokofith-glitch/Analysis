# ---------------------------------------------------------
# Workflow Definition
# ---------------------------------------------------------

from langgraph.graph import StateGraph, END, START
from state import State
from config import (llm, llm1, llm2, llm3, llm4, search_tool, 
                   DB_PATH, DB1_TABLE, DB2_TABLE,
                   ECONOMIC_DB_PATH, ECONOMIC_TABLE,
                   PRODUCTION_DB_PATH, PRODUCTION_TABLE)
from nodes.router_node import router, route_node
from nodes.web_search_node import web_search_node
from nodes.rag_node import rag_node
from nodes.rag_node2 import rag_node2
from nodes.integrator_node import integrator1
from nodes.tool_node import tool_node1
from nodes.simple_query_node import simple_query_node
from nodes.pdf_reader_node import pdf_reader_node


# 노드 래퍼 함수들 (config 주입)
def router_wrapper(state):
    return router(state)


def route_node_wrapper(state):
    return route_node(state, llm)


def simple_query_wrapper(state):
    return simple_query_node(state, llm, ECONOMIC_DB_PATH, PRODUCTION_DB_PATH)


def web_search_wrapper(state):
    return web_search_node(state, search_tool, llm3)


def rag_node_wrapper(state):
    return rag_node(state, llm1, ECONOMIC_DB_PATH, ECONOMIC_TABLE)


def rag_node2_wrapper(state):
    return rag_node2(state, llm2, PRODUCTION_DB_PATH, PRODUCTION_TABLE)


def pdf_reader_wrapper(state):
    """PDF 파일을 읽고 분석하는 래퍼"""
    return pdf_reader_node(state, llm3)


def both_rag_wrapper(state):
    """Economic과 Production 데이터를 모두 조회하는 래퍼"""
    # Economic 데이터 조회
    rag1_result = rag_node(state, llm1, ECONOMIC_DB_PATH, ECONOMIC_TABLE)
    
    # Production 데이터 조회
    rag2_result = rag_node2(state, llm2, PRODUCTION_DB_PATH, PRODUCTION_TABLE)
    
    # 결과를 state에 저장 (Integrator가 인식할 수 있도록)
    return {
        "economic_result": rag1_result.get("answer", ""),
        "production_result": rag2_result.get("answer", ""),
        "rag1_result": rag1_result,
        "rag2_result": rag2_result,
        "documents": (rag1_result.get("documents", []) + rag2_result.get("documents", [])),
    }


def both_with_pdf_wrapper(state):
    """Economic + Production + PDF를 모두 조회하는 래퍼"""
    # Economic 데이터 조회
    rag1_result = rag_node(state, llm1, ECONOMIC_DB_PATH, ECONOMIC_TABLE)
    
    # Production 데이터 조회
    rag2_result = rag_node2(state, llm2, PRODUCTION_DB_PATH, PRODUCTION_TABLE)
    
    # PDF 분석
    pdf_result = pdf_reader_node(state, llm3)
    
    # 결과를 state에 저장 (Integrator가 인식할 수 있도록)
    return {
        "economic_result": rag1_result.get("answer", ""),
        "production_result": rag2_result.get("answer", ""),
        "pdf_result": pdf_result.get("pdf_result", ""),
        "rag1_result": rag1_result,
        "rag2_result": rag2_result,
        "pdf_content": pdf_result.get("pdf_content", ""),
        "documents": (rag1_result.get("documents", []) + rag2_result.get("documents", [])),
    }


def integrator1_wrapper(state):
    return integrator1(state, llm4)


def tool_node1_wrapper(state):
    # tools는 추후 정의 필요
    tools = []
    return tool_node1(state, llm1, tools)


# Workflow 구성
workflow = StateGraph(State)

# 노드 추가
workflow.add_node("router", router_wrapper)
workflow.add_node("simple_query", simple_query_wrapper)
workflow.add_node("web_search", web_search_wrapper)
workflow.add_node("vector_rag", rag_node_wrapper)
workflow.add_node("vector_rag2", rag_node2_wrapper)
workflow.add_node("pdf_reader", pdf_reader_wrapper)  # PDF Reader 노드 추가
workflow.add_node("both_rag", both_rag_wrapper)  # Economic + Production 동시 조회
workflow.add_node("both_with_pdf", both_with_pdf_wrapper)  # Economic + Production + PDF 동시 조회
workflow.add_node("integrator1", integrator1_wrapper)
workflow.add_node("word_file", tool_node1_wrapper)

# 조건부 엣지 추가 - route_decision 함수 정의
def route_decision(state):
    """라우팅 결정을 반환하는 함수"""
    route = route_node_wrapper(state)
    state["route"] = route  # state에 route 저장
    
    # PDF가 업로드된 경우, both와 함께 실행되도록 수정
    pdf_path = state.get("pdf_path", None)
    if pdf_path and route == "both":
        return "both_with_pdf"
    
    return route

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "simple_query": "simple_query",
        "vector_rag": "vector_rag",
        "vector_rag2": "vector_rag2",
        "web_search": "web_search",
        "pdf_reader": "pdf_reader",  # PDF Reader 경로 추가
        "both": "both_rag",  # Economic + Production 동시 조회
        "both_with_pdf": "both_with_pdf",  # Economic + Production + PDF 동시 조회
    }
)

# 엣지 추가
workflow.add_edge(START, "router")
workflow.add_edge("simple_query", END)  # simple_query는 바로 종료
workflow.add_edge("web_search", "integrator1")
workflow.add_edge("vector_rag", "integrator1")
workflow.add_edge("vector_rag2", "integrator1")
workflow.add_edge("pdf_reader", "integrator1")  # PDF Reader도 integrator로
workflow.add_edge("both_rag", "integrator1")  # both_rag도 integrator로
workflow.add_edge("both_with_pdf", "integrator1")  # both_with_pdf도 integrator로
workflow.add_edge("integrator1", "word_file")  # integrator에서 word_file로
workflow.add_edge("word_file", END)  # word_file에서 종료

# Workflow 컴파일
app = workflow.compile()

print("Workflow 컴파일 완료!")

