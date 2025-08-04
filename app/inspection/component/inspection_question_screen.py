
from pprint import pprint
import pandas as pd
import streamlit as st
import pydeck as pdk

from apis.weather_api import WeatherAPI
from features.inspection.inspection_result import InspectionResult # type: ignore
from app.inspection.constant.common import questions

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
    "pitcher": 0,
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
            content_html = "".join([f"<div class='content item_box'>{idx + 1}. {co}</div>" for idx, co in enumerate(pan_type["content"])])
            rest_html = "".join([
                f"<a href='{rest["url"]}' target='_blank'><div class='content'>{rest["place_name"]}</div></a>"
                for rest in recommend["famous_restaurants"]
            ])

            print("@ recomment")
            pprint(recommend["famous_restaurants"])
            reommend_team_info = recommend["team"]
            recomment_team_stadium = reommend_team_info["stadium"]
            recomment_team_latitude = reommend_team_info["latitude"]
            recomment_team_longitude = reommend_team_info["longitude"]

            html_inspection_personality = f"""
            <div class='result-card'>
                <div class='title'>{pan_type['name']}</div>
                <div class='keyword-box'>{keyword_html}</div>
                <div class='title'>당신의 팬 성향!</div>
                <div class='content-box'>{content_html}</div>
            </div>
            """

            # 유저 팬 성향 출력
            st.markdown(html_inspection_personality, unsafe_allow_html=True)

            # 1. 구장 정보
            map_items = [{
                "name": recomment_team_stadium,
                "lat": float(recomment_team_latitude),
                "lon": float(recomment_team_longitude),
                "type": "stadium"
            }]

            # 2. 맛집 정보 추가
            for rest in recommend["famous_restaurants"]:
                map_items.append({
                    "name": rest["place_name"],
                    "lat": float(rest["latitude"]),
                    "lon": float(rest["longitude"]),
                    "type": "restaurant"
                })

            # 3. DataFrame으로 변환
            map_df = pd.DataFrame(map_items)

            # 좌표 + 이름
            # recommend_df = pd.DataFrame([{
            #     "name": recomment_team_stadium,
            #     "lat": recomment_team_latitude,
            #     "lon": recomment_team_longitude
            # }])

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position='[lon, lat]',
                get_radius="""
                    type === 'stadium' ? 100 : 75
                """,
                get_fill_color="""
                    [
                        type === 'stadium' ? 255 : 0,
                        type === 'restaurant' ? 128 : 0,
                        0,
                        255
                    ]
                """,
                pickable=True,
            )

            tooltip = {"text": "{name}"}

            view_state = pdk.ViewState(
                latitude=float(recomment_team_latitude),
                longitude=float(recomment_team_longitude),
                zoom=13,
                pitch=0,
            )

            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=view_state,
                layers=[layer],
                tooltip=tooltip
            ))

            html_inspection_recommend = f"""
            <div class='result-card'>
                <div class='recommend_container item_box'>
                    <div class='recommend_box'>
                        <div class="recommend_box_title">구장 추천</div>
                        <div>{recomment_team_stadium}</div>
                    </div>
                    <div class='recommend_box'>
                        <div class="recommend_box_title">인근 맛집 추천</div>
                        <div class='shop_list'>
                            {rest_html}
                        </div>
                    </div>
                </div>
            </div>
            """

            st.markdown(html_inspection_recommend, unsafe_allow_html=True)

            # 다시 시작 버튼
            if st.button("다시 시작", key="btn-reset"):
                st.session_state.started = False
                st.session_state.inspection_page_idx = 0
                st.session_state.answers = []
                st.rerun()