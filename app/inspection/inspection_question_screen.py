
import streamlit as st

from apis.weather_api import WeatherAPI
from features.inspection.inspection_result import InspectionResult # type: ignore
from app.inspection.constant import questions
# 야구팬 성향 수치
result = {
    "comfortable": 0, # 편안파 (쾌적함 & 먹거리 중시형)
    "profit": 0, # 실속파 (시설 & 경기력 중시형)
    "passion": 0, # 열정파 (응원 & 열정 중시형)
    "better": 0, # 실용파 (편리 & 실용 중시형)
    "sunny": 0,
    "rainy": 0,
    "cold": 0,
    "defense": 0,
    "runner": 0,
    "hitter": 0,
    "picher": 0,
}


def questions_screen():
    inspection_page_idx = st.session_state.inspection_page_idx

    if inspection_page_idx < len(questions):
        question = questions[inspection_page_idx]

        title = question["title"]

        st.subheader(title)

        # 선택지 버튼 렌더링
        for idx, option in enumerate(question["options"]):
            if st.button(option["text"], key=f"q{inspection_page_idx}_{title}_{idx}"):

                result = option["value"]

                st.session_state.answers.extend(result)
                st.session_state.inspection_page_idx += 1
                st.rerun()  # 다음 질문으로 넘어감

    else:
        with st.spinner("로딩 중입니다..."):
            # 테스트 완료 화면
            analyzer = InspectionResult(weather_api=WeatherAPI())

            answer = st.session_state.answers
            pan_type = analyzer.get_personality_result(answer) # 팬유형
            recommend = analyzer.get_recommend_stadium(answer) # 추천

            st.subheader("당신의 팬 유형")

            keyword_html = "".join([f"<div class='keyword item_box'># {kw}</div>" for kw in pan_type["keyword"]])
            content_html = "".join([f"<div class='content item_box'>{co}</div>" for co in pan_type["content"]])
            rest_html = "".join([
                f"<a href='{rest["url"]}' target='_blank'><div class='content'>{rest["place_name"]}</div></a>"
                for rest in recommend["famous_restaurants"]
            ])

            html = f"""
            <div class='result-card'>
                <div class='title'>{pan_type['name']}</div>
                <div class='keyword-box'>{keyword_html}</div>
                <div class='title'>당신의 팬 성향!</div>
                <div class='content-box'>{content_html}</div>
                <div class='recommend_container item_box'>
                    <div class='recommend_box'>
                        <div>구장 추천</div>
                        <div>{recommend["team"]}</div>
                    </div>
                    <div class='recommend_box'>
                        <div>인근 맛집 추천</div>
                        <div class='shop_list'>
                            {rest_html}
                        </div>
                    </div>
                </div>
            </div>
            """

            # 출력
            st.markdown(html, unsafe_allow_html=True)

            # 다시 시작 버튼
            if st.button("다시 시작", key="btn-reset"):
                st.session_state.started = False
                st.session_state.inspection_page_idx = 0
                st.session_state.answers = []
                st.rerun()