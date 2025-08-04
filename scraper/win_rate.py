from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

# 브라우저 꺼짐 방지 옵션 (headless 모드)quit
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
        print(f"  {year}년 데이터 수집 중...")
        year_data = scrape_kbo_team_winrates(year)
        if year_data:
            all_data[str(year)] = year_data
            print(f"   {len(year_data)}개 팀 데이터 수집 완료")
        else:
            print(f"   {year}년 데이터 수집 실패")
        time.sleep(1)  # 서버 부하 방지
    
    # 현재 작업 디렉토리 확인
    current_dir = os.getcwd()
    print(f"현재 작업 디렉토리: {current_dir}")
    
    # 절대 경로로 data 폴더 생성 (KBO_PROJECT/data)
    # scraper 폴더에서 실행하므로 ../data 경로 사용
    if 'scraper' in current_dir:
        output_dir = os.path.join(os.path.dirname(current_dir), "data")
    else:
        output_dir = "data"
    
    print(f"JSON 파일 저장 경로: {output_dir}")
    
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # JSON 파일로 저장
    output_file = os.path.join(output_dir, "kbo_team_winrate.json")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        
        print(f"\n JSON 파일 저장 완료: {output_file}")
        print(f"파일 절대 경로: {os.path.abspath(output_file)}")
        print(f"총 {sum(len(data) for data in all_data.values())}개의 팀 레코드가 저장되었습니다.")
        
        # 파일이 실제로 생성되었는지 확인
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"파일 크기: {file_size} bytes")
        else:
            print("파일 생성 실패!")
            
    except Exception as e:
        print(f" 파일 저장 오류: {e}")
    
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
