from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import json
import os
from datetime import datetime

def scrape_kbo_schedule(target_date=None, save_dir="../data"):
    if target_date is None:
        target_date = datetime.today().strftime("%Y-%m-%d")

    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={mobile_ua}")
    chrome_options.add_argument("--headless")

# # 날짜 변수
# target_date = "2025-07-31"

    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://m.sports.naver.com/kbaseball/schedule/index?category=kbo&date={target_date}"
    driver.get(url)
    time.sleep(2)

    games = []
    lis = driver.find_elements(By.CSS_SELECTOR, "ul[class*=match_list] > li")

    for li in lis:
        try:
            status = li.find_element(By.CSS_SELECTOR, "em[class*=MatchBox_status]").text.strip()
        except:
            status = ""
        if status != "예정":
            continue

        try:
            time_ = li.find_element(By.CSS_SELECTOR, "[class*=MatchBox_time]").text.replace("경기 시간", "").strip()
        except:
            time_ = ""

        team_items = li.find_elements(By.CSS_SELECTOR, "div[class*=team_item]")
        if len(team_items) == 2:
            away_name = team_items[0].find_element(By.CSS_SELECTOR, "strong[class*=team]").text.strip()
            try:
                away_pitcher = team_items[0].find_element(By.CSS_SELECTOR, "span[class*=item]").text.strip()
            except:
                away_pitcher = ""
            home_name = team_items[1].find_element(By.CSS_SELECTOR, "strong[class*=team]").text.strip()
            try:
                home_pitcher = team_items[1].find_element(By.CSS_SELECTOR, "span[class*=item]").text.strip()
            except:
                home_pitcher = ""
            home_mark = team_items[1].find_elements(By.CSS_SELECTOR, "div[class*=home_mark]")
            if home_mark:
                home, away = home_name, away_name
                home_starter, away_starter = home_pitcher, away_pitcher
            else:
                home, away = away_name, home_name
                home_starter, away_starter = away_pitcher, home_pitcher

            games.append({
            "날짜": target_date,
            "시간": time_,
            "원정팀": away,
            "원정선발": away_starter,
            "홈팀": home,
            "홈선발": home_starter,
            })

    driver.quit()

    df = pd.DataFrame(games)
    print(df)

    # === json.dump로 저장 ===
    import os

    save_path = "../data"
    os.makedirs(save_path, exist_ok=True)
    save_file = os.path.join(save_path, f"kbo_schedule_{target_date}.json")

    result = df.to_dict(orient="records")

    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"저장 완료: {save_file}")