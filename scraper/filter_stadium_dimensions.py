import json
import math
import pandas as pd

def calculate_stadium_area(left_distance, right_distance, center_distance):
    """
    야구장 면적을 계산하는 함수
    
    Args:
        left_distance (float): 좌측 펜스까지의 거리 (m)
        right_distance (float): 우측 펜스까지의 거리 (m)
        center_distance (float): 중앙 펜스까지의 거리 (m)
    
    Returns:
        float: 야구장 면적 (제곱미터)
    """
    # 내야 면적 계산 (90피트 = 27.43m의 정사각형)
    infield_side = 27.43  # 90 feet in meters
    infield_area = infield_side ** 2
    
    # 외야 면적 계산 (타원형 부채꼴 근사)
    major_radius = center_distance
    minor_radius = (left_distance + right_distance) / 2
    outfield_area = (math.pi * major_radius * minor_radius) / 4
    
    return infield_area + outfield_area

def preprocess_kbo_stadium_data(
    json_file_path='data/kbo_stadium_dimensions.json',
    output_json_path='data/kbo_stadium_area_final.json'
):
    """
    KBO 구장 데이터를 전처리하는 메인 함수
    """
    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as f:
        stadium_data = json.load(f)
    
    # 데이터 처리
    processed_data = []
    
    # 딕셔너리 형태로 순회 (실제 파일 구조에 맞춤)
    for stadium_name, dimensions in stadium_data.items():
        left = dimensions['좌']
        right = dimensions['우']
        center = dimensions['중앙']
        
        # 삼성 라이온즈파크 오류 데이터 수정
        if '삼성' in stadium_name and right == 10.0:
            left = 99.5
            right = 99.5
            print(f" {stadium_name} 데이터 수정: 좌우 99.5m로 보정")
        
        # 면적 계산
        area = calculate_stadium_area(left, right, center)
        
        # 구장명 간소화
        simple_name = stadium_name.split(' (')[0]  # 괄호 앞부분만
        
        processed_data.append({
            '구장명': simple_name,
            '면적(m²)': round(area, 2)
        })
    
    # DataFrame 생성 및 정렬
    df = pd.DataFrame(processed_data)
    df = df.sort_values('면적(m²)', ascending=False).reset_index(drop=True)
    
    # JSON으로 저장
    result_dict = df.to_dict('records')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    
    print(f" 전처리 완료! 결과를 '{output_json_path}'에 저장했습니다.")
    print(f" 총 {len(df)}개 구장 처리")
    
    return df

if __name__ == "__main__":
    # 실행
    df = preprocess_kbo_stadium_data()
    print("\n=== 최종 결과 ===")
    print(df)
