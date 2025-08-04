# main.py

import streamlit as st

from app.inspection.inspection_page import render_inspection_page  # type: ignore
from app.inspection.correlation_section import render_correlation_section
from app.schedule.schedule_view import render_schedule_view
from app.inspection.social_section import render_social_section

st.set_page_config(
    page_title="⚾ KBO 데이터 분석 대시보드",
    page_icon="⚾",
    layout="wide"
)

st.title("⚾ KBO 데이터 분석 대시보드")

tabs = st.tabs([
    "📊 승률-관중수 상관관계",
    "📱 SNS 팔로워 vs 관중수 분석",
    "📅 야구 경기 일정",
    "🧠 야구 직관 팬 성향 분석"
])

with tabs[0]:
    render_correlation_section()

with tabs[1]:
    render_social_section()

with tabs[2]:
    render_schedule_view()

with tabs[3]:
    # 세션 상태 초기화 for inspection
    if "inspection_page_idx" not in st.session_state:
        st.session_state.inspection_page_idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "inspection_start" not in st.session_state:
        st.session_state.inspection_start = False

    render_inspection_page()
