from libs.json import load_from_json

def process_recommend_famous_restaurant():
    """
        맛집 추천 전처리 함수
        
        Returns:
            {
                ...
                '한화': [{'category_name': '음식점 > 분식', 'place_name': '복수분식 본점'},
                {'category_name': '음식점 > 한식 > 해물,생선 > 게,대게', 'place_name': '여수게장백반 본점'},
                {'category_name': '음식점 > 한식 > 해물,생선 > 장어',
                'place_name': '신토불이추어탕 민물장어전문점'}]}
                ...
            }
    """
    data = load_from_json("./data/inspection/kakao_search_results.json");

    team_keys = {
        "LG 트윈스": "LG",
        "두산 베어스": "두산",
        "삼성 라이온즈": "삼성",
        "롯데 자이언츠": "롯데",
        "한화 이글스": "한화",
        "KIA 타이거즈": "KIA",
        "SSG 랜더스": "SSG",
        "KT 위즈": "KT",
        "키움 히어로즈": "키움",
        "NC 다이노스": "NC"
    }

    result = {}

    for full_name, short_name in team_keys.items():
        restraunts = data[full_name]
        result[short_name] = [
            {
                "place_name": restraunt["place_name"],
                "category_name": restraunt["category_name"],
                "address_name": restraunt["address_name"],
                "url": restraunt["place_url"]
            }
            for restraunt in restraunts
        ]

    return result
