def render_schedule_view():
    import streamlit as st
    import pandas as pd
    import os
    from datetime import datetime

    st.subheader("📅 오늘의 KBO 경기 일정")

    today = datetime.today().strftime("%Y-%m-%d")  # 예: '2025-08-04'
    today_short = datetime.today().strftime("%y-%m-%d")  # 예: '25-08-04'
    data_dir = "./data/inspection"
    json_path = os.path.join(data_dir, f"kbo_schedule.json")

    def load_schedule(path):
        try:
            df = pd.read_json(path)
            return None if df.empty else df
        except:
            return None

    if not os.path.exists(json_path):
        st.error(f"{json_path} 파일이 존재하지 않습니다. 데이터를 미리 저장해 주세요.")
        return

    df = load_schedule(json_path)
    if df is None:
        st.error(f"{json_path} 파일이 비어 있거나 로드에 실패했습니다.")
        return

    # ✅ 오늘 날짜 기준 필터링
    today_df = df[df["날짜"] == today_short]

    if today_df.empty:
        st.warning("오늘 예정된 경기가 없습니다. 해당 파일 내에서 가장 가까운 미래 경기 일정을 표시합니다.")

        # 저장된 JSON 안에서 오늘 이후 경기를 찾음
        future_df = df[df["날짜"] > today_short]

        if future_df.empty:
            st.error("파일 내에도 예정된 경기가 없습니다.")
            return

        # 가장 가까운 경기일 선택
        next_date = future_df.sort_values("날짜")["날짜"].iloc[0]
        today_df = df[df["날짜"] == next_date]
        st.info(f"가장 가까운 경기 일정: {next_date}")

    # ✅ UI
    grouped = today_df.groupby("날짜")

    for date, group in grouped:
        st.markdown(f"### 📌 {date}")
        for _, row in group.iterrows():
            st.markdown(f"""
            <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:8px 0;">
                <b>⏰ {row['시간']}</b><br>
                <span style="font-size: 18px;">
                    🎒 <b>{row['원정팀']}</b> (원정) vs 🏟 <b>{row['홈팀']}</b> (홈)
                </span>
            </div>
            """, unsafe_allow_html=True)
