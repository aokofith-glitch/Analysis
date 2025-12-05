#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

# Windows 콘솔 한글 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Testing query...")

try:
    from workflow import app as workflow_app
    print("[OK] Workflow imported")
    
    # 테스트 질문
    test_question = "Hac Long (Black Dragon), VN 분석해줘"
    print(f"\n[TEST] Question: {test_question}")
    
    result = workflow_app.invoke({"question": test_question})
    print(f"\n[SUCCESS] Result:")
    print("="*80)
    print(f"라우팅: {result.get('route', 'N/A')}")
    print(f"\n최종 답변:\n{result.get('answer', 'N/A')}")
    print("="*80)
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

