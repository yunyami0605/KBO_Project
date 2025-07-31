import requests
from dotenv import load_dotenv
import os
import json
from typing import List, Dict, Optional, Tuple

from libs.json import load_from_json, save_to_json

load_dotenv()

class KakaoMapLocalSearcherApi:
    def __init__(self):
        """
        KakaoMapLocalSearcher 클래스 초기화.
        환경변수에서 KAKAO_API_KEY를 로드하고 기본 설정을 구성합니다.
        """
        self.api_key = os.getenv("KAKAO_API_KEY")
        self.base_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

        if not self.api_key:
            raise ValueError("KAKAO_API_KEY 환경변수가 설정되지 않았습니다.")
        
    def search_items(self, query: str, sites: List[Tuple[float, float]], radius = 15000, size = 3, labels: Optional[List[str]] = None,) -> List[Dict]:
        """
        여러 좌표를 받아 라벨 기준으로 검색 결과를 반환합니다.

        Args:
            query (str): 검색 키워드
            sites (List[Tuple[float, float]]): (x, y) 좌표 리스트
            labels (List[str], optional): 각 좌표에 대응하는 라벨 리스트
            radius (int): 검색 반경
            size (int): 결과 개수

        Returns:
            Dict[str, List[Dict]]: {label: [검색 결과]} 형식의 딕셔너리
        """
        result: Dict[str, List[Dict]] = {}

        for i, (x, y) in enumerate(sites):
            # 라벨이 없거나, site에 비해 적게 줬을 경우, 빈 값 처리
            label = labels[i] if labels and i < len(labels) else ""
            results = self.search_one(query, x, y, radius, size)
            result[label] = results

        return result


    def search_one(self, query: str, x: float = None, y: float = None, radius: int = 15000, size: int = 3) -> List[Dict]:
        """
        카카오 로컬 API를 사용하여 장소를 검색하고 결과를 반환

        Args:
            query (str): 검색할 키워드 (예: "맛집")
            x (float, optional): 경도 좌표 -> (기본값 = None)
            y (float, optional): 위도 좌표 -> (기본값 = None)
            radius (int, optional): 검색 반경 -> (기본값 = None)
            size (int, optional): 반환할 결과 개수 -> (기본값 = 3)
            label (str) : 응답 데이터 라벨링

        Returns:
            List[Dict]: 검색 결과 리스트 (형식화된 데이터)
        """
        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        params = {"query": query, "size": size}

        if x and y:
            params["x"] = str(x)
            params["y"] = str(y)
            
        if radius:
            params["radius"] = str(radius)

        response = requests.get(self.base_url, headers=headers, params=params)

        if response.ok:
            documents = response.json().get("documents", [])
            results = [
                {
                    "place_name": p["place_name"],
                    "address_name": p["address_name"],
                    "category_name": p["category_name"],
                    "phone": p["phone"],
                    "place_url": p["place_url"],
                    "x": p["x"],
                    "y": p["y"],
                }
                for p in documents
            ]

            return results

            
        else:
            print("Error:", response.status_code, response.text)
            return []
        
if __name__ == "__main__":
    searcher = KakaoMapLocalSearcherApi()
    
    # JSON 로드
    loaded_data = load_from_json("./data/kbo_baseball_stadiums_info.json")

    if loaded_data:
        teams = loaded_data["teams"]

        sites = [(t["longitude"], t["latitude"]) for t in teams]
        labels = [t["team"] for t in teams]

        all_results = searcher.search_items("맛집", sites=sites, labels=labels)

        save_to_json("./data/inspection/kakao_search_results.json", all_results)

