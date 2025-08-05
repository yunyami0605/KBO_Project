# features/social_analyzer.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from typing import Dict, Any
from libs.json import load_from_json


class SocialAnalyzer:
    """SNS 팔로워 vs 경기 관중수 및 구단 나이 상관관계 분석 클래스"""
    
    def __init__(self, data_path: str = 'data/kbo_sns_followers.json'):
        """
        생성자: JSON 파일에서 데이터 로드
        Args:
            data_path: SNS 팔로워 데이터 JSON 파일 경로
        """
        # 연도, 구단, 팔로워수, 총관중수, 구단나이 필드가 포함된 데이터 로드
        data = load_from_json(data_path)
        self.df = pd.DataFrame(data) if data else pd.DataFrame()
    
    def filter(self, years: int, team: str) -> pd.DataFrame:
        """
        지정된 년수와 팀으로 데이터 필터링
        Args:
            years: 분석할 년수 (1, 3, 5)
            team: 분석할 구단명 ('전체 구단' 또는 특정 구단명)
        Returns:
            필터링된 데이터프레임
        """
        # 최근 N년 데이터만 선택
        df = self.df[self.df['연도'] >= self.df['연도'].max() - years + 1]
        # 특정 구단 선택된 경우 해당 구단만 필터링
        if team != '전체 구단':
            df = df[df['구단'] == team]
        return df
    
    def calc_corr(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        상관관계 계산 (팔로워-관중수, 구단나이-관중수)
        Args:
            df: 분석할 데이터프레임
        Returns:
            상관계수 결과 딕셔너리
        """
        results = {}
        n = len(df)
        results['size'] = n
        
        # 최소 2개 데이터 포인트 필요 (상관계수 계산을 위한 방어 코드)
        if n < 2:
            results.update({
                'followers_attendance_pearson': None,
                'followers_attendance_spearman': None,
                'age_attendance_pearson': None,
                'age_attendance_spearman': None,
            })
            return results
        
        # 팔로워 수 - 관중수 상관관계 계산
        f_a_pearson, _ = pearsonr(df['SNS팔로워수'], df['총관중수'])
        f_a_spearman, _ = spearmanr(df['SNS팔로워수'], df['총관중수'])
        
        # 구단나이 - 관중수 상관관계 계산
        age_a_pearson, _ = pearsonr(df['구단나이'], df['총관중수'])
        age_a_spearman, _ = spearmanr(df['구단나이'], df['총관중수'])
        
        results.update({
            'followers_attendance_pearson': f_a_pearson,
            'followers_attendance_spearman': f_a_spearman,
            'age_attendance_pearson': age_a_pearson,
            'age_attendance_spearman': age_a_spearman,
        })
        
        return results
    
    def scatter_followers_attendance(self, df: pd.DataFrame, years: int) -> go.Figure:
        """
        팔로워-관중수 산점도 그래프 생성
        Args:
            df: 분석할 데이터프레임
            years: 분석 년수
        Returns:
            Plotly Figure 객체
        """
        fig = px.scatter(
            df, x='SNS팔로워수', y='총관중수', color='연도',
            hover_data=['구단', '연도'], title=f'SNS 팔로워 vs 총관중수 ({years}년간)',
            labels={'SNS팔로워수': 'SNS 팔로워 수', '총관중수': '총 관중수'}
        )
        
        # 회귀선 추가 (데이터 포인트가 2개 이상일 때)
        if len(df) > 1:
            reg = LinearRegression().fit(df[['SNS팔로워수']], df['총관중수'])
            x_range = np.linspace(df['SNS팔로워수'].min(), df['SNS팔로워수'].max(), 100)
            y_pred = reg.predict(x_range.reshape(-1, 1))
            fig.add_trace(go.Scatter(
                x=x_range, y=y_pred, mode='lines', name='회귀선',
                line=dict(color='red', dash='dash')
            ))
        
        fig.update_layout(height=500, width=700)
        return fig
    
    def scatter_age_attendance(self, df: pd.DataFrame, years: int) -> go.Figure:
        """
        구단나이-관중수 산점도 그래프 생성
        Args:
            df: 분석할 데이터프레임
            years: 분석 년수
        Returns:
            Plotly Figure 객체
        """
        fig = px.scatter(
            df, x='구단나이', y='총관중수', color='연도',
            hover_data=['구단', '연도'], title=f'구단 나이 vs 총관중수 ({years}년간)',
            labels={'구단나이': '구단 나이 (년)', '총관중수': '총 관중수'}
        )
        
        # 회귀선 추가 (데이터 포인트가 2개 이상일 때)
        if len(df) > 1:
            reg = LinearRegression().fit(df[['구단나이']], df['총관중수'])
            x_range = np.linspace(df['구단나이'].min(), df['구단나이'].max(), 100)
            y_pred = reg.predict(x_range.reshape(-1, 1))
            fig.add_trace(go.Scatter(
                x=x_range, y=y_pred, mode='lines', name='회귀선',
                line=dict(color='red', dash='dash')
            ))
        
        fig.update_layout(height=500, width=700)
        return fig
    
    def trend_followers_attendance(self, df: pd.DataFrame, team: str) -> go.Figure:
        """
        팔로워-관중수 연도별 트렌드 그래프 생성
        Args:
            df: 분석할 데이터프레임
            team: 구단명
        Returns:
            Plotly Figure 객체
        """
        # 연도별 평균값 계산
        grouped = df.groupby('연도').agg({
            'SNS팔로워수': 'mean', 
            '총관중수': 'mean'
        }).reset_index()
        
        # 이중 축 그래프 생성
        fig = go.Figure()
        
        # 왼쪽 축: SNS 팔로워 수
        fig.add_trace(go.Scatter(
            x=grouped['연도'], y=grouped['SNS팔로워수'],
            name='평균 SNS 팔로워 수', line=dict(color='blue', width=3)
        ))
        
        # 오른쪽 축: 총 관중수
        fig.add_trace(go.Scatter(
            x=grouped['연도'], y=grouped['총관중수'],
            name='평균 총 관중수', line=dict(color='orange', width=3),
            yaxis='y2'
        ))
        
        # 레이아웃 설정
        fig.update_layout(
            title=f'{team} 연도별 SNS 팔로워 & 총관중수 트렌드',
            yaxis=dict(title='평균 SNS 팔로워 수', color='blue'),
            yaxis2=dict(
                title='평균 총 관중수', overlaying='y', side='right', color='orange'
            ),
            xaxis=dict(title='연도'),
            height=400, width=700
        )
        return fig
