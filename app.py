import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
from recommend import recommend # recommend 파일에서 recommend 함수를 가져 옴.
import folium
from streamlit_folium import st_folium

# 지도 높이를 화면 크기에 맞게 조절하는 반응형 CSS
st.markdown("""
<style>
/* st_folium이 생성하는 iframe을 반응형으로 만들기 */
iframe[title="streamlit_folium.st_folium"] {
    width: 100% !important;
    height: clamp(250px, 56vw, 500px) !important;
    min-height: 250px;
    max-height: 500px;
}
</style>
""", unsafe_allow_html=True)

try:    # 배포를 위한 로직, 추천 음식점 위치를 띄움.
    KAKAO_JS_KEY = st.secrets["KAKAO_JS_KEY"]

except Exception:   # secrets 변수에 있는 API KEY 이용
    load_dotenv()
    KAKAO_JS_KEY = os.getenv("KAKAO_JS_KEY")

# session_state 초기화
if "restaurants" not in st.session_state:
    st.session_state.restaurants = None

st.title("오늘 뭐 먹지?")

random_button = st.button("아무거나")

position = st.selectbox(
    "지금 위치에서 가장 가까운 곳",
    ["정문", "후문", "한울관", "누리관", "광운대역"]
)
st.write(position)

category = st.selectbox(
    "음식 종류",
    ["한식", "중식", "일식", "양식", "분식", "카페", "간식", "패스트푸드"]
)
st.write(category)

time = st.selectbox(
    "최대 소요 시간(분)",
    [2, 4, 6, 8, 10]
)
st.write(time)
    
cost = st.selectbox(
    "최대 예산(인당)",
    [5000, 8000, 12000, 15000, 20000]
)
st.write(cost)
    
search_button = st.button("추천 받기")
        
st.divider()

st.header("⭐ 추천 음식점(5순위)")

result_area = st.container()

st.subheader("📍 추천 음식점 위치")

result_map_area = st.container()

# 버튼 클릭 시 session_state에 결과 저장
if random_button:
    st.session_state.restaurants = recommend("아무거나")

if search_button:
    result = recommend(category.strip(), time, position, cost)
    if result.empty:
        st.warning("조건에 맞는 음식점이 없습니다. 시간이나 예산을 늘려보세요.")
        st.session_state.restaurants = None
    else:
        st.session_state.restaurants = result.head(5)

# session_state에 결과가 있으면 항상 표시
if st.session_state.restaurants is not None:
    restaurants = st.session_state.restaurants
    medals = ["🥇", "🥈", "🥉"]

    with result_area:
        for rank, (_, restaurant) in enumerate(restaurants.iterrows()):
            with st.container(border=True):
                col1, col2 = st.columns([1, 5])

                with col1:
                    if rank < len(medals):
                        st.markdown(f"# {medals[rank]}")
                    else:
                        st.markdown(f"# {rank+1}")

                with col2:
                    st.subheader(restaurant["name"])
                    st.write(restaurant["category"])
                    st.write(f"도보 시간: {restaurant['walk_time']}분")

    with result_map_area:
        first_lat = restaurants.iloc[0]["lat"]
        first_lng = restaurants.iloc[0]["lng"]

        m = folium.Map(
            location=[first_lat, first_lng],
            zoom_start=16
        )

        for rank, (_, row) in enumerate(restaurants.iterrows()):
            medal = medals[rank] if rank < len(medals) else f"{rank+1}위"
            folium.Marker(
                location=[row["lat"], row["lng"]],
                popup=folium.Popup(f"{medal} {row['name']}", max_width=200),
                tooltip=row["name"]
            ).add_to(m)

        st_folium(m, use_container_width=True, height=400)