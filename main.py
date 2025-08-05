# main.py (수정된 부분)

import streamlit as st
from app.inspection.inspection_page import render_inspection_page  # type: ignore
from app.inspection.correlation_section import render_correlation_section
from app.schedule.schedule_view import render_schedule_view
from app.inspection.social_section import render_social_section  # 새로운 SNS 분석 탭 임포트

st.set_page_config(
    page_title="KBO 데이터 분석",
    page_icon="⚾",
    layout="wide"
)

st.title("⚾ KBO 데이터 분석 대시보드")

# 탭 구성 (SNS 팔로워 분석 탭 추가)
tabs = st.tabs([
    "📊 승률-관중수 상관관계",
    "📱 SNS 팔로워 vs 관중수",  # 새로운 탭 추가
    "📅 야구 경기 일정",
    "🧠 야구 직관 팬 성향 분석"
])

# 첫 번째 탭: 승률-관중수 상관관계 분석
with tabs[0]:
    render_correlation_section()

# 두 번째 탭: SNS 팔로워 vs 관중수 분석 (새로 추가된 탭)
with tabs[1]:
    render_social_section()

# 세 번째 탭: 야구 경기 일정
with tabs[2]:
    render_schedule_view()

# 네 번째 탭: 야구 직관 팬 성향 분석
with tabs[3]:
    # 검사 페이지용 세션 상태 초기화
    if "inspection_page_idx" not in st.session_state:
        st.session_state.inspection_page_idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "inspection_start" not in st.session_state:
        st.session_state.inspection_start = False

    render_inspection_page()
