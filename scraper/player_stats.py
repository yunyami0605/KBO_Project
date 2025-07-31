from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# 폴더 설정
save_dir = '../data'
os.makedirs(save_dir, exist_ok=True)

# 크롤링할 URL 목록과 파일명
targets = [
    {
        'url': 'https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx',
        'filename': 'kbo_hitter_basic.json',
        'columns': 16
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx',
        'filename': 'kbo_pitcher_basic.json',
        'columns': 16
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Player/Defense/Basic.aspx',
        'filename': 'kbo_defense_basic.json',
        'columns': 9
    },
    {
        'url': 'https://www.koreabaseball.com/Record/Player/Runner/Basic.aspx',
        'filename': 'kbo_runner_basic.json',
        'columns': 8
    }
]

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



for target in targets:
    url = target['url']
    filename = target['filename']
    min_columns = target['columns']
    
    print(f"📄 크롤링 중: {url}")
    driver.get(url)
    time.sleep(3)
    
    # 📌 컬럼명 추출
    thead = driver.find_element(By.TAG_NAME, 'thead')
    headers = thead.find_elements(By.TAG_NAME, 'th')
    column_names = [header.text.strip() for header in headers]

    result = []
    tbody = driver.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) < min_columns:
            continue

        data = {}
        for i, cell in enumerate(cells):
            if i < len(column_names):  # 컬럼 수 일치 여부 확인
                data[column_names[i]] = cell.text.strip()
            else:
                data[f'추가정보_{i+1}'] = cell.text.strip()
        result.append(data)

    # JSON 저장
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"✅ 저장 완료: {filename} (총 {len(result)}명)")
