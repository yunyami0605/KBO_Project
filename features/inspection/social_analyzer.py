# features/social_analyzer.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr, linregress
from typing import Dict, Any
import json

class SocialAnalyzer:
    """SNS 팔로워 vs 경기 관중수 및 구단나이 상관분석 클래스"""

    def __init__(self, data_path: str = "data/kbo_sns_followers.json"):
        """JSON 파일에서 데이터 로드"""
        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)
        self.df = pd.DataFrame(data)

    def filter(self, years: int) -> pd.DataFrame:
        """최근 years년 데이터 필터링"""
        latest = self.df["연도"].max()
        return self.df[self.df["연도"] >= latest - years + 1]

    def calc_corr(self, df: pd.DataFrame) -> Dict[str, Any]:
        """팔로워-관중수 및 구단나이-관중수 상관계수 계산"""
        n = len(df)
        result = {"size": n}
        if n < 2:
            result.update({
                "followers_attendance_pearson": None,
                "followers_attendance_pval": None,
                "followers_attendance_spearman": None,
                "followers_attendance_spearman_pval": None,
                "age_attendance_pearson": None,
                "age_attendance_pval": None,
                "age_attendance_spearman": None,
                "age_attendance_spearman_pval": None,
            })
            return result

        pr, pp = pearsonr(df["SNS팔로워수"], df["총관중수"])
        sr, sp = spearmanr(df["SNS팔로워수"], df["총관중수"])
        ar, ap = pearsonr(df["구단나이"], df["총관중수"])
        as_, asp = spearmanr(df["구단나이"], df["총관중수"])
        result.update({
            "followers_attendance_pearson": pr,
            "followers_attendance_pval": pp,
            "followers_attendance_spearman": sr,
            "followers_attendance_spearman_pval": sp,
            "age_attendance_pearson": ar,
            "age_attendance_pval": ap,
            "age_attendance_spearman": as_,
            "age_attendance_spearman_pval": asp,
        })
        return result

    def scatter_followers_attendance(self, df: pd.DataFrame, years: int) -> go.Figure:
        """팔로워 vs 관중수 산점도 + 회귀선"""
        fig = px.scatter(df, x="SNS팔로워수", y="총관중수", color="연도",
                         hover_data=["구단"], title=f"SNS 팔로워 vs 관중수 ({years}년)")
        if len(df) > 1:
            x = df["SNS팔로워수"].to_numpy()
            y = df["총관중수"].to_numpy()
            reg = linregress(x, y)
            xr = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(
                x=xr, y=reg.slope * xr + reg.intercept,
                mode="lines", name=f"회귀선 (r={reg.rvalue:.2f})",
                line=dict(color="red", dash="dash")
            ))
        fig.update_layout(width=700, height=500)
        return fig

    def scatter_age_attendance(self, df: pd.DataFrame, years: int) -> go.Figure:
        """구단나이 vs 관중수 산점도 + 회귀선"""
        fig = px.scatter(df, x="구단나이", y="총관중수", color="연도",
                         hover_data=["구단"], title=f"구단 나이 vs 관중수 ({years}년)")
        if len(df) > 1:
            x = df["구단나이"].to_numpy()
            y = df["총관중수"].to_numpy()
            reg = linregress(x, y)
            xr = np.linspace(x.min(), x.max(), 100)
            fig.add_trace(go.Scatter(
                x=xr, y=reg.slope * xr + reg.intercept,
                mode="lines", name=f"회귀선 (r={reg.rvalue:.2f})",
                line=dict(color="red", dash="dash")
            ))
        fig.update_layout(width=700, height=500)
        return fig

    def trend_followers_attendance(self, df: pd.DataFrame) -> go.Figure:
        """연도별 팔로워 & 관중수 이중축 트렌드"""
        grouped = df.groupby("연도").agg({
            "SNS팔로워수": "mean",
            "총관중수": "mean"
        }).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=grouped["연도"], y=grouped["SNS팔로워수"],
            name="평균 SNS 팔로워", line=dict(color="blue")
        ))
        fig.add_trace(go.Scatter(
            x=grouped["연도"], y=grouped["총관중수"],
            name="평균 관중수", line=dict(color="orange"), yaxis="y2"
        ))
        fig.update_layout(
            xaxis_title="연도",
            yaxis_title="평균 SNS 팔로워",
            yaxis2=dict(title="평균 관중수", overlaying="y", side="right"),
            width=700, height=400
        )
        return fig
