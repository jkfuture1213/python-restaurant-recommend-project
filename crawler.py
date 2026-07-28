import os
from dotenv import load_dotenv
import requests
import pandas as pd
import time
from utils.geo import load_school_polygon
from utils.geo import filter_dataframe

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

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
    


def get_school_location(address):

    url = "https://dapi.kakao.com/v2/local/search/address.json"

    headers = {

        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"

    }

    params = {

        "query": address

    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:

        raise Exception(f"API 오류: {response.status_code}")

    result = response.json()

    if len(result["documents"]) == 0:

        return None

    location = result["documents"][0]

    return {

        "lat": float(location["y"]),

        "lng": float(location["x"]),

        "address": location["address"]["address_name"]

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

def add_walk(row, my_lat, my_lng):  # 도보 시간 API 하루에 1000번 제한

    result = get_walk_time(
        my_lat,
        my_lng,
        row["lat"],
        row["lng"]
    )
    
    print(result)

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
    
    category_codes = {
        "음식점": "FD6",
        "카페": "CE7",
        "편의점": "CS2"
    }
    
    for category_name, code in category_codes.items():
        # 최대 45페이지
        for page in range(1, 4):
            params = {
                # 음식점
                "category_group_code": code,

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
                    int(item["distance"])   # 거리를 integer로 저장

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
    restaurant_all = pd.DataFrame()
    
    UNIVERSITIES = {
        "정문(복지관)": "서울 노원구 광운로 20",
        "후문": "서울 노원구 월계동 429-44", # 월계어린이공원
        "한울관": "서울 노원구 광운로 27-38",
        "누리관": "서울 노원구 광운로1길 60",
        "광운대역": "서울특별시 노원구 석계로 98-2",
    }
    WALK_SPEED = 70      # m/min
    DETOUR_RATIO = 1.5  # 실제 도보거리 / 직선거리(허용계수)
    
    polygon = load_school_polygon(
        "utils/restaurant_boundary.geojson",
        "광운대학교"
    )
    
    for university, address in UNIVERSITIES.items():
        print(f"{university} 수집 중...")
        location = get_school_location(address)

        if location is None:
            print("학교 위치를 찾을 수 없습니다.")
            exit()

        print(location)

        print("음식점 검색")
        
        restaurants = search_restaurants(
            location["lat"],
            location["lng"],
            radius=500
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
                    radius=500
                )
            )

        print(
            f"{len(restaurants)}개 음식점 발견"
        )

        df = pd.DataFrame(restaurants)
        
        # 학교 이름 컬럼 추가
        df.insert(0, "university", university)
        
        # API 호출하지 않고 도보 시간 계산, 추후에 광운대에 맞게 허용계수 조정
        df["walk_distance"] = df["distance"] * DETOUR_RATIO
        df["walk_time"] = (df["walk_distance"] / WALK_SPEED).round().astype(int)
        
        # 일정 경계를 넘어가면 걸러내는 로직, 광운대역 기찻길 뒤쪽, 누리관 쪽 장위동에서 너무 멀리 나가지 않도록 거름.
        df = filter_dataframe(df, polygon)
        
        # 기존 DataFrame에 추가
        restaurant_all = pd.concat(
            [
                restaurant_all,
                df
            ],
            ignore_index=True
        )
        print(
            f"{university} 추가 완료 : {len(df)}개"
        )
        
        """
        df["walk_time"] = df.apply( # 도보 시간 계산 로직
            lambda row: add_walk(
                row,
                location['lat'],
                location['lng']
            ), axis=1
        )
        """
        

    restaurant_all.drop_duplicates( # 중복 제거 로직
        subset=["university","name","address"],
        inplace=True
    )
    

    restaurant_all.to_csv(
        "data/restaurants.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "restaurants.csv 저장 완료"
    )