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
            border: 1xp solid #3f51b5;
            color: white;
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
            background-color: #3f51b5;
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
        }
                
        div.st-key-btn-start button:hover,
        div.st-key-btn-start button:focus:not(:active),
        div.st-key-btn-reset button:hover,
        div.st-key-btn-reset button:focus:not(:active){
            border: 1px solid #1565c0;
            background-color: #1565c0;
            color: white;
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
            background-color: #1a1a1a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 24px;
            margin: 24px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
                
        div.item_box{
            border: 1px solid #555;
            background: #131720;
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
                
        div.shop_list{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
                
        div.shop_list a{
            display: inline-block;
            color: #ffffff;
            padding: 14px 20px;
            margin: 6px 0;
            border-radius: 6px;
            border: 1px solid #444;
            text-decoration: none;
            transition: background-color 0.2s, border-color 0.2s;    
        }
                
        div.shop_list a:hover {
            border-color: #777;
            color: #fff;
        }
                

        </style>
    """, unsafe_allow_html=True)