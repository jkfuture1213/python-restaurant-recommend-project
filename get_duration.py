import os
import requests
import pandas as pd

KAKAO_KEY = os.getenv("KAKAO_KEY")

def get_duration(start_lat, start_lng, end_lat, end_lng):

    url = "https://apis-navi.kakaomobility.com/v1/directions"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_KEY}"
    }

    params = {
        "origin": f"{start_lng},{start_lat}",
        "destination": f"{end_lng},{end_lat}"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()


    # 소요시간(초)
    duration = data["routes"][0]["summary"]["duration"]

    return duration

df = pd.read_csv(
    "restaurants.csv"
)

df["duration"] = df.apply(

    lambda row:

    get_duration(

        my_lat,

        my_lng,

        row["lat"],

        row["lng"]

    ),

    axis=1

)

df.to_csv(

    "restaurants_with_time.csv",

    index=False

)