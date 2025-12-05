#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Workflow FlowGraph 시각화
"""
import sys
import io

# 윈도우 콘솔 인코딩 문제 해결
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from workflow import app
    from IPython.display import Image, display
    
    print("=" * 80)
    print("Workflow FlowGraph 생성 중...")
    print("=" * 80)
    
    # Mermaid PNG 생성
    graph_png = app.get_graph().draw_mermaid_png()
    
    # 파일로 저장
    with open("workflow_graph.png", "wb") as f:
        f.write(graph_png)
    
    print("\n[OK] FlowGraph가 'workflow_graph.png'로 저장되었습니다!")
    print("\n파일 위치: C:\\Users\\LG\\Desktop\\Asset Analysis\\workflow_graph.png")
    
    # Jupyter/IPython 환경에서 실행 시 이미지 표시
    try:
        display(Image(graph_png))
        print("\n[OK] 이미지가 표시되었습니다!")
    except:
        print("\n[INFO] IPython/Jupyter 환경이 아니므로 이미지를 직접 표시할 수 없습니다.")
        print("       'workflow_graph.png' 파일을 직접 열어서 확인하세요.")
    
    # Mermaid 코드도 텍스트로 출력
    print("\n" + "=" * 80)
    print("Mermaid 다이어그램 코드:")
    print("=" * 80)
    mermaid_code = app.get_graph().draw_mermaid()
    print(mermaid_code)
    
    # Mermaid 코드도 파일로 저장
    with open("workflow_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_code)
    
    print("\n[OK] Mermaid 코드가 'workflow_graph.mmd'로 저장되었습니다!")
    
except ImportError as e:
    print(f"필요한 패키지를 설치해야 합니다:")
    print(f"  pip install pygraphviz")
    print(f"\n또는:")
    print(f"  pip install grandalf")
    print(f"\nError: {e}")

except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()

