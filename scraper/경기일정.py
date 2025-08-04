from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json
from datetime import datetime

from libs.json import save_to_json

def convert_korean_date_to_str(date_text, year="2025"):
    # "8월 1일 (금)" → "8 1"
    try:
        month_day = date_text.split("월")
        month = int(month_day[0].strip())
        day = int(month_day[1].split("일")[0].strip())

        # 날짜 객체로 만들기
        date_obj = datetime.strptime(f"{year}-{month:02d}-{day:02d}", "%Y-%m-%d")

        # 원하는 형식으로 변환
        return date_obj.strftime("%y-%m-%d")  # '25-08-01'
    except Exception as e:
        print(f"변환 실패: {e}")
        return None



def fetch_kbo_schedule():
    # 크롬 옵션
    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={mobile_ua}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 오늘부터 7일간 탐색
    base_date = datetime.now()
    found = False
    # for i in range(7):
    target_date = "2025-08-04"
    url = f"https://m.sports.naver.com/kbaseball/schedule/index?category=kbo&date={target_date}"
    driver.get(url)
    driver.implicitly_wait(3)

    games_per_day = driver.find_elements(By.CSS_SELECTOR, "div[class*=ScheduleLeagueType_match_list_group]")

    data = []

    for games_day in games_per_day:
        
        title = games_day.find_element(By.CSS_SELECTOR, "em[class*=ScheduleLeagueType_title]")


        _time = ""
        _team = []
        
        games = games_day.find_elements(By.CSS_SELECTOR, "div[class*=MatchBox_item_content]")

        for game in games:

            # 경기 시간 가져오기
            time = game.find_element(By.CSS_SELECTOR, "div[class*=MatchBox_time]")

            _time = time.text.replace("경기 시간\n", "")

            # 팀
            teams = game.find_elements(By.CSS_SELECTOR, "strong[class*=MatchBoxHeadToHeadArea_team]")
            
            for team in teams:
                _team.append(team.text)

            data.append({
                "날짜": convert_korean_date_to_str(title.text),
                "시간": _time,
                "원정팀": _team[0],
                "홈팀": _team[1],
            })


    save_to_json("data/inspection/kbo_schedule.json", data)
    print(data)
    print(len(data))

    driver.quit()
    return []  # 7일 동안 경기가 없을 경우

# 실행 예시
if __name__ == "__main__":
    result = fetch_kbo_schedule()
    print(json.dumps(result, ensure_ascii=False, indent=2))
