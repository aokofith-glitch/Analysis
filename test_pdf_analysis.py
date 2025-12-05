"""
PDF 분석 테스트 스크립트

Vantage Asset/Field Report PDF를 분석하는 전체 워크플로우를 테스트합니다.

사용 방법:
    python test_pdf_analysis.py
"""

from workflow import app
import os

def test_pdf_analysis():
    """PDF 분석 테스트"""
    
    # PDF 파일 경로 설정
    pdf_file = "pdf files/Vantage_Cepu PSC_AssetReport_2025-12-04.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_file}")
        print("\n사용 가능한 PDF 파일:")
        pdf_dir = "pdf files"
        if os.path.exists(pdf_dir):
            for f in os.listdir(pdf_dir):
                if f.endswith('.pdf'):
                    print(f"  - {f}")
        return
    
    # 초기 state 설정
    initial_state = {
        "question": "이 자산에 대해 상세히 분석해주세요",
        "pdf_path": pdf_file,
        "answer": "",
        "documents": [],
        "route": None,
        "economic_result": None,
        "production_result": None,
        "pdf_result": None,
        "pdf_content": None,
        "websearch_result": None,
        "rag1_result": None,
        "rag2_result": None,
    }
    
    print("="*100)
    print("PDF 분석 워크플로우 시작")
    print("="*100)
    print(f"PDF 파일: {pdf_file}")
    print(f"질문: {initial_state['question']}")
    print("="*100)
    print()
    
    # 워크플로우 실행
    try:
        result = app.invoke(initial_state)
        
        print("\n" + "="*100)
        print("분석 완료!")
        print("="*100)
        
        # 최종 결과 출력
        if "answer" in result:
            print("\n[최종 분석 결과]\n")
            print(result["answer"])
        else:
            print("결과를 찾을 수 없습니다.")
            print(f"\nState 키: {list(result.keys())}")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


def test_pdf_with_database():
    """PDF + Database 통합 분석 테스트"""
    
    # PDF 파일 경로 설정
    pdf_file = "pdf files/Vantage_Cepu PSC_AssetReport_2025-12-04.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"오류: PDF 파일을 찾을 수 없습니다: {pdf_file}")
        return
    
    # 초기 state 설정 (both 모드 - Economic + Production + PDF)
    initial_state = {
        "question": "Cepu PSC 자산을 종합적으로 분석하고 투자 의견을 제시해주세요",
        "pdf_path": pdf_file,
        "answer": "",
        "documents": [],
        "route": None,
        "economic_result": None,
        "production_result": None,
        "pdf_result": None,
        "pdf_content": None,
        "websearch_result": None,
        "rag1_result": None,
        "rag2_result": None,
    }
    
    print("="*100)
    print("통합 분석 워크플로우 시작 (Economic + Production + PDF)")
    print("="*100)
    print(f"PDF 파일: {pdf_file}")
    print(f"질문: {initial_state['question']}")
    print("="*100)
    print()
    
    # 워크플로우 실행
    try:
        result = app.invoke(initial_state)
        
        print("\n" + "="*100)
        print("통합 분석 완료!")
        print("="*100)
        
        # 최종 결과 출력
        if "answer" in result:
            print("\n[최종 종합 분석 결과]\n")
            print(result["answer"])
        else:
            print("결과를 찾을 수 없습니다.")
            print(f"\nState 키: {list(result.keys())}")
        
        # 중간 결과도 확인
        print("\n" + "="*100)
        print("중간 결과 확인")
        print("="*100)
        print(f"Route: {result.get('route', 'N/A')}")
        print(f"Economic 결과 길이: {len(result.get('economic_result', '')) if result.get('economic_result') else 0}")
        print(f"Production 결과 길이: {len(result.get('production_result', '')) if result.get('production_result') else 0}")
        print(f"PDF 결과 길이: {len(result.get('pdf_result', '')) if result.get('pdf_result') else 0}")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "="*100)
    print("테스트 옵션을 선택하세요:")
    print("="*100)
    print("1. PDF만 분석 (PDF Reader 단독)")
    print("2. PDF + Database 통합 분석 (Economic + Production + PDF)")
    print("="*100)
    
    choice = input("\n선택 (1 or 2): ").strip()
    
    if choice == "1":
        test_pdf_analysis()
    elif choice == "2":
        test_pdf_with_database()
    else:
        print("잘못된 선택입니다. 1 또는 2를 입력하세요.")

