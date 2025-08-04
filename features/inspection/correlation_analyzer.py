import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr
from typing import Dict, List, Tuple, Optional
import os

from libs.json import load_from_json

class CorrelationAnalyzer:
    """승률과 관중수 상관관계 분석 클래스"""
    
    def __init__(self, data_file_path: str = 'data/kbo_merged_crowd_winrate.json'):
        """
        Args:
            data_file_path: 병합된 데이터 파일 경로
        """
        self.data_file_path = data_file_path
        self.df = None
        self.load_data()
    
    def load_data(self) -> None:
        """데이터 로드"""
        try:
            data = load_from_json(self.data_file_path)
            if data:
                self.df = pd.DataFrame(data)
                print(f" 데이터 로드 완료: {len(self.df)}개 레코드")
            else:
                raise FileNotFoundError("데이터를 불러올 수 없습니다.")
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
            self.df = None
    
    def filter_data_by_years(self, years: int) -> pd.DataFrame:
        """
        지정된 년수만큼 최근 데이터 필터링
        
        Args:
            years: 분석할 년수 (1, 3, 5)
        
        Returns:
            필터링된 DataFrame
        """
        if self.df is None:
            return pd.DataFrame()
        
        # 최근 N년 데이터만 선택
        latest_year = self.df['year'].max()
        start_year = latest_year - years + 1
        
        filtered_df = self.df[self.df['year'] >= start_year].copy()
        print(f"📅 {years}년 데이터 필터링: {start_year}-{latest_year} ({len(filtered_df)}개 레코드)")
        
        return filtered_df
    
    def calculate_correlation(self, df: pd.DataFrame) -> Dict:
        """
        상관관계 계산
        
        Args:
            df: 분석할 DataFrame
        
        Returns:
            상관관계 결과 딕셔너리
        """
        if df.empty:
            return {}
        
        # 피어슨 상관계수 (선형 관계)
        pearson_corr, pearson_p = pearsonr(df['win_rate'], df['avg_spectators'])
        
        # 스피어만 상관계수 (순위 관계)
        spearman_corr, spearman_p = spearmanr(df['win_rate'], df['avg_spectators'])
        
        # 상관관계 강도 해석
        def interpret_correlation(corr_value):
            abs_corr = abs(corr_value)
            if abs_corr >= 0.7:
                return "강한 상관관계"
            elif abs_corr >= 0.3:
                return "중간 상관관계"
            elif abs_corr >= 0.1:
                return "약한 상관관계"
            else:
                return "상관관계 없음"
        
        return {
            'pearson_correlation': round(pearson_corr, 4),
            'pearson_p_value': round(pearson_p, 4),
            'pearson_interpretation': interpret_correlation(pearson_corr),
            'spearman_correlation': round(spearman_corr, 4),
            'spearman_p_value': round(spearman_p, 4),
            'spearman_interpretation': interpret_correlation(spearman_corr),
            'sample_size': len(df),
            'years_analyzed': sorted(df['year'].unique().tolist())
        }
    
    def create_scatter_plot(self, df: pd.DataFrame, years: int) -> go.Figure:
        """
        산점도 그래프 생성 (Plotly)
        
        Args:
            df: 분석할 DataFrame
            years: 분석 년수
        
        Returns:
            Plotly Figure 객체
        """
        if df.empty:
            return go.Figure()
        
        # 상관계수 계산
        corr_result = self.calculate_correlation(df)
        pearson_corr = corr_result.get('pearson_correlation', 0)
        
        # 산점도 생성
        fig = px.scatter(
            df, 
            x='win_rate', 
            y='avg_spectators',
            color='year',
            hover_data=['team', 'year', 'total_spectators'],
            title=f'KBO 승률 vs 평균관중수 상관관계 ({years}년간)',
            labels={
                'win_rate': '승률',
                'avg_spectators': '평균 관중수 (명)',
                'year': '연도'
            }
        )
        
        # 회귀선 추가
        from sklearn.linear_model import LinearRegression
        X = df[['win_rate']]
        y = df['avg_spectators']
        
        if len(X) > 1:
            reg = LinearRegression().fit(X, y)
            x_range = np.linspace(df['win_rate'].min(), df['win_rate'].max(), 100)
            y_pred = reg.predict(x_range.reshape(-1, 1))
            
            fig.add_trace(go.Scatter(
                x=x_range,
                y=y_pred,
                mode='lines',
                name=f'회귀선 (r={pearson_corr:.3f})',
                line=dict(color='red', dash='dash')
            ))
        
        # 레이아웃 업데이트
        fig.update_layout(
            width=800,
            height=600,
            showlegend=True,
            font=dict(size=12),
            title_font_size=16
        )
        
        return fig
    
    def create_yearly_trend_plot(self, df: pd.DataFrame) -> go.Figure:
        """
        연도별 트렌드 그래프 생성
        
        Args:
            df: 분석할 DataFrame
        
        Returns:
            Plotly Figure 객체
        """
        if df.empty:
            return go.Figure()
        
        # 연도별 평균 계산
        yearly_stats = df.groupby('year').agg({
            'win_rate': 'mean',
            'avg_spectators': 'mean'
        }).reset_index()
        
        # 이중 축 그래프 생성
        fig = go.Figure()
        
        # 승률 선 (왼쪽 축)
        fig.add_trace(go.Scatter(
            x=yearly_stats['year'],
            y=yearly_stats['win_rate'],
            name='평균 승률',
            line=dict(color='blue', width=3),
            yaxis='y'
        ))
        
        # 관중수 선 (오른쪽 축)
        fig.add_trace(go.Scatter(
            x=yearly_stats['year'],
            y=yearly_stats['avg_spectators'],
            name='평균 관중수',
            line=dict(color='orange', width=3),
            yaxis='y2'
        ))
        
        # 레이아웃 설정
        fig.update_layout(
            title='연도별 평균 승률 vs 평균 관중수 트렌드',
            xaxis=dict(title='연도'),
            yaxis=dict(
                title='평균 승률',
                side='left',
                color='blue'
            ),
            yaxis2=dict(
                title='평균 관중수 (명)',
                side='right',
                overlaying='y',
                color='orange'
            ),
            width=800,
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    def get_team_ranking_by_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        팀별 승률-관중수 상관관계 순위
        
        Args:
            df: 분석할 DataFrame
        
        Returns:
            팀별 통계 DataFrame
        """
        if df.empty:
            return pd.DataFrame()
        
        team_stats = df.groupby('team').agg({
            'win_rate': ['mean', 'std'],
            'avg_spectators': ['mean', 'std'],
            'year': 'count'
        }).round(3)
        
        # 컬럼명 정리
        team_stats.columns = ['평균_승률', '승률_표준편차', '평균_관중수', '관중수_표준편차', '데이터_수']
        team_stats = team_stats.reset_index()
        
        # 승률 순으로 정렬
        team_stats = team_stats.sort_values('평균_승률', ascending=False)
        
        return team_stats
    
    def analyze_correlation_by_years(self, years: int) -> Dict:
        """
        지정된 년수로 상관관계 분석 실행
        
        Args:
            years: 분석할 년수 (1, 3, 5)
        
        Returns:
            분석 결과 딕셔너리
        """
        if self.df is None:
            return {}
        
        # 데이터 필터링
        filtered_df = self.filter_data_by_years(years)
        
        if filtered_df.empty:
            return {'error': f'{years}년 데이터가 없습니다.'}
        
        # 상관관계 계산
        correlation_result = self.calculate_correlation(filtered_df)
        
        # 그래프 생성
        scatter_plot = self.create_scatter_plot(filtered_df, years)
        trend_plot = self.create_yearly_trend_plot(filtered_df)
        
        # 팀별 순위
        team_ranking = self.get_team_ranking_by_correlation(filtered_df)
        
        return {
            'correlation_stats': correlation_result,
            'scatter_plot': scatter_plot,
            'trend_plot': trend_plot,
            'team_ranking': team_ranking,
            'filtered_data': filtered_df
        }
