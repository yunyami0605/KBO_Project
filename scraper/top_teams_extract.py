import pandas as pd

def load_top_team(filepath, category):
    df = pd.read_json(filepath, encoding='utf-8')
    df["순위"] = df["순위"].astype(str)
    top_team = df[df["순위"] == "1"][["순위", "팀명"]]
    top_team["종류"] = category
    return top_team

file_info = {
    "타자": "../data/rank_spectators/kbo_team_hitter_basic.json",
    "수비": "../data/rank_spectators/kbo_team_defense_basic.json",
    "투수": "../data/rank_spectators/kbo_team_pitcher_basic.json",
    "도루": "../data/rank_spectators/kbo_team_runner_basic.json"
}


result_list = [load_top_team(path, kind) for kind, path in file_info.items()]
result_df = pd.concat(result_list)[["종류", "순위", "팀명"]].reset_index(drop=True)

print(result_df)
print(result_df.values.tolist())