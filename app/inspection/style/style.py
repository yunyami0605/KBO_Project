import streamlit as st

# 팬 유형 스타일 코드
def apply_inspection_styles():
    st.markdown("""
        <style>
        /* 기본 버튼 */
        .stButton {
            margin: 6px 0;
        }        
        .stButton > button {
            width: 400px;
            border: 1px solid #ccc;
            color: black;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
        }
                
        /* 시작 버튼 */
        div.st-key-btn-start {
            padding: 24px 0;        
        }
                
        div.st-key-btn-start button, div.st-key-btn-reset button {
            width: 400px;
            background-color: transparent;
            border: 1px solid #6732D5;
            color: #6732D5;
        }
                
        .stButton > button:hover,
        .stButton > button:focus:not(:active),
        .stButton > button:hover,
        .stButton > button:focus:not(:active){
            border: 2px solid #6732D5;
            background: transparent;
            color: #6732D5;
            transform: scale(1.02);
        }

        /* 제목 섹션 */
        div.stHeading{
            margin-bottom: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
                
        /* 이미지 섹션 */        
        div.stElementContainer > div{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
                
        div.stVerticalBlock{
            width: 100%;
            
        }

        /* 두 번째 버튼 (빨간색) */
        div.st-key-btn-red button {
            background-color: #e53935;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
        }

        .stMarkdown > div{
            width: 100%;
        }

        /* 결과 카드 */
        .result-card {
            background-color: transparent;
            border: 1px solid #aaa;
            border-radius: 12px;
            padding: 24px;
            margin: 24px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
                
        div.item_box{
            border: 1px solid #555;
            background: transparent;
            border-radius: 6px;
        }


        /* 결과 키워드 구간 */
        div.keyword-box {
            margin-bottom: 32px;
            gap: 18px;
            display: flex;        
        }
                
        div.keyword-box div.keyword{
            padding: 8px 14px;
            background: transparent;
        }
                
        /* 성향 내용 구간 */
        div.content-box {
            margin-bottom: 24px;
            gap: 18px;
            display: flex;
            flex-direction: column;    
        }
                
        div.content-box div.content{
            padding: 8px 14px;
        }
                
        div.title{
            font-size: 20px;
            margin-bottom:14px;
        }
                
        div.recommend_container{
            padding: 30px;
            display: flex;
        }
                
        div.recommend_box{
            flex: 1;
            gap: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
                
        div.recommend_box_title{
            font-size: 20px;
            font-weight: bold;
            color: #222;
        }
                
        div.shop_list{
            display: flex;
            gap: 12px;
        }
                
        div.shop_list a{
            display: inline-block;
            color: black;
            padding: 14px 20px;
            margin: 6px 0;
            border-radius: 6px;
            border: 1px solid #6732D5;
            color: #6732D5;
            text-decoration: none;
            transition: background-color 0.2s, border-color 0.2s;    
        }
                
        div.shop_list a:hover {
            border: 2px solid #6732D5;
            transform: scale(1.02);
            cursor: pointer;
            color: black;
        }
                

        </style>
    """, unsafe_allow_html=True)