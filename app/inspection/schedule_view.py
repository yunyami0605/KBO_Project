# 경기일정.py

def render_schedule_view():
    import streamlit as st
    import pandas as pd
    import os
    from datetime import datetime
    from scraper.kbo_schedule_scraper import scrape_kbo_schedule

    st.subheader("📅 오늘의 KBO 경기 일정")

    today = datetime.today().strftime("%Y-%m-%d")
    data_dir = "./data"
    json_path = os.path.join(data_dir, f"kbo_schedule_{today}.json")

    if not os.path.exists(json_path):
        with st.spinner("오늘의 경기 일정을 가져오는 중..."):
            df, path = scrape_kbo_schedule(today, save_dir=data_dir)
            st.success("경기 일정 로딩 완료!")
    else:
        df = pd.read_json(json_path)

    st.dataframe(df)

# 이렇게 하면 streamlit run으로 실행할 경우에는 작동안 하고, 모듈로만 쓰임
if __name__ == "__main__":
    render_schedule_view()
