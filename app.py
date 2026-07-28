import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
from recommend import recommend # recommend 파일에서 recommend 함수를 가져 옴.

if "KAKAO_JS_KEY" in st.secrets:    # 배포를 위한 로직, 추천 음식점 위치를 띄움.
    KAKAO_JS_KEY = st.secrets["KAKAO_JS_KEY"]

else:   # 로컬 환경 변수에 있는 API KEY 이용
    load_dotenv()
    KAKAO_JS_KEY = os.getenv("KAKAO_JS_KEY")

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

food = st.selectbox(

    "음식 세분류",

    ["치킨"]

)
st.write(food)

time = st.selectbox(

    "최대 소요 시간(분)",

    [2, 4, 6, 8, 10]

)

if time != 0:
    st.write(time)
    
cost = st.text_input("최대 예산(인당)")
st.write(cost)
    
search_button = st.button("추천 받기")
    
        
st.divider()

st.header("⭐ 추천 음식점(5순위)")

result_area = st.container()

st.subheader("📍 추천 음식점 위치")

result_map_area = st.container()

if random_button:
    restaurants = recommend("아무거나")
    
    json_restaurants = []

    for _, row in restaurants.iterrows():

        json_restaurants.append({
            "name": row["name"],
            "lat": row["lat"],
            "lng": row["lng"]
        })

    restaurant_json = json.dumps(json_restaurants, ensure_ascii=False)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false&libraries=services"></script>
    </head>
    
    <body>
    <div id="map" style="width:100%;height:500px;"></div>
    <script>
    var restaurants = {restaurant_json};
    kakao.maps.load(function(){{
        var mapContainer = document.getElementById('map');
        var options = {{
            center: new kakao.maps.LatLng(
                restaurants[0].lat,
                restaurants[0].lng
            ),
            level: 4
        }};

        var map = new kakao.maps.Map(
            mapContainer,
            options
        );
        
        // 모든 음식점 표시
        var bounds = new kakao.maps.LatLngBounds();
        restaurants.forEach(function(r){{
            var position =
                new kakao.maps.LatLng(
                    r.lat,
                    r.lng
                );
        
            var marker = new kakao.maps.Marker({{
                map:map,
                position:position
            }});
        
            var info = new kakao.maps.InfoWindow({{
                content:
                "<div style='padding:10px'>"
                + r.name +
                "</div>"
            }});
        
            kakao.maps.event.addListener(
                marker,
                'click',
                function(){{
                    info.open(map,marker);
                }}
            );
            bounds.extend(position);
        }});
        
        // 마커가 모두 보이도록 조정
        map.setBounds(bounds);
    }});

    </script>
    </body>
    """
    
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
                    
    with result_map_area:
        components.html(
            html,
            height=550
        )
        
    
if search_button:
    category = category.strip()
    
    restaurants = recommend(category, time, position).head(5) # 상위 5개 음식점만 저장
    
    json_restaurants = []
    
    for _, row in restaurants.iterrows():
    
        json_restaurants.append({
            "name": row["name"],
            "lat": row["lat"],
            "lng": row["lng"]
        })
    
    restaurant_json = json.dumps(json_restaurants, ensure_ascii=False)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false&libraries=services"></script>
    </head>
    
    <body>
    <div id="map" style="width:100%;height:500px;"></div>
    <script>
    var restaurants = {restaurant_json};
    kakao.maps.load(function(){{
        var mapContainer = document.getElementById('map');
        var options = {{
            center: new kakao.maps.LatLng(
                restaurants[0].lat,
                restaurants[0].lng
            ),
            level: 4
        }};
    
        var map = new kakao.maps.Map(
            mapContainer,
            options
        );
        
        // 모든 음식점 표시
        var bounds = new kakao.maps.LatLngBounds();
        restaurants.forEach(function(r){{
            var position =
                new kakao.maps.LatLng(
                    r.lat,
                    r.lng
                );
        
            var marker = new kakao.maps.Marker({{
                map:map,
                position:position
            }});
        
            var info = new kakao.maps.InfoWindow({{
                content:
                "<div style='padding:10px'>"
                + r.name +
                "</div>"
            }});
        
            kakao.maps.event.addListener(
                marker,
                'click',
                function(){{
                    info.open(map,marker);
                }}
            );
            bounds.extend(position);
        }});
        
        // 마커가 모두 보이도록 조정
        map.setBounds(bounds);
    }});
    
    </script>
    </body>
    """
    
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
                    
    with result_map_area:
        components.html(
            html,
            height=550
        )