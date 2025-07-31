from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# 브라우저 꺼짐 방지 옵션 (headless 모드)
options = Options()
options.add_argument("--headless")

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = 'https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx'
driver.get(url)

time.sleep(3)

# 팀 순위 테이블 찾기
table = driver.find_element(By.CSS_SELECTOR, 'table.tData')
rows = table.find_elements(By.TAG_NAME, 'tr')

# 데이터 수집
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')
    if cols:
        data.append([col.text for col in cols])

columns = ['순위', '팀명', '경기', '승', '패', '무', '승률', '게임차', '최근10경기', '연속', '홈', '방문']

# DataFrame 생성
df = pd.DataFrame(data, columns=columns)

driver.quit()

output_dir = "../data"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "kbo_team_rank_daily.json")

# JSON 파일로 저장
df.to_json(output_file, orient='records', force_ascii=False, indent=4)

print(f"\n✅ JSON 파일 저장 완료: {output_file}")
