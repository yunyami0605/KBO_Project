import requests
from dotenv import load_dotenv
import os
from typing import Dict, Optional

load_dotenv()

class WeatherAPI:
    """
    WeatherAPI.com의 날씨 데이터를 가져오는 클래스
    """
    
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    
    def __init__(self, api_key: str = None):
        """
        Args:
            api_key (str, optional): WeatherAPI.com 키
        """
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("API 키가 없습니다.")

    def get_current_weather(self, location: str) -> Optional[Dict]:
        """
        현재 날씨 정보 조회
        
        Args:
            location (str): 위치 (예: "37.5665,126.9780" 또는 "서울")
            
        Returns:
            Optional[Dict]: {
                "temp_c": float,       # 현재 온도(℃)
                "feelslike_c": float,  # 체감 온도(℃)
                "humidity": int,       # 습도(%)
                "wind_kph": float,     # 풍속(km/h)
                "wind_dir": str,       # 풍향 (예: "NE")
                "uv": float,           # 자외선 지수
                "precip_mm": float     # 강수량(mm)
            }
        """
        params = {
            "key": self.api_key,
            "q": location,
            "units": "metric",
            "lang": "ko"  # 한국어 응답
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # 4xx/5xx 에러 시 예외 발생
            
            current = response.json().get("current", {})
            
            # 요청하신 필드만 추출
            return {
                "temp_c": current.get("temp_c"),
                "feelslike_c": current.get("feelslike_c"),
                "humidity": current.get("humidity"),
                "wind_kph": current.get("wind_kph"),
                "wind_dir": current.get("wind_dir"),
                "uv": current.get("uv"),
                "precip_mm": current.get("precip_mm")
            }
        

        except requests.exceptions.RequestException as e:
            print(f"날씨 조회 실패: {e}")
            return None


'''

from apis.weather_api import WeatherAPI


if __name__ == "__main__":
    # 사용 예시
    weather = WeatherAPI()
    
    seoul_weather = weather.get_current_weather("37.5665,126.9780")
    
    if seoul_weather:
        print(seoul_weather)
    else:
        print("날씨 데이터를 가져오지 못했습니다.")
'''