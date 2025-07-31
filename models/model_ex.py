import pandas as pd
import os


def extract_hitters_data(json_path: str = "hitters.json") -> pd.DataFrame:
    """
    hitters.json 파일에서 필요한 컬럼만 추출하여 DataFrame으로 반환합니다.

    Args:
        json_path (str): JSON 파일 경로 (기본값: "hitters.json")

    Returns:
        pd.DataFrame: 추출된 선수 데이터 (name, hit_ratio, homerun, hit_score, walk)
    """

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {json_path}")

    # JSON 파일을 pandas로 로드
    data = pd.read_json(json_path, encoding="utf-8")

    # 필요한 컬럼만 선택
    columns = ["name", "hit_ratio", "homerun", "hit_score", "walk"]

    # 컬럼이 모두 있는지 확인
    for col in columns:
        if col not in data.columns:
            raise ValueError(f"컬럼 '{col}'이 JSON에 존재하지 않습니다.")
        

    print(data[columns])

    return data[columns]