# app/social_section.py

import streamlit as st
import plotly.graph_objects as go
from features.inspection.social_analyzer import SocialAnalyzer  # 반드시 SocialAnalyzer 임포트

def render_social_section():
    """SNS 팔로워 vs 평균 관중수 상관관계 탭 렌더링"""

    st.subheader("📱 SNS 팔로워 vs 평균 관중수 분석")
    st.markdown("---")

    sa = SocialAnalyzer()           # SocialAnalyzer 인스턴스
    df = sa.df                      # SNS+관중수 병합된 DataFrame
    if df is None or df.empty:
        st.error("데이터를 불러올 수 없습니다. 'data/kbo_sns_followers.json'을 확인하세요.")
        return

    # 기간·구단 선택
    c1, c2 = st.columns([2, 2])
    with c1:
        yrs = st.selectbox("분석 기간", [1, 3, 5], index=2,
                          format_func=lambda x: f"최근 {x}년", key="sns_years")
    with c2:
        teams = ["전체 구단"] + sorted(df['team'].unique().tolist())
        tm = st.selectbox("구단 선택", teams, key="sns_team")

    st.markdown("---")

    # 데이터 필터링
    filt = sa.filter(yrs, tm)

    # 상관계수 계산
    stats = sa.calc_corr(filt)

    # 메트릭
    m1, m2, m3 = st.columns(3)
    p = stats['pearson']
    m1.metric("피어슨 상관계수", f"{p:.4f}" if p is not None else "–")
    s = stats['spearman']
    m2.metric("스피어만 상관계수", f"{s:.4f}" if s is not None else "–")
    m3.metric("샘플 수", f"{stats['size']}개")

    # 산점도
    st.markdown("### 📈 팔로워 vs 평균 관중수 산점도")
    fig_scatter = sa.scatter(filt, yrs)  # SocialAnalyzer.scatter 호출
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 연도별 트렌드
    if yrs > 1:
        if stats['size'] >= 2:
            st.markdown("### 📊 연도별 트렌드")
            fig_trend = sa.trend(filt, tm)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("연도별 트렌드를 보려면 최소 2개 이상의 데이터가 필요합니다.")
