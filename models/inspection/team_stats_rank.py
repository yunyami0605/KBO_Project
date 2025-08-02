

import pandas as pd

from libs.json import load_from_json


def get_team_stats_rank(stat_type = "defense"):
    '''
        stat_type 에 따른 순위 반환
    '''

    defense_team_raw_data = load_from_json(f"data/rank_spectators/kbo_team_{stat_type}_basic.json")
        
    # DataFrame으로 변환
    defense_team_data = pd.DataFrame(defense_team_raw_data)

    return defense_team_data["팀명"].tolist()
