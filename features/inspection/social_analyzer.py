import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from typing import Dict, Any

from libs.json import load_from_json

class SocialAnalyzer:
    """SNS 팔로워 vs 경기 관중수 상관관계 분석 클래스"""

    def __init__(self,
                 crowd_winrate_path: str = 'data/kbo_merged_crowd_winrate.json',
                 sns_path: str = 'data/kbo_sns_followers.json'):
        # 관중+승률 데이터
        data = load_from_json(crowd_winrate_path) or []
        self.df = pd.DataFrame(data)
        # SNS 팔로워 데이터: [{'year':2024,'team':'LG','followers':12345}, ...]
        sns_data = load_from_json(sns_path) or []
        self.sns = pd.DataFrame(sns_data)
        # 병합
        if not self.df.empty and not self.sns.empty:
            self.df = pd.merge(
                self.df, self.sns,
                on=['year','team'], how='inner'
            )

    def filter(self, years: int, team: str) -> pd.DataFrame:
        df = self.df[self.df['year'] >= self.df['year'].max()-years+1]
        if team!='전체 구단':
            df = df[df['team']==team]
        return df

    def calc_corr(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df.shape[0]<2:
            return {'pearson':None,'spearman':None,'size':df.shape[0]}
        p_corr,p_p = pearsonr(df['followers'], df['avg_spectators'])
        s_corr,s_p = spearmanr(df['followers'], df['avg_spectators'])
        return {
            'pearson':round(p_corr,4),
            'pearson_p':round(p_p,4),
            'spearman':round(s_corr,4),
            'spearman_p':round(s_p,4),
            'size':df.shape[0]
        }

    def scatter(self, df: pd.DataFrame, years:int) -> go.Figure:
        fig = px.scatter(
            df, x='followers', y='avg_spectators', color='year',
            hover_data=['team'], title=f'팔로워 vs 평균관중수 ({years}년)'
        )
        if df.shape[0]>1:
            reg=LinearRegression().fit(df[['followers']],df['avg_spectators'])
            xr=np.linspace(df['followers'].min(),df['followers'].max(),100)
            yr=reg.predict(xr.reshape(-1,1))
            fig.add_trace(go.Scatter(x=xr,y=yr,mode='lines',
                                     name='회귀선',line=dict(color='red')))
        fig.update_layout(width=700,height=500)
        return fig

    def trend(self, df: pd.DataFrame, team:str) -> go.Figure:
        ys=df.groupby('year').agg({'followers':'mean','avg_spectators':'mean'}).reset_index()
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=ys['year'],y=ys['followers'],
                                 name='평균 팔로워',line=dict(color='green')))
        fig.add_trace(go.Scatter(x=ys['year'],y=ys['avg_spectators'],
                                 name='평균 관중수',line=dict(color='orange'),
                                 yaxis='y2'))
        fig.update_layout(
            title=f"{team} 연도별 팔로워 & 관중수 트렌드",
            xaxis_title='연도',
            yaxis_title='평균 팔로워',
            yaxis2=dict(title='평균 관중수',overlaying='y',side='right'),
            width=700,height=400
        )
        return fig
