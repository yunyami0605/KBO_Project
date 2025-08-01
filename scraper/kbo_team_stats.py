from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os


save_dir = '../data'
os.makedirs(save_dir, exist_ok=True)

# 크롤링 대상 URL, 파일명 리스트
targets = [
    {
        'url': 'https://www.koreabaseball.com/Record/Team/Hitter/Basic1.aspx',
        'filename': 'kbo_team_hitter_basic.json',
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Team/Pitcher/Basic1.aspx',
        'filename': 'kbo_team_pitcher_basic.json',
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Team/Defense/Basic.aspx',
        'filename': 'kbo_team_defense_basic.json',
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Team/Runner/Basic.aspx',
        'filename': 'kbo_team_runner_basic.json',
    }
]

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


try:
    for target in targets:
        url = target['url']
        filename = target['filename']
        print(f"📄 크롤링 중: {url}")
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        thead = driver.find_element(By.TAG_NAME, 'thead')
        headers = thead.find_elements(By.TAG_NAME, 'th')
        column_names = [header.text.strip() for header in headers]

        tbody = driver.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')

        result = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            data = {}
            for i, cell in enumerate(cells):
                if i < len(column_names):
                    data[column_names[i]] = cell.text.strip()
                else:
                    data[f'추가정보_{i+1}'] = cell.text.strip()
            result.append(data)

        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ 저장 완료: {filename} (총 {len(result)}개 팀 기록)")

finally:
    driver.quit()

