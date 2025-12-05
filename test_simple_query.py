# ---------------------------------------------------------
# Simple Query Node 테스트
# ---------------------------------------------------------

from nodes.simple_query_node import simple_query_node
from config import llm
from state import State

# 테스트 질문들
test_questions = [
    "L22/43의 OPERATOR가 누구야?",
    "PTTEP가 운영하는 블록 목록 알려줘",
    "태국에 있는 모든 운영사 리스트",
    "Block A-18의 계약 만료일은?",
    "인도네시아 자산 개수는?",
]

print("=" * 60)
print("Simple Query Node 테스트")
print("=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n[테스트 {i}]")
    print(f"질문: {question}")
    print("-" * 60)
    
    # State 생성
    state = {"question": question}
    
    try:
        # Simple Query Node 실행
        result = simple_query_node(state, llm)
        print(f"답변: {result['answer']}")
    except Exception as e:
        print(f"오류 발생: {e}")
    
    print("-" * 60)

print("\n테스트 완료!")

