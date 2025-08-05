# features/social_analyzer.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr, linregress
from typing import Dict, Any
from libs.json import load_from_json


class SocialAnalyzer:
    """SNS 팔로워 vs 경기 관중수 및 구단 나이 상관관계 분석 클래스"""
    
    def __init__(self, data_path: str = 'data/kbo_sns_followers.json'):
        """생성자: JSON 파일에서 데이터 로드"""
        data = load_from_json(data_path) or []
        self.df = pd.DataFrame(data)
    
    def filter_by_years(self, years: int) -> pd.DataFrame:
        """지정된 년수만큼 최근 데이터 필터링"""
        latest = self.df['연도'].max()
        return self.df[self.df['연도'] >= latest - years + 1]
    
    def compute_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """상관계수 및 회귀식 통계 계산"""
        n = len(df)
        stats = {'sample_size': n}
        if n < 2:
            return {**stats, 'pearson_r': None, 'pearson_p': None,
                    'spearman_rho': None, 'spearman_p': None,
                    'reg_slope': None, 'reg_intercept': None, 'reg_r': None}
        
        pr, pp = pearsonr(df['SNS팔로워수'], df['총관중수'])
        sr, sp = spearmanr(df['SNS팔로워수'], df['총관중수'])
        reg = linregress(df['SNS팔로워수'], df['총관중수'])
        stats.update({
            'pearson_r': pr, 'pearson_p': pp,
            'spearman_rho': sr, 'spearman_p': sp,
            'reg_slope': reg.slope, 'reg_intercept': reg.intercept, 'reg_r': reg.rvalue
        })
        return stats
    
    def scatter_followers_vs_attendance(self, df: pd.DataFrame) -> go.Figure:
        """팔로워 vs 관중수 산점도 + 회귀선"""
        fig = px.scatter(df, x='SNS팔로워수', y='총관중수',
                         color='연도', hover_data=['구단'],
                         title="SNS 팔로워 vs 총 관중수")
        if len(df) > 1:
            x = df['SNS팔로워수']; y = df['총관중수']
            reg = linregress(x, y)
            xr = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(x=xr, y=reg.slope*xr+reg.intercept,
                                     mode='lines', name=f"회귀선 (r={reg.rvalue:.2f})",
                                     line=dict(color='red', dash='dash')))
        fig.update_layout(width=700, height=500)
        return fig
    
    def scatter_age_vs_attendance(self, df: pd.DataFrame) -> go.Figure:
        """구단 나이 vs 관중수 산점도 + 회귀선"""
        fig = px.scatter(df, x='구단나이', y='총관중수',
                         color='연도', hover_data=['구단'],
                         title="구단 나이 vs 총 관중수")
        if len(df) > 1:
            x = df['구단나이']; y = df['총관중수']
            reg = linregress(x, y)
            xr = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(x=xr, y=reg.slope*xr+reg.intercept,
                                     mode='lines', name=f"회귀선 (r={reg.rvalue:.2f})",
                                     line=dict(color='red', dash='dash')))
        fig.update_layout(width=700, height=500)
        return fig
    
    def histogram_followers(self, df: pd.DataFrame) -> go.Figure:
        """팔로워 수 히스토그램"""
        fig = px.histogram(df, x='SNS팔로워수', nbins=10,
                           title="SNS 팔로워 수 분포")
        fig.update_layout(width=700, height=300)
        return fig
    
    def boxplot_age_vs_attendance(self, df: pd.DataFrame) -> go.Figure:
        """구단 나이별 관중수 박스플롯"""
        fig = px.box(df, x='구단나이', y='총관중수',
                     title="구단 나이별 관중수 분포")
        fig.update_layout(width=700, height=400)
        return fig
