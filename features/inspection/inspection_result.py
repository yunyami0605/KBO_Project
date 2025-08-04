
# 야구팬 성향 수치
from apis.weather_api import WeatherAPI
from libs.json import load_from_json
from pprint import pprint

from models.inspection.famous_restaurant import process_recommend_famous_restaurant
from models.inspection.team_stats_rank import get_team_stats_rank


personality_results = {
    "comfortable": {
        "name": "🍱편안파 - 쾌적함 & 먹거리 중시형", 
        "keyword": ["여유로운 시간", "맛있는 먹거리", "편안한 분위기", "피크닉 감성"],
        "content": [
            "야구장에서는 경기보다 함께 간 사람과의 분위기를 더 중요하게 여깁니다.",
            "먹거리, 날씨, 좌석의 편안함이 직관의 핵심!",
            "가족, 연인과 함께하는 낮 경기에서 힐링을 느낍니다.",
        ]
    },

    "profit": {
        "name": "⚾실속파 - 경기력 & 집중 중시형",
        "keyword": ["분석적", "맛있는 먹거리", "전략적 플레이", "선수 집중", "뷰 우선"],
        "content": [
            "경기력 중심! 멋진 수비, 선수 퍼포먼스를 보며 해설보다 더 잘 해설함.",
            "돔구장이나 시야 좋은 내야석에서 관전하는 걸 선호.",
            "혼잡보다 경기 자체의 퀄리티가 우선!",
        ]
    },

    "passion": {
        "name": "🔥 열정파 - 응원 & 분위기 중시형",
        "keyword": ["응원", "단체", "소리", "열정", "이벤트"],
        "content": [
            "야구는 응원이다!",
            "같은 팀 유니폼을 맞춰 입고 친구들이랑 외야석에서 목이 쉬도록 응원.",
            "홈런, 치어리더, 응원단, 단체 이벤트도 빠짐없이 참여!",
        ]
    },

    "better": {
        "name": "🚇 실용파 – 접근성 & 효율 중시형",
        "keyword": ["시간 효율", "교통 편의,", "빠른 입퇴장", "가성비", "편리"],
        "content": [
            "집이나 회사 근처, 대중교통 가까운 구장을 선호",
            "혼자서도 부담 없이 직관하고, 일정 끝나고 귀가도 빠르게",
            "경기보다 시간 관리, 편의성이 직관의 핵심!",
        ]
    },

}

class InspectionResult:

    '''
        날씨조건
        "sunny": 0,
        "rainy": 0,
        "cold": 0,
        "windy": 0,
    '''


    '''
        스탯 조건
        "defense": 0,
        "runner": 0,
        "hitter": 0,
        "pitcher": 0,
    '''

    def __init__(self, weather_api: WeatherAPI):
        self.weather_api = weather_api
        self.personality = {
            "comfortable": 0,
            "profit": 0,
            "passion": 0,
            "better": 0
        }

    # 결과치에 따른 유저 성향 설정
    def set_personality(self, arr):
        for value in arr:
            if value in self.personality:
                self.personality[value] += 1

    # 가장 높은 유저 성향 반환
    def get_max_personality(self):
        return max(self.personality, key=self.personality.get)
    
    # 유저 취향 날씨
    def get_selected_weather(self, arr):
        for tag in ["sunny", "rainy", "cold", "windy"]:
            if tag in arr:
                return tag
            
        return None
            
    # 없는 경우가 없어야함..
    
    def get_selected_stat(self, arr):
        '''
        유저가 선택한 선수 스탯 종류 반환
        '''
        
        for stat in ["defense", "runner", "hitter", "pitcher"]:
            if stat in arr:
                return stat
            
        return "defense"
            
    
    def get_today_home_team_data(self):
        '''
        오늘 경기 홈팀 정보(위도, 경도, 팀이름) 가져오기
        '''
        pprint("### get_today_home_team_data start ###")

        stadium_data = load_from_json("data/kbo_baseball_stadiums_info.json")["teams"]
        schedule_data = load_from_json("data/inspection/kbo_schedule.json")

        home_teams = [item["홈팀"] for item in schedule_data]

        pprint(stadium_data)
        pprint(home_teams)
        pprint("### end ###")

        return {
            item["team"]: {
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "stadium": item["stadium"]
            }
            for item in stadium_data if item["team"] in home_teams
        }
    
    def get_recommend_weather_stadiums(self, selected_weather):
        '''
        조건 만족한 홈 경기장 리스트 반환 (없을 경우, 전체다 반환)
        각 stadium 위도/경도 정보 가져오기 -> 금일 홈 경기에 대한 정보 가져오기 -> 4개 홈 구장 날씨 가져오기

        Returns:
            "name": str,
            "location": {
                "latitude": str,
                "longitude": str,
            }[]

        '''
        stadiums_info = self.get_today_home_team_data()
        matched = []

        print("@@@ team")
        print(stadiums_info)

        for team, loc in stadiums_info.items():
            weather = self.weather_api.get_current_weather(f"{loc['latitude']},{loc['longitude']}")
            tags = []

            if weather:
                if weather["precip_mm"] >= 1:
                    tags.append("rainy")
                if weather["feelslike_c"] >= 27 or weather["feelslike_c"] < 10:
                    tags.append("cold")
                if weather["wind_kph"] >= 12:
                    tags.append("windy")
                if not tags:
                    tags.append("sunny")
            else:
                tags.append("error")

            if selected_weather in tags:
                matched.append({
                    "name": team,
                    "latitude": loc["latitude"], "longitude": loc["longitude"],
                    "stadium": loc["stadium"]
                    })
    
        # 날씨와 matched가 있으면 해당 구장 정보 반환, 없으면 전체 구장 정보 목록 반환
        return matched if matched else [
            {"name": team, "latitude": _data["latitude"], "longitude": _data["longitude"], "stadium": _data["stadium"]} for team, _data in stadiums_info.items()
        ]

    
    # 구장 추천
    def get_recommend_stadium(self, result_arr):
        '''
            로직 : 선택된 날씨에 해당하는 팀(스타디움) 선택 > 선택된 팀에서 스탯 높은 순으로 한 팀 봅음
        '''
        weather = self.get_selected_weather(result_arr)
        stat = self.get_selected_stat(result_arr)
        candidates = self.get_recommend_weather_stadiums(weather)
        team_rank = get_team_stats_rank(stat)

        pprint("@@@ candidates_SELECTED ")
        pprint(candidates)

        # 맛집 추천
        famous_rests = process_recommend_famous_restaurant()

        selected_team = None

        for team in team_rank:
            for item in candidates:
                if item["name"] == team:
                    selected_team = item  # 전체 dict 저장
                    break
            if selected_team:
                break

        pprint("@@@ selected_team_SELECTED ")
        pprint(selected_team)

        '''
        Return:
        {
            "team": {'latitdue', 'longitude', 'name', 'stadium}
            "famous_restaurants": [
                {
                    'address_name': string,
                    'category_name': string,
                    'place_name': string
                }
            ]
        }
        '''

        
            
        return {
            "team" : selected_team,
            "famous_restaurants": famous_rests[selected_team["name"]]
        }

    def get_personality_result(self, result_arr):
        print()
        print()
        print("# 성향 분석 시작 #")
        pprint(result_arr)

        self.set_personality(result_arr)
        max_key = self.get_max_personality()

        print(max_key)
        print(personality_results[max_key])

        print("# 성향 분석 끝 #")
        return personality_results.get(max_key, {})

