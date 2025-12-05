# 그래프 구조 시각화 스크립트

# 현재 workflow의 구조를 텍스트로 출력

print("=" * 60)
print("Workflow 그래프 구조")
print("=" * 60)

print("\n[노드 목록]")
nodes = ["router", "simple_query", "web_search", "vector_rag", "vector_rag2", "integrator1", "word_file"]
for i, node in enumerate(nodes, 1):
    print(f"  {i}. {node}")

print("\n[엣지 연결 구조]")
print("\n1. 시작점:")
print("   START → router")

print("\n2. router에서 조건부 분기:")
print("   router → simple_query  (단순 정보 조회)")
print("   router → vector_rag    (Economic 분석)")
print("   router → vector_rag2   (Production 분석)")
print("   router → web_search    (웹 검색)")
print("   router → both          (종합 분석)")

print("\n3. simple_query는 바로 종료:")
print("   simple_query → END (integrator 거치지 않음)")

print("\n4. 분석 경로는 integrator1로 수렴:")
print("   web_search → integrator1")
print("   vector_rag → integrator1")
print("   vector_rag2 → integrator1")

print("\n5. 최종 처리:")
print("   integrator1 → word_file")
print("   word_file → END")

print("\n" + "=" * 60)
print("전체 흐름:")
print("=" * 60)
print("""
START 
  ↓
router (질문 분류)
  ↓
  ├─→ simple_query (단순 조회) ──────→ END
  ├─→ web_search (웹 검색) ──────┐
  ├─→ vector_rag (Economic) ─────┼─→ integrator1 (결과 통합)
  ├─→ vector_rag2 (Production) ──┘        ↓
  └─→ both (종합 분석) ───────────────→ word_file (파일 생성)
                                           ↓
                                          END
""")
print("=" * 60)

