# scraper/statiz_team_stats.py

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_statiz_team_stats(season: int):
    """
    statiz.sporki.com에서 시즌별 팀 HR, ERA 스크래핑
    Args:
        season: 연도 (예: 2024)
    Returns:
        List[dict]]: [{'season':2024,'team':'LG','HR':120,'ERA':3.45}, ...]
    """
    # 1) 웹드라이버 설정 (헤드리스)
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    # 2) 시즌별 페이지 접속
    url = f"https://statiz.sporki.com/stat/team?season={season}"
    driver.get(url)
    time.sleep(2)

    # 3) 테이블 찾기
    table = driver.find_element(By.CSS_SELECTOR, "table.table.table-striped")
    headers = [th.text for th in table.find_elements(By.CSS_SELECTOR, "thead th")]

    # 컬럼 인덱스 찾기
    # 예: headers = ['순위','팀명',...,'HR','ERA',...]
    try:
        idx_team = headers.index("팀명")
        idx_hr   = headers.index("HR")
        idx_era  = headers.index("ERA")
    except ValueError:
        driver.quit()
        raise RuntimeError(f"{season}시즌: HR 또는 ERA 컬럼을 찾을 수 없습니다.")

    # 4) tbody rows 순회
    stats = []
    for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
        cols = row.find_elements(By.TAG_NAME, "td")
        team = cols[idx_team].text.strip()
        try:
            hr  = int(cols[idx_hr].text.strip().replace(",", ""))
            era = float(cols[idx_era].text.strip())
        except:
            continue
        stats.append({
            "season": season,
            "team": team,
            "HR": hr,
            "ERA": era
        })

    driver.quit()
    return stats

def main():
    # 최근 5시즌: 올해 포함 5개
    current_year = time.localtime().tm_year
    seasons = list(range(current_year - 4, current_year + 1))
    all_stats = []

    for s in seasons:
        try:
            data = scrape_statiz_team_stats(s)
            print(f"{s}시즌 스크래핑 완료: {len(data)}개")
            all_stats.extend(data)
        except Exception as e:
            print(f"{s}시즌 스크래핑 오류: {e}")
        time.sleep(1)

    # JSON 저장
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_file = os.path.join(data_dir, "kbo_team_stats.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_stats, f, ensure_ascii=False, indent=2)
    print(f"팀별 시즌별 HR·ERA 저장 완료: {out_file}")

if __name__ == "__main__":
    main()
