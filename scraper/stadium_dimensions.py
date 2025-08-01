import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time
import re
from urllib.parse import quote

def StadiumDimensions():
    """
    나무위키에서 KBO 구장별 크기 데이터를 스크래핑합니다.
    (최종 보장판: 페이지 전체 텍스트에서 키워드와 숫자 쌍을 직접 찾는 방식으로 전면 재설계)
    """
    stadium_pages = {
        "잠실 야구장 (LG/두산)": "서울종합운동장 야구장",
        "고척 스카이돔 (키움)": "고척 스카이돔",
        "인천 SSG 랜더스필드 (SSG)": "인천 SSG 랜더스필드",
        "수원 KT 위즈 파크 (KT)": "수원 kt 위즈 파크", # 소문자 URL 수정
        "광주-기아 챔피언스 필드 (KIA)": "광주-기아 챔피언스 필드",
        "대전 한화생명 이글스파크 (한화)": "대전 한화생명 이글스파크",
        "대구 삼성 라이온즈 파크 (삼성)": "대구 삼성 라이온즈 파크",
        "창원 NC 파크 (NC)": "창원 NC 파크",
        "사직 야구장 (롯데)": "사직 야구장"
    }

    # 각 정보를 찾기 위한 키워드와 정규식 패턴
    patterns = {
        '좌우': re.compile(r'(?:좌우|좌ㆍ우)\s*(?:대칭|폴대|펜스)?[^0-9>]*(\d{2,3}(?:\.\d+)?)'),
        '좌': re.compile(r'(?<!우)\s*좌(?:측|익|쪽|왼쪽)[^0-9>]*(\d{2,3}(?:\.\d+)?)'),
        '우': re.compile(r'(?<!좌)\s*우(?:측|익|쪽|오른쪽)[^0-9>]*(\d{2,3}(?:\.\d+)?)'),
        '중앙': re.compile(r'(?:중앙|가운데|센터)\s*(?:펜스)?[^0-9>]*(\d{2,3}(?:\.\d+)?)'),
    }
    
    base_url = "https://namu.wiki/w/"
    final_data = {}
    
    print("KBO 구장 정보 스크래핑을 시작합니다 (최종 보장판)...")

    for name, page in stadium_pages.items():
        print(f"\n--- '{name}' 스크래핑 중 ---")
        scraped_info = {}
        try:
            url = base_url + quote(page)
            time.sleep(1)
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            response.raise_for_status()

            # HTML 구조를 무시하고, 페이지의 모든 텍스트를 가져옴
            soup = BeautifulSoup(response.text, 'html.parser')
            # 줄바꿈과 태그를 공백으로 변환하여 문장 연속성을 유지
            text = re.sub(r'<[^>]+>', ' ', response.text)
            text = re.sub(r'\s+', ' ', text) # 여러 공백을 하나로 축소

            # --- 패턴을 사용하여 텍스트에서 직접 정보 추출 ---
            # 1. 좌우 대칭 정보 최우선 탐색
            match_lr = patterns['좌우'].search(text)
            if match_lr:
                value = float(match_lr.group(1))
                scraped_info['좌'] = value
                scraped_info['우'] = value
            
            # 2. 개별 정보 탐색 (찾지 못한 경우에만)
            for key in ['좌', '우', '중앙']:
                if key not in scraped_info:
                    match = patterns[key].search(text)
                    if match:
                        scraped_info[key] = float(match.group(1))

            # --- 결과 판정 ---
            if all(k in scraped_info for k in ['좌', '우', '중앙']):
                final_data[name] = scraped_info
                print(f" 완벽 성공: {scraped_info}")
            else:
                print(f" 실패: 필수 정보를 모두 찾지 못했습니다. 수집된 정보: {scraped_info}")

        except Exception as e:
            print(f" 심각한 오류 발생: '{name}' 처리 중 문제가 발생했습니다. ({e})")

    # --- 최종 결과 보고 및 파일 저장 ---
    try:
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(data_dir, f'kbo_stadium_dimensions_scraped_{timestamp}.json')
        
        success_count = len(final_data)
        total_count = len(stadium_pages)

        print("\n" + "="*60)
        print("모든 스크래핑 작업이 완료되었습니다.")
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"\n 파일 저장 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    StadiumDimensions()