from apis.kakao_map_search_api import KakaoMapLocalSearcherApi
from libs.json import load_from_json, save_to_json
        
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

