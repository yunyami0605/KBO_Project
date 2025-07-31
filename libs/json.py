import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union, Optional

def save_to_json(file_path: str, data: Union[List[Dict[str, Any]], Dict[str, Any]]):
    """
    누적된 검색 결과를 JSON 파일로 저장합니다.

    Args:
        file_path : 저장할 파일 이름
        data : 저장할 데이터
    """


    if file_path is None or data is None:
        raise ValueError("파일 이름")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except (TypeError, OverflowError) as e:
        raise TypeError(f"JSON 직렬화 실패: {e}\n지원하지 않는 데이터 타입")
    except Exception as e:
        raise OSError(f"파일 저장 실패: {e}")

    print(f"데이터가 {file_path}에 저장되었습니다.")

def load_from_json(file_path: str) -> Optional[List[Dict]]:
    """
    JSON 파일에서 검색 결과를 로드합니다.

    Args:
        file_path (str, optional): 로드할 파일 이름

    Returns:
        Optional[List[Dict]]: 로드된 데이터. 파일이 없으면 None 반환.
    """

    if file_path is None:
        raise ValueError("파일 이름")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            return data
        
    except FileNotFoundError:
        print(f"경고: {file_path} 파일을 찾을 수 없습니다.")
        return None

    except json.JSONDecodeError:
        print(f"경고: {file_path} 파일 형식이 잘못되었습니다.")
        return None