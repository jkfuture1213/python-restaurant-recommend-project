import os
from dotenv import load_dotenv
import requests
import pandas as pd
import time

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_KEY")

# ---------------------------------
# 주소 -> 좌표 변환
# ---------------------------------

def get_location(address):

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    params = {
        "query": address
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()
    print(data)

    if len(data["documents"]) == 0:
        return None

    location = data["documents"][0]

    return {
        "lat": float(location["y"]),
        "lng": float(location["x"])
    }
    
def get_walk_time(start_lat, start_lng, end_lat, end_lng):

    url = "https://dapi.kakao.com/v2/routing/walk"

    headers = {

        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"

    }

    params = {

        "start_x": start_lng,

        "start_y": start_lat,

        "end_x": end_lng,

        "end_y": end_lat

    }

    response = requests.get(

        url,

        headers=headers,

        params=params

    )

    data = response.json()

    return data

def add_walk(row, my_lat, my_lng):

    result = get_walk_time(
        my_lat,
        my_lng,
        row["lat"],
        row["lng"]
    )

    if result["status"] != "OK":
        return None

    info = result["route"]["properties"]
    walk_distance = info["totalDistance"]
    walk_time = info["totalTime"]

    return walk_time // 60

# ---------------------------------
# 주변 음식점 검색
# ---------------------------------

def search_restaurants(
        lat,
        lng,
        radius=1000):

    url = "https://dapi.kakao.com/v2/local/search/category.json"

    headers = {
        "Authorization":
        f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    restaurants = []

    # 최대 45페이지
    for page in range(1, 4):
        params = {
            # 음식점
            "category_group_code": "FD6",

            "x": lng,
            "y": lat,

            # 최대 1km
            "radius": radius,

            "page": page,

            "size": 15
        }

        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        data = response.json()

        for item in data["documents"]:

            restaurants.append({

                "name":
                item["place_name"],

                "category":
                item["category_name"],

                "address":
                item["road_address_name"],

                "phone":
                item["phone"],

                "lat":
                item["y"],

                "lng":
                item["x"],

                "distance":
                item["distance"]

            })
            
        # 마지막 페이지면 종료
        if data["meta"]["is_end"]:
            break

        time.sleep(0.1)
        
    return restaurants

# ---------------------------------
# 실행
# ---------------------------------

if __name__ == "__main__":
    school = "광운대학교"

    print("학교 좌표 검색")

    location = get_location(school)

    if location is None:

        print("학교 위치를 찾을 수 없습니다.")
        exit()

    print(location)

    print("음식점 검색")
    
    restaurants = search_restaurants(
        location["lat"],
        location["lng"],
        radius=1000
    )
    # 격자 검색
    offset = 0.005  # 약 500m
    points = [
        (location["lat"], location["lng"]),
        (location["lat"]+offset, location["lng"]),
        (location["lat"]-offset, location["lng"]),
        (location["lat"], location["lng"]+offset),
        (location["lat"], location["lng"]-offset),
    ]

    for p in points:
        restaurants.extend(
            search_restaurants(
                p[0],
                p[1],
                radius=1000
            )
        )

    print(
        f"{len(restaurants)}개 음식점 발견"
    )

    df = pd.DataFrame(restaurants)

    df.drop_duplicates( # 중복 제거 로직
        subset=["name","address"],
        inplace=True
    )
    
    df["walk_time"] = df.apply(

        lambda row: add_walk(
        row,
        location['lat'],
        location['lng']
    ), axis=1
    )
    

    df.to_csv(
        "restaurants.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "restaurants.csv 저장 완료"
    )