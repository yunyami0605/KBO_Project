# scraper/team_stats_selenium.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

def scrape_team_stats_selenium(year: int):
    """
    Selenium으로 KBO 팀별 시즌별 주요 기록(홈런 수, 방어율) 스크래핑
    """
    # ChromeDriver 자동 설치 + 로깅 숨기기 설정
    driver_path = ChromeDriverManager().install()
    # Windows: NUL, macOS/Linux: /dev/null
    log_path = 'NUL' if os.name == 'nt' else '/dev/null'
    service = Service(executable_path=driver_path, log_path=log_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.koreabaseball.com/TeamRank/TeamStat.aspx?season={year}&gameType=RR"
    driver.get(url)
    time.sleep(3)

    stats = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table.rank_tbl tbody tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 16:
            continue
        team = cols[1].text.strip()
        try:
            home_runs = int(cols[12].text.strip().replace(",", ""))
            era = float(cols[15].text.strip())
        except ValueError:
            continue
        stats.append({
            "year": year,
            "team": team,
            "home_runs": home_runs,
            "era": era
        })

    driver.quit()
    return stats

def main():
    all_stats = []
    current_year = time.localtime().tm_year
    for year in range(current_year - 4, current_year + 1):
        try:
            year_stats = scrape_team_stats_selenium(year)
            all_stats.extend(year_stats)
            print(f"{year}년 데이터 수집 완료: {len(year_stats)}개")
        except Exception as e:
            print(f"{year}년 수집 실패: {e}")
        time.sleep(1)

    output_path = "data/kbo_team_stats.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_stats, f, ensure_ascii=False, indent=2)
    print(f"팀별 시즌별 기록 저장 완료: {output_path}")

if __name__ == "__main__":
    main()