# app/social_section.py

import streamlit as st
from features.inspection.social_analyzer import SocialAnalyzer

def render_social_section():
    """SNS 팔로워 vs 관중수 및 구단나이 상관분석 탭 렌더링"""
    
    st.subheader("📱 SNS 팔로워 vs 경기 관중수 및 구단 나이 상관분석")
    st.markdown("---")

    # SocialAnalyzer 인스턴스 생성 및 데이터 로드
    sa = SocialAnalyzer()
    if sa.df.empty:
        st.error("SNS 데이터 파일을 불러올 수 없습니다. 'data/kbo_sns_followers.json' 파일을 확인하세요.")
        return
    
    # 기간 및 구단 선택 UI
    col1, col2 = st.columns([2, 2])
    with col1:
        years = st.selectbox(
            "분석 기간 선택", 
            options=[1, 3, 5], 
            index=2, 
            format_func=lambda x: f"최근 {x}년", 
            key='social_years'
        )
    with col2:
        teams = ['전체 구단'] + sorted(sa.df['구단'].unique())
        team = st.selectbox("분석 팀 선택", teams, key='social_team')
    
    st.markdown("---")
    
    # 선택된 기간과 구단으로 데이터 필터링
    filtered = sa.filter(years, team)
    # 상관관계 계산
    corr_results = sa.calc_corr(filtered)

    # 상관계수 메트릭 표시 (4개로 확장)
    col1, col2, col3, col4 = st.columns(4)
    
    followers_pearson = corr_results['followers_attendance_pearson']
    followers_spearman = corr_results['followers_attendance_spearman']
    age_pearson = corr_results['age_attendance_pearson']
    age_spearman = corr_results['age_attendance_spearman']
    
    col1.metric(
        "팔로워-관중수 피어슨", 
        f"{followers_pearson:.4f}" if followers_pearson is not None else "–"
    )
    col2.metric(
        "팔로워-관중수 스피어만", 
        f"{followers_spearman:.4f}" if followers_spearman is not None else "–"
    )
    col3.metric(
        "구단나이-관중수 피어슨",
        f"{age_pearson:.4f}" if age_pearson is not None else "–"
    )
    col4.metric("분석 샘플 수", f"{corr_results['size']}개")

    # SNS 팔로워 vs 관중수 산점도
    st.markdown("### 📈 SNS 팔로워 vs 총관중수 산점도")
    scatter_fig1 = sa.scatter_followers_attendance(filtered, years)
    st.plotly_chart(scatter_fig1, use_container_width=True)

    # 구단나이 vs 관중수 산점도 추가
    st.markdown("### 📊 구단 나이 vs 총관중수 산점도")
    scatter_fig2 = sa.scatter_age_attendance(filtered, years)
    st.plotly_chart(scatter_fig2, use_container_width=True)

    # 연도별 트렌드 그래프 (분석 기간이 1년 초과하고 충분한 데이터가 있을 때)
    if years > 1:
        if corr_results['size'] > 1:
            st.markdown("### 📈 연도별 SNS 팔로워 & 관중수 트렌드")
            trend_fig = sa.trend_followers_attendance(filtered, team)
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.info("📊 연도별 트렌드 분석을 위해서는 최소 2개 이상의 데이터가 필요합니다.")

    # 분석 결과 해석 (추가 제안 없이 해석만)
    with st.expander("🔍 분석 결과 해석"):
        st.markdown("""
        **SNS 팔로워 vs 관중수 관계:**
        - 양의 상관관계가 나타날 경우: SNS 마케팅이 실제 관중 동원에 효과적임을 의미합니다.
        - 상관계수가 0.3 이상이면 중간 정도의 관계, 0.7 이상이면 강한 관계로 해석됩니다.
        - 피어슨 상관계수는 선형 관계를, 스피어만 상관계수는 순위 관계를 나타냅니다.
        
        **구단 나이 vs 관중수 관계:**
        - 양의 상관관계: 오래된 구단일수록 안정적이고 충성도 높은 팬층을 보유하고 있음을 의미합니다.
        - 음의 상관관계: 새로운 구단이 더 활발한 마케팅과 참신함으로 관중을 끌어모으고 있음을 의미합니다.
        - 상관관계가 약할 경우: 구단의 역사보다는 현재 성과나 다른 요인이 관중수에 더 큰 영향을 미침을 의미합니다.
        
        **해석 시 주의사항:**
        - 상관관계는 인과관계를 의미하지 않습니다.
        - 외부 요인(경기력, 스타 선수, 경제 상황 등)도 함께 고려해야 합니다.
        """)
