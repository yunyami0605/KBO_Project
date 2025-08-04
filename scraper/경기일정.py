from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import pandas as pd

from libs.json import save_to_json

def convert_korean_date_to_str(date_text, year="2025"):
    # "8월 1일 (금)" → "8 1"
    try:
        month_day = date_text.split("월")
        month = int(month_day[0].strip())
        day = int(month_day[1].split("일")[0].strip())

        date_obj = datetime.strptime(f"{year}-{month:02d}-{day:02d}", "%Y-%m-%d")
        return date_obj.strftime("%y-%m-%d")  # '25-08-01'
    except Exception as e:
        print(f"변환 실패: {e}")
        return None


def fetch_kbo_schedule(target_date: str, save_dir="data"):
    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={mobile_ua}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = f"https://m.sports.naver.com/kbaseball/schedule/index?category=kbo&date={target_date}"
    driver.get(url)
    driver.implicitly_wait(3)

    games_per_day = driver.find_elements(By.CSS_SELECTOR, "div[class*=ScheduleLeagueType_match_list_group]")
    data = []

    for games_day in games_per_day:
        title = games_day.find_element(By.CSS_SELECTOR, "em[class*=ScheduleLeagueType_title]")
        games = games_day.find_elements(By.CSS_SELECTOR, "div[class*=MatchBox_item_content]")

        for game in games:
            time = game.find_element(By.CSS_SELECTOR, "div[class*=MatchBox_time]").text.replace("경기 시간\n", "")
            teams = game.find_elements(By.CSS_SELECTOR, "strong[class*=MatchBoxHeadToHeadArea_team]")
            away, home = teams[0].text, teams[1].text
            data.append({
                "날짜": convert_korean_date_to_str(title.text),
                "시간": time,
                "원정팀": away,
                "홈팀": home,
            })

    driver.quit()

    os.makedirs("data/inspection", exist_ok=True)
    save_to_json("data/inspection/kbo_schedule.json", data)
    print(data)
    print(len(data))

    return pd.DataFrame(data), data

if __name__ == "__main__":
    today = datetime.today().strftime("%Y-%m-%d")
    fetch_kbo_schedule(today)

