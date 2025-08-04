import streamlit as st



def start_screen():
    st.subheader("야구 직관 팬 성향 분석")
    st.image("https://storage2.ilyo.co.kr/contents/article/images/2024/0322/1711090517318430.jpg", width=400)

    if st.button("테스트 시작", key="btn-start"):
        st.session_state.inspection_start = True
        st.rerun()
