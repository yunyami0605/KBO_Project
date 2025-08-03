import json
import pandas as pd
import os

def merge_crowd_and_winrate_data(
    crowd_file_path='data/kbo_crowd_2020_2024.json',
    winrate_file_path='data/kbo_winrate_filter.json',
    output_json_path='data/kbo_merged_crowd_winrate.json'
):
    """
    관중수 데이터와 승률 데이터를 통합하는 함수
    
    Args:
        crowd_file_path (str): 관중수 데이터 JSON 파일 경로
        winrate_file_path (str): 승률 데이터 JSON 파일 경로
        output_json_path (str): 통합된 결과 JSON 파일 경로
    
    Returns:
        pandas.DataFrame: 통합된 데이터프레임
    """
    
    print("=" * 60)
    print("📊 KBO 관중수 + 승률 데이터 통합 시작")
    print("=" * 60)
    
    # 1. 관중수 데이터 로드
    try:
        with open(crowd_file_path, 'r', encoding='utf-8') as f:
            crowd_data = json.load(f)
        print(f" 관중수 데이터 로드 완료: {len(crowd_data)}개 연도")
    except FileNotFoundError:
        print(f" 관중수 파일을 찾을 수 없습니다: {crowd_file_path}")
        return None
    
    # 2. 승률 데이터 로드
    try:
        with open(winrate_file_path, 'r', encoding='utf-8') as f:
            winrate_data = json.load(f)
        print(f" 승률 데이터 로드 완료: {len(winrate_data)}개 레코드")
    except FileNotFoundError:
        print(f" 승률 파일을 찾을 수 없습니다: {winrate_file_path}")
        return None
    
    # 3. 관중수 데이터 전처리 (넓은 형태 → 긴 형태로 변환)
    crowd_records = []
    team_mapping = {
        '삼성': '삼성',
        'KIA': 'KIA', 
        '롯데': '롯데',
        'LG': 'LG',
        '두산': '두산',
        '한화': '한화',
        'SSG': 'SSG',
        '키움': '키움',
        'NC': 'NC',
        'KT': 'KT'
    }
    
    
    for year_data in crowd_data:
        year = year_data['연도']
        
        
        for team_key, team_name in team_mapping.items():
            total_key = f"{team_key}_총관중수"
            avg_key = f"{team_key}_평균관중수"
            
            if total_key in year_data and avg_key in year_data:
                crowd_records.append({
                    'year': year,
                    'team': team_name,
                    'total_spectators': year_data[total_key],
                    'avg_spectators': year_data[avg_key]
                })
    
    # 4. 승률 데이터를 DataFrame으로 변환
    winrate_df = pd.DataFrame(winrate_data)
    crowd_df = pd.DataFrame(crowd_records)
    
    
    print(f"   • 승률 데이터: {len(winrate_df)}개 레코드")
    print(f"   • 관중수 데이터: {len(crowd_df)}개 레코드")
    
    # 5. 팀명 매핑 (승률 데이터의 팀명을 관중수 데이터 팀명에 맞춤)
    team_name_mapping = {
        'SK': 'SSG',  # SK → SSG 변경
        # 나머지는 동일
    }
    
    winrate_df['team'] = winrate_df['team'].replace(team_name_mapping)
    
    # 6. 데이터 병합 (year, team 기준으로 조인)
   
    merged_df = pd.merge(
        winrate_df, 
        crowd_df, 
        on=['year', 'team'], 
        how='inner'  # 양쪽 모두 있는 데이터만
    )
    
    print(f" 병합 완료: {len(merged_df)}개 레코드")
    
    # 7. 정렬 (년도 → 승률 순)
    merged_df = merged_df.sort_values(['year', 'win_rate'], ascending=[True, False]).reset_index(drop=True)
    
    # 8. JSON으로 저장
    try:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        
        result_data = merged_df.to_dict('records')
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f" 통합 데이터 저장 완료: {output_json_path}")
        
        # 파일 크기 확인
        file_size = os.path.getsize(output_json_path)
        print(f" 파일 크기: {file_size:,} bytes")
        
    except Exception as e:
        print(f" 파일 저장 오류: {e}")
        return merged_df
    
    # 9. 결과 요약 출력
    print(f"\n 통합 데이터 요약:")
    print(f"   • 총 레코드 수: {len(merged_df):,}개")
    print(f"   • 처리된 년도: {sorted(merged_df['year'].unique())}")
    print(f"   • 포함된 팀: {sorted(merged_df['team'].unique())}")
    
    # 년도별 승률-관중수 상관관계 미리보기
    print(f"\n 년도별 승률 1위 팀과 관중수:")
    for year in sorted(merged_df['year'].unique()):
        year_data = merged_df[merged_df['year'] == year]
        best_team = year_data.iloc[0]  # 승률 순 정렬이므로 첫 번째가 최고
        print(f"   {year}년: {best_team['team']} - 승률 {best_team['win_rate']:.3f}, "
              f"평균관중 {best_team['avg_spectators']:,}명")
    
    return merged_df

def main():
    """메인 실행 함수"""
    # 데이터 통합 실행
    df = merge_crowd_and_winrate_data()
    
    if df is not None:
        # 결과 미리보기
        print(f"\n 통합된 데이터 미리보기 (상위 10개):")
        print(df.head(10).to_string(index=False))
        
    
    else:
        print(f"\n 데이터 통합 실패")

if __name__ == "__main__":
    main()
