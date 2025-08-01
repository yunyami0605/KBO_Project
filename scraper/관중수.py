import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import os

url = "https://www.koreabaseball.com/Record/Crowd/History.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

table = soup.find("table", class_="tData")
columns = [th.get_text(strip=True) for th in table.find("tr").find_all("th")]
data = []
for row in table.find_all("tr")[1:]:
    cells = [td.get_text(strip=True) for td in row.find_all("td")]
    if cells:
        data.append(cells)

df = pd.DataFrame(data, columns=columns)
df["연도"] = pd.to_numeric(df["연도"], errors="coerce")
df = df[df["연도"].between(2020, 2024)]

# 사용할 구단만
team_cols = ["삼성", "KIA", "롯데", "LG", "두산", "한화", "SSG", "키움", "NC", "KT"]

# 총관중수와 평균관중수 분리 함수
def split_total_avg(s):
    m = re.match(r"([0-9,]+)\s*\(([\d,]+)\)", s)
    if m:
        total = int(m.group(1).replace(",", ""))
        avg = int(m.group(2).replace(",", ""))
        return total, avg
    elif s.replace(",", "").isdigit():
        # 값만 있는 경우(코로나 등)
        return int(s.replace(",", "")), None
    else:
        return None, None

# 각 구단별로 분리
for team in team_cols + ["계"]:
    totals, avgs = [], []
    for v in df[team]:
        total, avg = split_total_avg(v)
        totals.append(total)
        avgs.append(avg)
    df[f"{team}_총관중수"] = totals
    df[f"{team}_평균관중수"] = avgs

# 필요한 컬럼만 남기기
cols_final = ["연도"]
for team in team_cols:
    cols_final += [f"{team}_총관중수", f"{team}_평균관중수"]
cols_final += ["계_총관중수"]

df_final = df[cols_final]
print(df_final)

# === json.dump로 저장 ===
save_path = "../data"
os.makedirs(save_path, exist_ok=True)
save_file = os.path.join(save_path, "kbo_crowd_2020_2024.json")

result = df_final.to_dict(orient="records")
with open(save_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"저장 완료: {save_file}")
