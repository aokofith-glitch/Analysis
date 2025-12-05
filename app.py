from flask import Flask, render_template, request, jsonify
import os
import sys
from werkzeug.utils import secure_filename

# workflow import
from workflow import app as workflow_app

flask_app = Flask(__name__)

# PDF 업로드 설정
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 업로드 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """업로드 가능한 파일인지 확인"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/process', methods=['POST'])
def process_question():
    try:
        # multipart/form-data로 받기 (PDF 업로드 지원)
        question = request.form.get('question', '')
        pdf_file = request.files.get('pdf_file', None)
        pdf_path = None
        
        if not question:
            return jsonify({
                "success": False,
                "error": "질문을 입력해주세요."
            }), 400
        
        print(f"[USER QUESTION] {question}")
        
        # PDF 파일 처리
        if pdf_file and pdf_file.filename:
            if allowed_file(pdf_file.filename):
                filename = secure_filename(pdf_file.filename)
                pdf_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
                pdf_file.save(pdf_path)
                print(f"[PDF UPLOADED] {pdf_path}")
            else:
                return jsonify({
                    "success": False,
                    "error": "PDF 파일만 업로드 가능합니다."
                }), 400
        
        # Workflow 실행 (PDF 경로 포함)
        workflow_input = {
            "question": question,
            "pdf_path": pdf_path,
            "answer": "",
            "documents": [],
            "route": None,
        }
        
        result = workflow_app.invoke(workflow_input)
        
        print(f"[SUCCESS] Workflow completed")
        print(f"[ROUTE] {result.get('route', 'Unknown')}")
        
        # 업로드된 파일 정리 (선택사항 - 보안상 권장)
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                print(f"[CLEANUP] Removed {pdf_path}")
            except Exception as e:
                print(f"[WARNING] Could not remove file: {e}")
        
        # 응답 생성
        response = {
            "success": True,
            "answer": result.get("answer", "답변을 생성할 수 없습니다."),
            "route": result.get("route", "Unknown"),
            "documents": result.get("documents", []),
            "pdf_analyzed": pdf_path is not None,
            "word_file_path": result.get("word_file_path", None)  # Word 파일 경로 추가
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

