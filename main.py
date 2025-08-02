import streamlit as st

from app.inspection.inspection_section import render_inspection_section  # type: ignore

st.title("KBO 데이터 분석")

tabs = st.tabs(["야구 직관 팬 성향 분석", "구장 정보"])

with tabs[0]:
    # 세션 상태 초기화
    if "inspection_page_idx" not in st.session_state:
        st.session_state.inspection_page_idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "inspection_start" not in st.session_state:
        st.session_state.inspection_start = False

    render_inspection_section()

with tabs[1]:
    st.subheader("관중수 분석")
    st.line_chart([100, 200, 300])

