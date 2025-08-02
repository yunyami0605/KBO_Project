import streamlit as st


from app.inspection.inspection_start_screen import start_screen # type: ignore
from app.inspection.inspection_question_screen import questions_screen
from app.inspection.style import apply_inspection_styles # type: ignore

'''
    성격 유형 검사 탭 화면
'''
def render_inspection_section():
    apply_inspection_styles()

    if not st.session_state.inspection_start:
        start_screen()

    else:
        questions_screen()