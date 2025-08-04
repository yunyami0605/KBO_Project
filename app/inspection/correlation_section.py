# app/correlation_section.py

import streamlit as st
import plotly.graph_objects as go
from features.inspection.correlation_analyzer import CorrelationAnalyzer

def render_correlation_section():
    """승률-관중수 상관관계 분석 섹션 렌더링"""

    st.subheader("📊 KBO 승률 vs 평균 관중수 상관관계 분석")
    st.markdown("---")

    # 1) 데이터 로드
    analyzer = CorrelationAnalyzer()
    df = analyzer.df
    if df is None or df.empty:
        st.error("데이터를 불러올 수 없습니다. 'data/kbo_merged_crowd_winrate.json' 파일을 확인하세요.")
        return

    # 2) 분석 설정: 기간 선택 + 구단 선택
    col_year, col_team = st.columns([2, 2])
    with col_year:
        selected_years = st.selectbox(
            "분석할 기간",
            options=[1, 3, 5],
            index=2,
            format_func=lambda x: f"최근 {x}년",
            key="corr_years"
        )
    with col_team:
        teams = ["전체 구단"] + sorted(df['team'].unique().tolist())
        selected_team = st.selectbox(
            "구단 선택",
            options=teams,
            key="corr_team"
        )

    st.markdown("---")

    # 3) 데이터 필터링: 기간 → 구단
    filtered_df = analyzer.filter_data_by_years(selected_years)
    if selected_team != "전체 구단":
        filtered_df = filtered_df[filtered_df['team'] == selected_team]

    # 4) 상관관계 통계 계산
    stats = analyzer.calculate_correlation(filtered_df)

    # 5) 상단 메트릭 표시
    m1, m2, m3 = st.columns(3)
    pearson_val = stats.get('pearson_correlation')
    if pearson_val is not None:
        m1.metric("피어슨 상관계수", f"{pearson_val:.4f}")
    else:
        m1.metric("피어슨 상관계수", "–")

    m2.metric("상관관계 강도", stats.get('pearson_interpretation', "-"))
    m3.metric("분석 샘플 수", f"{stats.get('sample_size', 0)}개")

    # 6) 통계 유의성 표시
    p_value = stats.get('pearson_p_value')
    if p_value is not None:
        if p_value < 0.05:
            st.success(f"✅ 통계적으로 유의함 (p-value: {p_value:.4f})")
        else:
            st.warning(f"⚠️ 통계적으로 유의하지 않음 (p-value: {p_value:.4f})")
    else:
        st.info("⚠️ 상관관계 계산을 위해서는 최소 2개 이상의 데이터가 필요합니다.")

    # 7) 분석 정보
    st.markdown("### 📋 분석 정보")
    years_list = stats.get('years_analyzed', [])
    if years_list:
        st.markdown(f"**분석 기간:** {min(years_list)} - {max(years_list)}")
        st.markdown(f"**포함된 연도:** {', '.join(map(str, years_list))}")
    spearman_val = stats.get('spearman_correlation')
    if spearman_val is not None:
        spearman_str = f"{spearman_val:.4f}"
    else:
        spearman_str = "–"
    st.markdown(f"**스피어만 상관계수:** {spearman_str}")

    # 8) 산점도 시각화
    st.markdown("### 📈 승률 vs 평균관중수 산점도")
    scatter_fig = analyzer.create_scatter_plot(filtered_df, selected_years)
    st.plotly_chart(scatter_fig, use_container_width=True)

    # 9) 연도별 트렌드 그래프 (기간 >1, 최소 2개 데이터)
    if selected_years > 1:
        if stats.get('sample_size', 0) >= 2:
            st.markdown("### 📊 연도별 승률 & 관중수 트렌드")
            trend_df = filtered_df.copy()
            if selected_team == "전체 구단":
                trend_df = (
                    trend_df.groupby('year')
                    .agg({'win_rate':'mean','avg_spectators':'mean'})
                    .reset_index()
                    .assign(team="전체 구단")
                )
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend_df['year'], y=trend_df['win_rate'],
                name=f"{selected_team} 평균 승률",
                line=dict(color='blue', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=trend_df['year'], y=trend_df['avg_spectators'],
                name=f"{selected_team} 평균 관중수",
                line=dict(color='orange', width=3),
                yaxis='y2'
            ))
            fig.update_layout(
                title=f"{selected_team} 연도별 승률 & 관중수 트렌드",
                xaxis=dict(title='연도'),
                yaxis=dict(title='평균 승률', side='left', color='blue'),
                yaxis2=dict(
                    title='평균 관중수', side='right',
                    overlaying='y', color='orange'
                ),
                width=800, height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 연도별 트렌드 분석을 위해서는 최소 2개 이상의 데이터가 필요합니다.")

    # 10) 팀별 순위 표
    st.markdown("### 🏆 팀별 승률 및 관중수 순위")
    ranking_df = analyzer.get_team_ranking_by_correlation(filtered_df)
    if not ranking_df.empty:
        styled = ranking_df.style.format({
            '평균_승률': '{:.3f}',
            '승률_표준편차': '{:.3f}',
            '평균_관중수': '{:,.0f}',
            '관중수_표준편차': '{:,.0f}'
        }).background_gradient(subset=['평균_승률'], cmap='RdYlGn')
        st.dataframe(styled, use_container_width=True)

    # 11) 분석 인사이트
    st.markdown("### 🔍 분석 인사이트")
    corr_val = stats.get('pearson_correlation')
    if corr_val is not None and abs(corr_val) >= 0.3:
        if corr_val > 0:
            st.success("양의 상관관계: 승률이 높을수록 관중수도 증가하는 경향이 있습니다.")
        else:
            st.warning("음의 상관관계: 승률이 높을수록 관중수가 감소하는 경향이 있습니다.")
    elif corr_val is not None:
        st.info("약한 상관관계: 승률과 관중수 사이에 뚜렷한 선형 관계가 없습니다.")
    else:
        st.info("분석 인사이트를 위해서는 최소 2개 이상의 데이터가 필요합니다.")

    # 12) 추가 분석 제안
    with st.expander("💡 추가 분석 제안"):
        st.markdown("""
        **더 깊이 있는 분석을 위한 제안:**
        
        1. **구장별 분석**: 각 구장의 특성(면적, 위치)이 관중수에 미치는 영향  
        2. **시계열 분석**: 코로나19 등 외부 요인이 관중수에 미친 영향  
        3. **팀별 세분화**: 인기팀 vs 비인기팀의 승률-관중수 관계 차이  
        4. **월별/요일별 분석**: 시기별 관중수 패턴 분석  
        5. **경기 결과별**: 홈/원정 경기별 관중수 차이 분석  
        """)

    # 13) 데이터 다운로드
    if st.button("📥 분석 데이터 다운로드"):
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv,
            file_name=f"kbo_corr_{selected_team}_{selected_years}years.csv",
            mime="text/csv"
        )
