import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
from recommend import recommend

load_dotenv()

KAKAO_JS_KEY = os.getenv("KAKAO_JS_KEY")

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
    <script src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false&libraries=services"></script>
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
    
    restaurants = recommend(category, time).head(5) # 상위 5개 음식점만 저장
    
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
    <script src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JS_KEY}&autoload=false&libraries=services"></script>
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