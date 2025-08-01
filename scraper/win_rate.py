import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def KBOWINRATE():
    """
    최근 5년간의 KBO 팀 순위 데이터를 스크래핑하여 JSON 파일로 저장합니다.
    """
    # 현재 연도를 기준으로 최근 5년치(올해 포함)를 대상 기간으로 설정합니다.
    current_year = datetime.now().year
    years_to_scrape = range(current_year - 4, current_year + 1)

    all_years_data = {}

    print(f"KBO 팀 순위 스크래핑을 시작합니다. 대상 연도: {list(years_to_scrape)}")

    for year in years_to_scrape:
        # 연도별 순위 페이지 URL
        url = f"https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx?season={year}"
        try:
            response = requests.get(url)
            # HTTP 요청이 성공했는지 확인합니다 (200 OK).
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            # 순위 데이터가 담긴 테이블을 찾습니다.
            table = soup.find('table', {'class': 'tData'})

            if table:
                # 테이블 헤더 (순위, 팀명, 경기수 등)를 추출합니다.
                headers = [header.get_text(strip=True) for header in table.find_all('th')]
                
                team_data_for_year = []
                # 테이블의 각 행(팀) 데이터를 추출합니다.
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    row_data = {headers[i]: col.get_text(strip=True) for i, col in enumerate(cols)}
                    team_data_for_year.append(row_data)
                
                # 연도별로 데이터를 딕셔너리에 저장합니다.
                all_years_data[year] = team_data_for_year
                print(f"성공: {year}년 데이터를 스크래핑했습니다.")
            else:
                print(f"경고: {year}년 데이터에서 팀 순위 테이블을 찾을 수 없습니다.")

        except requests.exceptions.RequestException as e:
            print(f"오류: {year}년 페이지를 가져오는 데 실패했습니다: {e}")

    # --- 파일 저장 로직 ---
    # 이 스크립트 파일(win_rate.py)의 위치를 기준으로 상위 폴더로 이동한 후 data 폴더의 경로를 설정합니다.
    # 스크립트 위치: /KBO_Project/scraper/
    # 데이터 저장 위치: /KBO_Project/data/
    try:
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, '..', 'data')

        # 'data' 디렉토리가 없으면 생성합니다.
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"'{data_dir}' 디렉토리를 생성했습니다.")

        # 현재 시간을 기준으로 파일명을 생성합니다. (예: kbo_team_rankings_20250801_100511.json)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(data_dir, f'kbo_team_rankings_{timestamp}.json')

        # 스크래핑한 전체 데이터를 JSON 파일로 저장합니다.
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_years_data, f, ensure_ascii=False, indent=4)
        
        print(f"\n스크래핑 완료! 모든 데이터가 성공적으로 아래 경로에 저장되었습니다:\n{os.path.abspath(file_path)}")

    except Exception as e:
        print(f"\n파일 저장 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    
    KBOWINRATE()