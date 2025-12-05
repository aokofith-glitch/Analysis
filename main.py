# ---------------------------------------------------------
# 📌 2. 필수 라이브러리 임포트
# ---------------------------------------------------------

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END, START

# LangChain의 메시지, LLM, 파서 등
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

# Web Search
from langchain_tavily import TavilySearch

# Vector DB
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

from langgraph.prebuilt import ToolNode
import pandas as pd
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

print("모든 라이브러리 임포트 완료!")

# ---------------------------------------------------------
# State는 LangGraph에서 노드 간 데이터를 전달하는 구조입니다.
# 아래 구조는 모든 노드가 공통으로 접근할 수 있는 형태입니다.
# ---------------------------------------------------------

class State(TypedDict):
    question: str                          # 사용자 질문
    documents: Optional[List[str]]         # RAG 문서 저장용
    answer: str                            # 최종 생성 답변

print("State 클래스 정의 완료!")

# ---------------------------------------------------------

# 📌 기본 LLM 설정
# ---------------------------------------------------------
# 자주 쓰는 gpt-4.1 모델로 설정
llm = ChatOpenAI(model="gpt-4.1", temperature=0.0)

print("LLM 설정 완료!")

# ---------------------------------------------------------

# 🔍 Web Search Tool
# ---------------------------------------------------------
search_tool = TavilySearch(max_results=5)

print("Web Search Tool 설정 완료!")

# ---------------------------------------------------------
# 📊 CSV 파일 로드 및 SQLite 데이터베이스 설정
# ---------------------------------------------------------
import sqlite3

# 첫 번째 CSV 파일 경로 설정 (실제 파일 경로로 변경 필요)
csv_file_path = "회사상황.csv"

# CSV 파일이 존재하는 경우에만 로드
if os.path.exists(csv_file_path):
    # CSV 파일을 pandas로 로드
    df = pd.read_csv(csv_file_path)
    
    # SQLite 데이터베이스에 저장
    conn = sqlite3.connect("company_data.db")
    df.to_sql("company_info", conn, if_exists="replace", index=False)
    conn.close()
    
    print("첫 번째 CSV 파일 로드 및 SQLite 데이터베이스 설정 완료!")
else:
    print(f"경고: {csv_file_path} 파일을 찾을 수 없습니다.")

# 두 번째 CSV 파일 경로 설정 (실제 파일 경로로 변경 필요)
csv_file_path2 = "회사상황2.csv"

# 두 번째 CSV 파일이 존재하는 경우에만 로드
if os.path.exists(csv_file_path2):
    # CSV 파일을 pandas로 로드
    df2 = pd.read_csv(csv_file_path2)
    
    # SQLite 데이터베이스에 저장 (같은 DB, 다른 테이블)
    conn2 = sqlite3.connect("company_data.db")
    df2.to_sql("company_info2", conn2, if_exists="replace", index=False)
    conn2.close()
    
    print("두 번째 CSV 파일 로드 및 SQLite 데이터베이스 설정 완료!")
else:
    print(f"경고: {csv_file_path2} 파일을 찾을 수 없습니다.")

# ---------------------------------------------------------
# 📌 Router 함수
# ---------------------------------------------------------
def router(state:State):
    return state

print("Router 함수 정의 완료!")

# ---------------------------------------------------------
# Router Node
# ---------------------------------------------------------
# 사용자 질문을 분석하여 다음 중 하나를 결정:
# - web_search
# - vector_rag
# - vector_rag2
# ---------------------------------------------------------
def route_node(state: State):
    input = state["question"]
    route_system_message = """
        당신은 분류기입니다.
        사용자 질문을 다음 중 하나로 분류하세요:
        - web_search
        - vector_rag
        - vector_rag2

        반드시 하나만 출력하세요.
        당신은 '질문 분류 전문가'입니다.
사용자의 질문이 다음 4가지 중 어떤 처리 방식이 필요한지 정확히 분류하세요:

1. "web_search"
   - 최신 정보, 시사/뉴스, 일정, 가격, 주가, 유명인, 제품 정보처럼
     인터넷 검색이 필요한 경우

2. "vector_rag"
   - DB1 과 관련된 질문일 경우

3. "vector_rag2"
   - DB2 와 관련된 질문일 경우

    출력 형식:
    {{
      "route": "web_search" 또는 "vector_rag" 또는 "vector_rag2"
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

print("Route Node 함수 정의 완료!")

# ---------------------------------------------------------
# Tool Node 1
# ---------------------------------------------------------
def tool_node1(state: State):
    """
    사용자 메시지를 분석하여 필요한 툴을 호출하는 노드입니다.
    LLM에 툴을 바인딩하고, 사용자 메시지를 기반으로 툴 호출을 생성합니다.

    Args:
        state: 현재 State 객체 (messages 필드를 포함)

    Returns:
        dict: 업데이트된 State (tool_calls 필드 추가)
    """
    messages = state["messages"][-1].content
    contents_word = state["contents_word"]

    user_query = f"""
    사용할 수 있는 툴만 사용하세요.
    {messages}

    내용 : {contents_word}
    """

    llm_with_tools = llm1.bind_tools(tools)
    response = llm_with_tools.invoke(user_query)

    print(f"툴 호출 메세지 : {response}")
    tool_node = ToolNode(tools)
    result = tool_node.invoke({"messages": [response]})
    print(f"user_query : {user_query}")
    return {"answer_word": result}

print("Tool Node 1 함수 정의 완료!")

# ---------------------------------------------------------
# Web Search Node
# ---------------------------------------------------------
def web_search_node(state: State):
    print("🌐 [웹검색 노드 실행]")

    # 검색 결과
    result = search_tool.invoke(state["question"])

    # 검색 결과 기반 답변 생성
    prompt = ChatPromptTemplate.from_template(
        """
        다음 웹검색 결과를 사용하여 질문에 답하세요.

        --- 검색 결과 ---
        {web_result}

        --- 질문 ---
        {question}
        """
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "web_result": result,
        "question": state["question"]
    })

    return {"answer": answer}

print("Web Search Node 함수 정의 완료!")

# ---------------------------------------------------------
# RAG Node
# ---------------------------------------------------------
def rag_node(state: State):
    print("📚 [RAG 노드 실행]")

    docs = retriever.invoke(state["question"])
    docs_text = "\n\n".join([d.page_content for d in docs])

    prompt = ChatPromptTemplate.from_template(
        """
        다음 문서만 사용하여 질문에 답하세요.

        --- 문서 ---
        {context}

        --- 질문 ---
        {question}
        """
    )

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": docs_text,
        "question": state["question"]
    })

    return {
        "answer": answer,
        "documents": [d.page_content for d in docs]
    }

print("RAG Node 함수 정의 완료!")

# ---------------------------------------------------------
# RAG Node 2
# ---------------------------------------------------------
def rag_node2(state: State):
    print("📚 [RAG 노드 실행]")

    docs = retriever2.invoke(state["question"])
    docs_text = "\n\n".join([d.page_content for d in docs])

    prompt = ChatPromptTemplate.from_template(
        """
        다음 문서만 사용하여 질문에 답하세요.

        --- 문서 ---
        {context}

        --- 질문 ---
        {question}
        """
    )

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": docs_text,
        "question": state["question"]
    })

    return {
        "answer": answer,
        "documents": [d.page_content for d in docs]
    }

print("RAG Node 2 함수 정의 완료!")

# ---------------------------------------------------------
# Manager: Integrator1 (결과 취합)
# ---------------------------------------------------------
def integrator1(state: State):
    """
    Workers의 결과를 취합하는 Manager
    """
    subject = state["subject"]
    websearch = state["websearch"]
    dbsearch = state["dbsearch"]

    print(f"=== 워드 Manager (Integrator) 실행 ===")

    # 통합 프롬프트
    prompt = f"""
                주제:
                {subject}

                웹서치 결과:
                {websearch}

                db서치 결과:
                {dbsearch}


                위 내용들을 통합하여
                아래 양식 기반의 보고서 만들어줘

                1.개요(Introduction)
                2.현재 상황 분석(Current Status)
                3.분석 결과(Findings)
                4.대안 검토(Options Review)
                5.추천 방안(Recommendation)
                6.기대 효과(Expected Impact)
                7.결론(Conclusion)
                """

    response = llm1.invoke([HumanMessage(content=prompt)])
    final_design = response.content

    print(f"결과:\n{final_design}")

    return {"contents_word": final_design}

print("Integrator1 함수 정의 완료!")

# ---------------------------------------------------------
# Workflow 설정
# ---------------------------------------------------------
workflow = StateGraph(State)

workflow.add_node("router", router)
workflow.add_node("web_search", web_search_node)
workflow.add_node("vector_rag", rag_node)
workflow.add_node("vector_rag2", rag_node2)
workflow.add_node("integrator1", integrator1)
workflow.add_node("word_file", tool_node1)


workflow.add_conditional_edges(
    "router",
    route_node,
    {
        "vector_rag": "vector_rag",
        "vector_rag2": "vector_rag2",
        "web_search": "web_search",
    }
)

workflow.add_edge(START, "router")
workflow.add_edge("web_search", "integrator1")
workflow.add_edge("vector_rag", "integrator1")
workflow.add_edge("vector_rag2", "integrator1")
workflow.add_edge("integrator1","word_file")
workflow.add_edge("word_file", END)


app = workflow.compile()

print("Workflow 설정 완료!")

