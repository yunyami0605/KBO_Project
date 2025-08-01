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
output_file = os.path.join(output_dir, "kbo_team_rank_week.json")

# JSON 저장
all_data.to_json(output_file, orient='records', force_ascii=False, indent=4)

print(f"\n✅ 7일치 데이터 JSON 저장 완료: {output_file}")
