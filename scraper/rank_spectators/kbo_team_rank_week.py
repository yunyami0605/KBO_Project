from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
from datetime import datetime, timedelta

options = Options()
options.add_argument("--headless")

# 날짜 리스트 만들기 
def get_date_list(days=7):
    today = datetime.today()
    return [(today - timedelta(days=i)).strftime("%Y%m%d") for i in range(days)]

# 데이터 크롤링 함수
def crawl_kbo_team_rank(date_str):
    url = f'https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx?gameDate={date_str}'
    driver.get(url)
    time.sleep(3)  
    
    table = driver.find_element(By.CSS_SELECTOR, 'table.tData')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols:
            data.append([col.text for col in cols])
    
    columns = ['순위', '팀명', '경기', '승', '패', '무', '승률', '게임차', '최근10경기', '연속', '홈', '방문']
    df = pd.DataFrame(data, columns=columns)
    df['날짜'] = datetime.strptime(date_str, "%Y%m%d").strftime('%Y-%m-%d')  # 문자열 변환
    return df

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 날짜별 데이터 수집
date_list = get_date_list(7)
all_data = pd.DataFrame()

for date_str in date_list:
    print(f"크롤링 중: {date_str}")
    df = crawl_kbo_team_rank(date_str)
    all_data = pd.concat([all_data, df], ignore_index=True)

driver.quit()

output_dir = "../../data/rank_spectators"
os.makedirs(output_dir, exist_ok=True)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

# 브라우저 꺼짐 방지 옵션 (headless 모드)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_kbo_team_winrates(year):
    """특정 연도의 KBO 팀 순위 및 승률 데이터 스크래핑"""
    url = 'https://www.koreabaseball.com/record/teamrank/teamrank.aspx'
    driver.get(url)
    time.sleep(3)
    
    try:
        # 연도 선택 드롭다운 찾기 및 선택
        year_dropdown = driver.find_element(By.CSS_SELECTOR, 'select')
        select = Select(year_dropdown)
        select.select_by_visible_text(str(year))
        time.sleep(2)
        
        # 팀 순위 테이블 찾기
        table = driver.find_element(By.CSS_SELECTOR, 'table.tData')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        # 데이터 수집
        year_data = []
        for i, row in enumerate(rows):
            if i == 0:  # 헤더 행 건너뛰기
                continue
            cols = row.find_elements(By.TAG_NAME, 'td')
            if cols and len(cols) >= 7:
                try:
                    team_data = {
                        'rank': int(cols[0].text.strip()),
                        'team': cols[1].text.strip(),
                        'games': int(cols[2].text.strip()),
                        'wins': int(cols[3].text.strip()),
                        'losses': int(cols[4].text.strip()),
                        'draws': int(cols[5].text.strip()),
                        'win_rate': float(cols[6].text.strip())
                    }
                    year_data.append(team_data)
                except ValueError:
                    continue
        
        return year_data
        
    except Exception as e:
        print(f"{year}년 데이터 스크래핑 오류: {e}")
        return []

def main():
    # 최근 5년 데이터 수집
    years = [2020, 2021, 2022, 2023, 2024]
    all_data = {}
    
    print("KBO 최근 5년 구단별 승률 데이터 스크래핑 시작...")
    
    for year in years:
        print(f"  ▶ {year}년 데이터 수집 중...")
        year_data = scrape_kbo_team_winrates(year)
        if year_data:
            all_data[str(year)] = year_data
            print(f"    ✔ {len(year_data)}개 팀 데이터 수집 완료")
        else:
            print(f"    ✗ {year}년 데이터 수집 실패")
        time.sleep(1)  # 서버 부하 방지
    
    # 출력 디렉토리 생성 (data 폴더)
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    
    # JSON 파일로 저장
    output_file = os.path.join(output_dir, "kbo_team_winrate.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ JSON 파일 저장 완료: {output_file}")
    print(f"총 {sum(len(data) for data in all_data.values())}개의 팀 레코드가 저장되었습니다.")
    
    # 연도별 승률 요약 출력
    print("\n=== 최근 5년 KBO 구단별 승률 요약 ===")
    for year, teams in all_data.items():
        print(f"\n{year}년:")
        sorted_teams = sorted(teams, key=lambda x: x['win_rate'], reverse=True)
        for team in sorted_teams:
            print(f"  {team['rank']:2d}. {team['team']:4s}: {team['win_rate']:.3f} "
                  f"({team['wins']}승 {team['losses']}패 {team['draws']}무)")
    
    # 드라이버 종료
    driver.quit()

if __name__ == "__main__":
    main()

# JSON 저장
all_data.to_json(output_file, orient='records', force_ascii=False, indent=4)

print(f"\n✅ 7일치 데이터 JSON 저장 완료: {output_file}")
