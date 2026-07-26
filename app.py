import streamlit as st
import pandas as pd
from recommend import recommend

st.title("오늘 뭐 먹지?")

random_button = st.button("아무거나")
        
category = st.selectbox(

    "음식 종류",

    ["한식", "중식", "일식", "양식", "분식", "간식", "패스트푸드"]

)
        
st.write(category)

food = st.text_input("음식을 쓰세요")
st.write(food)

cost = st.text_input("최대 예산(인당)")
st.write(cost)

time = st.selectbox(

    "최대 소요 시간(분)",

    [5, 10, 15, 20]

)

if time != 0:
    st.write(time)
    
search_button = st.button("추천 받기")
    
        
st.divider()

st.header("⭐ 추천 음식점(5순위)")

result_area = st.container()


if random_button:
    restaurants = recommend("아무거나")
    
    with result_area:
        
        medals = ["🥇", "🥈", "🥉"]

        for i, restaurant in restaurants.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([1, 5])

                with col1:
                    if i < len(medals):
                        st.markdown(f"# {medals[i]}")
                    else:
                        st.markdown(f"# {i+1}")

                with col2:
                    st.subheader(restaurant["name"])
                    st.write(restaurant["category"])
                    st.write(f"도보 시간: {restaurant["walk_time"]}분")

                    if st.button("상세보기", key=i):
                        st.write("여기에 상세 정보 출력")
    
if search_button:
    category = category.strip()
    
    restaurants = recommend(category, time).head(5) # 상위 5개 음식점만 저장
    
    with result_area:

        medals = ["🥇", "🥈", "🥉"]

        for i, restaurant in restaurants.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([1, 5])

                with col1:
                    if i < len(medals):
                        st.markdown(f"# {medals[i]}")
                    else:
                        st.markdown(f"# {i+1}")

                with col2:
                    st.subheader(restaurant["name"])
                    st.write(restaurant["category"])
                    st.write(f"도보 시간: {restaurant["walk_time"]}분")

                    if st.button("상세보기", key=i):
                        st.write("여기에 상세 정보 출력")