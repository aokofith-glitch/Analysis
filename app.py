from flask import Flask, render_template, request, jsonify
import os
import sys

# workflow import
from workflow import app as workflow_app

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/process', methods=['POST'])
def process_question():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                "success": False,
                "error": "질문을 입력해주세요."
            }), 400
        
        print(f"[USER QUESTION] {question}")
        
        # Workflow 실행
        result = workflow_app.invoke({"question": question})
        
        print(f"[SUCCESS] Workflow completed")
        print(f"[RESULT] {result}")
        
        # 응답 생성
        response = {
            "success": True,
            "answer": result.get("answer", "답변을 생성할 수 없습니다."),
            "route": result.get("route", "Unknown"),
            "documents": result.get("documents", [])
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("[STARTING] Flask server starting...")
    print("[INFO] Server available at http://localhost:5000")
    flask_app.run(host='0.0.0.0', port=5000, debug=True)

