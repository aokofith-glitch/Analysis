# ---------------------------------------------------------
# Production DB 설정 스크립트
# ---------------------------------------------------------
# document 폴더에서 Production이 포함된 CSV 파일들을 SQLite DB로 변환

import os
import pandas as pd
import sqlite3
import glob

# 경로 설정
DOCUMENT_PATH = "document"
DB_PATH = "production_data.db"

def setup_production_database():
    """
    document 폴더에서 Production이 포함된 모든 CSV 파일을 찾아서
    SQLite 데이터베이스에 저장
    """
    # Production이 포함된 CSV 파일 찾기
    pattern = os.path.join(DOCUMENT_PATH, "*Production*.csv")
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print(f"경고: {DOCUMENT_PATH} 폴더에서 Production CSV 파일을 찾을 수 없습니다.")
        return
    
    print(f"찾은 Production CSV 파일: {len(csv_files)}개")
    
    # SQLite 연결
    conn = sqlite3.connect(DB_PATH)
    
    # 각 CSV 파일을 하나의 통합 테이블로 저장
    all_data = []
    
    for csv_file in csv_files:
        try:
            filename = os.path.basename(csv_file)
            print(f"처리 중: {filename}")
            
            # CSV 읽기
            df = pd.read_csv(csv_file)
            
            # 파일명에서 연도 범위 추출
            # 예: Rystad_Indonesia_Production (1960-1984).csv
            year_range = ""
            if '(' in filename and ')' in filename:
                year_range = filename.split('(')[1].split(')')[0]
            
            # 메타데이터 컬럼 추가 (Country는 이미 존재하므로 제외)
            df['source_file'] = filename
            df['year_range'] = year_range
            
            all_data.append(df)
            
            print(f"  [OK] {filename}: {len(df)} 행 로드됨")
            
        except Exception as e:
            print(f"  [ERROR] {filename} 처리 실패: {e}")
    
    # 모든 데이터 통합
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # SQLite에 저장
        combined_df.to_sql('production_data', conn, if_exists='replace', index=False)
        
        print(f"\n총 {len(combined_df)} 행이 'production_data' 테이블에 저장되었습니다.")
        print(f"데이터베이스: {DB_PATH}")
        
        # 테이블 정보 출력
        print("\n테이블 컬럼:")
        print(combined_df.columns.tolist())
        
        # 국가별 데이터 수 출력
        if 'Country' in combined_df.columns:
            print("\n국가별 데이터:")
            print(combined_df['Country'].value_counts())
    
    conn.close()
    print("\n[완료] Production 데이터베이스 설정 완료!")

if __name__ == "__main__":
    setup_production_database()

