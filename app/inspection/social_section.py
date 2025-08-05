# app/social_section.py

import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from io import BytesIO
from features.inspection.social_analyzer import SocialAnalyzer

def render_social_section():
    """SNS 팔로워 vs 관중수 및 구단나이 상관분석 + 다중회귀"""

    st.subheader("📱 SNS 팔로워 vs 경기 관중수 및 구단나이 상관분석")
    st.markdown("---")

    sa = SocialAnalyzer()
    df = sa.df
    if df.empty:
        st.error("데이터를 불러올 수 없습니다.")
        return

    # 기간 선택
    years = st.selectbox("분석 기간 선택", [1,3,5], index=2, format_func=lambda x: f"최근 {x}년")
    latest = df['연도'].max()
    df_period = df[df['연도'] >= latest - years + 1]

    # 상관분석
    corr = sa.calc_corr(df_period)
    pr = corr.get('followers_attendance_pearson')
    pp = corr.get('followers_attendance_pval')
    ar = corr.get('age_attendance_pearson')
    ap = corr.get('age_attendance_pval')
    size = corr.get('size',0)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("팔로워-관중 r", f"{pr:.4f}" if pr is not None else "–")
    c2.metric("팔로워 p-value", f"{pp:.4f}" if pp is not None else "–")
    c3.metric("구단나이 r", f"{ar:.4f}" if ar is not None else "–")
    c4.metric("샘플 수", f"{size}개")

    # 산점도 & 트렌드
    st.markdown("### 📈 산점도")
    st.plotly_chart(sa.scatter_followers_attendance(df_period, years), use_container_width=True)
    st.plotly_chart(sa.scatter_age_attendance(df_period, years), use_container_width=True)
    if years>1 and size>1:
        st.markdown("### 📊 연도별 트렌드")
        st.plotly_chart(sa.trend_followers_attendance(df_period), use_container_width=True)

    # 다중회귀분석
    st.markdown("### 🏷️ 팀별 다중회귀계수 비교")
    vars = ['win_rate','rank','SNS팔로워수','구단나이']
    # 필터링: 독립변수 모두 존재하는 행
    df_reg = df_period.dropna(subset=vars + ['총관중수'])
    teams = df_reg['구단'].unique()
    results = {}
    for team in teams:
        sub = df_reg[df_reg['구단']==team]
        if len(sub) < len(vars)+1:
            continue
        X = sm.add_constant(sub[vars])
        y = sub['총관중수']
        model = sm.OLS(y, X).fit()
        results[team] = model.params

    coef_df = pd.DataFrame(results).T

    if not coef_df.empty:
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False

        for var in vars:
            if var not in coef_df:
                continue
            fig, ax = plt.subplots(figsize=(10,4))
            coef_df[var].sort_values().plot.bar(ax=ax, color='skyblue')
            ax.axhline(0, color='black', linewidth=0.8)
            ax.set_title(f"{var} 계수", fontsize=14)
            ax.set_ylabel("회귀계수")
            ax.set_xlabel("구단")
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

        # 다운로드
        csv = coef_df.to_csv(index=True, encoding='utf-8-sig').encode('utf-8-sig')
        interp = (
            f"다중회귀 R²: {model.rsquared:.3f}\n" +
            "\n".join([f"{v} 계수={model.params[v]:.3f} (p={model.pvalues[v]:.3f})" 
                       for v in vars if v in model.params])
        )
        colA, colB = st.columns(2)
        with colA:
            st.download_button("CSV 다운로드", csv, "multi_reg_coeff.csv", "text/csv")
        with colB:
            st.download_button("해설 다운로드", interp, "multi_reg_summary.txt", "text/plain")
    else:
        st.info("회귀분석에 충분한 데이터가 없습니다 (각 팀 최소 변수개수+1개 필요).")

    # 해설
    st.markdown("### 🔍 분석 해설")
    st.write(f"- 기간: 최근 {years}년, 샘플 수: {size}개")
    if pr is not None:
        strength = "강한" if abs(pr)>=0.7 else "중간" if abs(pr)>=0.3 else "약한"
        dirc = "양의" if pr>0 else "음의"
        st.write(f"- 팔로워 vs 관중수: {strength} {dirc} 상관관계 (r={pr:.4f}, p={pp:.4f})")
    if ar is not None:
        strength2 = "강한" if abs(ar)>=0.7 else "중간" if abs(ar)>=0.3 else "약한"
        dir2 = "양의" if ar>0 else "음의"
        st.write(f"- 구단나이 vs 관중수: {strength2} {dir2} 상관관계 (r={ar:.4f}, p={ap:.4f})")
