import json
import pandas as pd

# 원본 JSON 파일 경로
input_path = "data/kbo_sns_followers.json"
# 추출한 데이터 저장 경로
output_path = "data/kbo_sns_followers_filter.json"

# JSON 파일 로드
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 데이터프레임 변환
df = pd.DataFrame(data)

# 필요한 컬럼만 선택
needed_cols = ['연도', '구단', '총관중수', 'SNS팔로워수', '구단나이']
df_extracted = df[needed_cols]

# 결과 확인 (선택적)
print(df_extracted.head())

# JSON 파일로 저장 (한글 깨짐 방지용, indent 포함)
df_extracted.to_json(output_path, orient='records', force_ascii=False, indent=2)

print(f"추출된 데이터가 {output_path}에 저장되었습니다.")
