import streamlit as st

from app.inspection.correlation_section import render_correlation_section
from app.inspection.inspection_page import render_inspection_page  # type: ignore
from app.schedule.schedule_view import render_schedule_view

st.set_page_config(
    page_title="KBO 데이터 분석",
    page_icon="⚾",
    layout="wide"
)

st.title("⚾ KBO 데이터 분석 대시보드")

tabs = st.tabs(["🧠 야구 직관 팬 성향 분석", "📊 승률-관중수 상관관계", "🏟️ 구장 정보"])

with tabs[0]:
    # 세션 상태 초기화
    if "inspection_page_idx" not in st.session_state:
        st.session_state.inspection_page_idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "inspection_start" not in st.session_state:
        st.session_state.inspection_start = False

    render_inspection_page()

with tabs[1]:
    render_correlation_section()

with tabs[2]:
    render_schedule_view()


    st.subheader("🏟️ 구장 정보")
    st.info("구장 면적 분석 및 기타 정보가 여기에 표시됩니다.")
    st.line_chart([100, 200, 300])
