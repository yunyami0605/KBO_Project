import json
import pandas as pd
import os

def filter_kbo_winrate_data(
    json_file_path='data/kbo_team_winrate.json',
    output_json_path='data/kbo_winrate_filter.json'
):
    """
    KBO 팀 승률 데이터를 전처리하는 함수
    년도, 팀명, 승률만 추출하여 정리
    
    Args:
        json_file_path (str): 입력 JSON 파일 경로
        output_json_path (str): 출력 JSON 파일 경로
    
    Returns:
        pandas.DataFrame: 전처리된 데이터프레임
    """
    
    # JSON 파일 읽기
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print(f" 원본 데이터 로드 완료: {json_file_path}")
    except FileNotFoundError:
        print(f" 파일을 찾을 수 없습니다: {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f" JSON 파일 형식 오류: {json_file_path}")
        return None
    
    # 전처리된 데이터를 저장할 리스트
    preprocessed_data = []
    
    # 년도별로 데이터 처리
    for year, teams_data in raw_data.items():
        
        
        for team_info in teams_data:
            # 필요한 필드만 추출
            processed_record = {
                'year': int(year),
                'team': team_info['team'],
                'win_rate': float(team_info['win_rate'])
            }
            preprocessed_data.append(processed_record)
    
    # DataFrame 생성
    df = pd.DataFrame(preprocessed_data)
    
    # 년도 → 팀명 순으로 정렬
    df = df.sort_values(['year', 'win_rate'], ascending=[True, False]).reset_index(drop=True)
    
    # JSON으로 저장
    try:
        # 출력 디렉토리 생성
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        
        # DataFrame을 딕셔너리 리스트로 변환 후 JSON 저장
        result_data = df.to_dict('records')
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        
        
        # 파일 크기 확인
        file_size = os.path.getsize(output_json_path)
        print(f" 파일 크기: {file_size:,} bytes")
        
    except Exception as e:
        print(f" 파일 저장 오류: {e}")
        return df
    
    # 결과 요약 출력
    print(f"\n 전처리 결과 요약:")
    print(f"   • 총 레코드 수: {len(df):,}개")
    print(f"   • 처리된 년도: {sorted(df['year'].unique())}")
    print(f"   • 포함된 팀: {sorted(df['team'].unique())}")
    
    # 년도별 최고 승률 팀 출력
    print(f"\n 년도별 최고 승률 팀:")
    for year in sorted(df['year'].unique()):
        year_data = df[df['year'] == year]
        best_team = year_data.iloc[0]  # 승률 순 정렬이므로 첫 번째가 최고
        print(f"   {year}년: {best_team['team']} ({best_team['win_rate']:.3f})")
    
    return df

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🏟️  KBO 팀 승률 데이터 전처리 시작")
    print("=" * 60)
    
    # 전처리 실행
    df = filter_kbo_winrate_data()
    
    if df is not None:
        # 결과 미리보기
        print(f"\n📋 전처리된 데이터 미리보기 (상위 10개):")
        print(df.head(10).to_string(index=False))
        
        print(f"\n 전처리 완료!")
    else:
        print(f"\n 전처리 실패!")

if __name__ == "__main__":
    main()
