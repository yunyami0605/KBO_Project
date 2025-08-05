# app/social_section.py

import streamlit as st
from features.inspection.social_analyzer import SocialAnalyzer
from scipy.stats import pearsonr, spearmanr

def render_social_section():
    """SNS 팔로워 vs 경기 관중수·구단 나이 상관분석 탭"""

    st.subheader("📱 SNS 팔로워 vs 경기 관중수·구단 나이 상관분석")
    st.markdown("---")

    sa = SocialAnalyzer()
    df = sa.df
    if df.empty:
        st.error("데이터를 불러올 수 없습니다. 'data/kbo_sns_followers.json' 확인하세요.")
        return

    # 분석 기간 선택
    years = st.selectbox("분석 기간 선택", [1,3,5], index=2,
                         format_func=lambda x: f"최근 {x}년")
    st.markdown("---")

    # 기간 필터링
    latest = df['연도'].max()
    df_period = df[df['연도'] >= latest - years + 1]

    # 통계 계산
    stats = sa.compute_stats(df_period)
    pr = stats['pearson_r']; pp = stats['pearson_p']
    sr = stats['spearman_rho']; sp = stats['spearman_p']
    n = stats['sample_size']

    # 메트릭
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pearson r", f"{pr:.3f}" if pr is not None else "–")
    c2.metric("p-value", f"{pp:.3f}" if pp is not None else "–")
    c3.metric("Spearman ρ", f"{sr:.3f}" if sr is not None else "–")
    c4.metric("샘플 수", f"{n}개")

    # 유의성 알림
    if pp is not None:
        if pp < 0.05:
            st.success("✅ 통계적으로 유의함 (p < 0.05)")
        else:
            st.warning("⚠ 통계적으로 유의하지 않음 (p ≥ 0.05)")

    # 산점도
    st.markdown("### 📈 SNS 팔로워 vs 총 관중수 산점도")
    st.plotly_chart(sa.scatter_followers_vs_attendance(df_period), use_container_width=True)

    st.markdown("### 🎂 구단 나이 vs 총 관중수 산점도")
    st.plotly_chart(sa.scatter_age_vs_attendance(df_period), use_container_width=True)

    # 추가 시각화
    st.markdown("### 📊 SNS 팔로워 수 분포")
    st.plotly_chart(sa.histogram_followers(df_period), use_container_width=True)

    st.markdown("### 📋 구단 나이별 관중수 분포")
    st.plotly_chart(sa.boxplot_age_vs_attendance(df_period), use_container_width=True)

    # 분석 해설
    st.markdown("### 🔍 분석 해설")
    if pr is not None:
        strength = "강한" if abs(pr)>=0.7 else "중간" if abs(pr)>=0.3 else "약한"
        direction = "양의" if pr>0 else "음의"
        st.write(f"- **상관계수(r={pr:.3f})**: {strength} {direction} 상관관계")
        st.write(f"- **p-value**: {pp:.3f} ({'유의함' if pp<0.05 else '유의하지 않음'})")
    else:
        st.write("- 데이터 부족: 상관관계 계산 불가")

    # 다운로드
    if st.button("📥 데이터 및 해설 다운로드"):
        csv = df_period.to_csv(index=False, encoding='utf-8-sig')
        interp = f"r={pr:.3f}, p={pp:.3f}" if pr is not None else "데이터 부족"
        colA, colB = st.columns(2)
        with colA:
            st.download_button("CSV 다운로드", csv, f"sns_{years}y.csv", "text/csv")
        with colB:
            st.download_button("해설 다운로드", interp, f"sns_{years}y.txt", "text/plain")
