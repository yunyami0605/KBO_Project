import streamlit as st
import plotly.graph_objects as go
from features.inspection.correlation_analyzer import CorrelationAnalyzer

def render_correlation_section():
    """승률-관중수 상관관계 분석 섹션 렌더링"""
    
    st.subheader(" KBO 승률 vs 관중수 상관관계 분석")
    st.markdown("---")
    
    # 분석기 초기화
    analyzer = CorrelationAnalyzer()
    
    if analyzer.df is None:
        st.error(" 데이터를 불러올 수 없습니다. 데이터 파일을 확인해주세요.")
        return
    
    # 사이드바에서 년수 선택
    st.sidebar.markdown("### 📊 분석 설정")
    selected_years = st.sidebar.selectbox(
        "분석할 기간을 선택하세요:",
        options=[1, 3, 5],
        index=2,  # 기본값: 5년
        format_func=lambda x: f"최근 {x}년"
    )
    
    # 분석 실행
    with st.spinner(f"최근 {selected_years}년 데이터 분석 중..."):
        result = analyzer.analyze_correlation_by_years(selected_years)
    
    if 'error' in result:
        st.error(result['error'])
        return
    
    # 결과 표시
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 상관관계 분석 결과 ({selected_years}년간)")
        
        # 상관계수 표시
        stats = result['correlation_stats']
        
        # 메트릭 표시
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                label="피어슨 상관계수",
                value=f"{stats['pearson_correlation']:.4f}",
                help="선형 관계의 강도 (-1 ~ 1)"
            )
        
        with metric_col2:
            st.metric(
                label="상관관계 강도",
                value=stats['pearson_interpretation'],
                help="상관계수 절댓값 기준 해석"
            )
        
        with metric_col3:
            st.metric(
                label="분석 샘플 수",
                value=f"{stats['sample_size']}개",
                help="분석에 사용된 데이터 개수"
            )
        
        # 통계적 유의성 표시
        if stats['pearson_p_value'] < 0.05:
            st.success(f" 통계적으로 유의함 (p-value: {stats['pearson_p_value']:.4f})")
        else:
            st.warning(f" 통계적으로 유의하지 않음 (p-value: {stats['pearson_p_value']:.4f})")

    with col2:
        st.markdown("###  분석 정보")
        st.markdown(f"**분석 기간:** {min(stats['years_analyzed'])} - {max(stats['years_analyzed'])}")
        st.markdown(f"**포함된 연도:** {', '.join(map(str, stats['years_analyzed']))}")
        st.markdown(f"**스피어만 상관계수:** {stats['spearman_correlation']:.4f}")
    
    # 산점도 그래프
    st.markdown("### 📈 승률 vs 평균관중수 산점도")
    if 'scatter_plot' in result:
        st.plotly_chart(result['scatter_plot'], use_container_width=True)
    
    # 연도별 트렌드 그래프
    if selected_years > 1 and 'trend_plot' in result:
        st.markdown("### 📊 연도별 트렌드 분석")
        st.plotly_chart(result['trend_plot'], use_container_width=True)
    
    # 팀별 순위 표
    st.markdown("###  팀별 승률 및 관중수 순위")
    if 'team_ranking' in result and not result['team_ranking'].empty:
        
        # 표 스타일링
        styled_df = result['team_ranking'].style.format({
            '평균_승률': '{:.3f}',
            '승률_표준편차': '{:.3f}',
            '평균_관중수': '{:,.0f}',
            '관중수_표준편차': '{:,.0f}'
        }).background_gradient(subset=['평균_승률'], cmap='RdYlGn')
        
        st.dataframe(styled_df, use_container_width=True)
    
    # 인사이트 및 해석
    st.markdown("###  분석 인사이트")
    
    # 상관관계 해석
    corr_value = stats['pearson_correlation']
    
    if abs(corr_value) >= 0.3:
        if corr_value > 0:
            st.success(" **양의 상관관계**: 승률이 높을수록 관중수도 증가하는 경향이 있습니다.")
        else:
            st.warning(" **음의 상관관계**: 승률이 높을수록 관중수가 감소하는 경향이 있습니다.")
    else:
        st.info(" **약한 상관관계**: 승률과 관중수 사이에 뚜렷한 선형 관계가 없습니다.")
    
    # 추가 분석 제안
    with st.expander(" 추가 분석 제안"):
        st.markdown("""
        **더 깊이 있는 분석을 위한 제안:**
        
        1. **구장별 분석**: 각 구장의 특성(면적, 위치)이 관중수에 미치는 영향
        2. **시계열 분석**: 코로나19 등 외부 요인이 관중수에 미친 영향
        3. **팀별 세분화**: 인기팀 vs 비인기팀의 승률-관중수 관계 차이
        4. **월별/요일별 분석**: 시기별 관중수 패턴 분석
        5. **경기 결과별**: 홈/원정 경기별 관중수 차이 분석
        """)
    
    # 데이터 다운로드 옵션
    if st.button(" 분석 데이터 다운로드"):
        csv_data = result['filtered_data'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv_data,
            file_name=f"kbo_correlation_analysis_{selected_years}years.csv",
            mime="text/csv"
        )
