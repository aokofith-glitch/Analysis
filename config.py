# ---------------------------------------------------------
# Configuration File
# ---------------------------------------------------------

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# .env 파일에서 환경 변수 로드
load_dotenv()

# LLM 설정 (각 노드별로 다른 LLM 사용)
llm = ChatOpenAI(model="gpt-4.1", temperature=0.0)      # router용
llm1 = ChatOpenAI(model="gpt-4.1", temperature=0.0)     # rag_node용
llm2 = ChatOpenAI(model="gpt-4.1", temperature=0.0)     # rag_node2용
llm3 = ChatOpenAI(model="gpt-4.1", temperature=0.0)     # web_search용
llm4 = ChatOpenAI(model="gpt-4.1", temperature=0.0)     # integrator용

# Web Search Tool 설정
search_tool = TavilySearch(max_results=5)

# 데이터베이스 설정
DB_PATH = "company_data.db"
DB1_TABLE = "company_info"
DB2_TABLE = "company_info2"

# Economic 데이터베이스 (rag_node용)
ECONOMIC_DB_PATH = "economic_data.db"
ECONOMIC_TABLE = "economic_data"

# Production 데이터베이스 (rag_node2용)
PRODUCTION_DB_PATH = "production_data.db"
PRODUCTION_TABLE = "production_data"

# CSV 파일 경로
CSV_FILE_PATH = "회사상황.csv"
CSV_FILE_PATH2 = "회사상황2.csv"

print("Configuration 로드 완료!")

