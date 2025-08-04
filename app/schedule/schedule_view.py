def render_schedule_view():
    import streamlit as st
    import pandas as pd
    import os
    import glob
    from datetime import datetime
    from scraper.경기일정 import fetch_kbo_schedule

    st.subheader("📅 오늘의 KBO 경기 일정")

    today = datetime.today().strftime("%Y-%m-%d")
    data_dir = "./data"
    json_path = os.path.join(data_dir, f"kbo_schedule_{today}.json")

    def load_schedule(path):
        try:
            df = pd.read_json(path)
            return None if df.empty else df
        except:
            return None

    df = load_schedule(json_path) if os.path.exists(json_path) else None

    if df is None:
        json_files = sorted(
            glob.glob(os.path.join(data_dir, "kbo_schedule_*.json")),
            key=lambda x: os.path.basename(x).split("_")[-1].replace(".json", ""),
            reverse=True
        )
        for file in json_files:
            df = load_schedule(file)
            if df is not None:
                st.info(f"오늘 경기가 없어 가장 최신 일정({os.path.basename(file)})을 보여드립니다.")
                break

    if df is None:
        with st.spinner("경기 일정이 없어 데이터를 새로 불러오는 중입니다..."):
            df, _ = fetch_kbo_schedule(today, save_dir=data_dir)
        if df.empty:
            st.warning("오늘도, 최근에도 예정된 경기가 없습니다.")
            return

    # ✅ 오늘 날짜 기준으로 필터링
    today_str = datetime.today().strftime("%y-%m-%d")  # ex: '25-08-04'
    today_df = df[df["날짜"] == today_str]

    if today_df.empty:
        st.warning("오늘 예정된 경기가 없습니다. 전체 일정 중 가장 가까운 날짜의 경기를 표시합니다.")
         # 🔥 오늘 이후 날짜만 필터링
        future_df = df[df["날짜"] > today_str]

        if future_df.empty:
            st.error("앞으로 예정된 경기도 없습니다.")
            return

        # 오름차순 정렬 후 가장 가까운 미래 날짜 선택
        next_date = future_df.sort_values("날짜")["날짜"].iloc[0]
        today_df = df[df["날짜"] == next_date]
        st.info(f"가장 가까운 경기 일정: {next_date}")

    # ✅ UI
    grouped = today_df.groupby("날짜")

    for date, group in grouped:
        st.markdown(f"### 📌 {date}")
        for _, row in group.iterrows():
            st.markdown(f"""
            <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:8px 0; background-color:#f9f9f9">
                <b>⏰ {row['시간']}</b><br>
                <span style="font-size: 18px;">
                    🎒 <b>{row['원정팀']}</b> (원정) vs 🏟 <b>{row['홈팀']}</b> (홈)
                </span>
            </div>
            """, unsafe_allow_html=True)
