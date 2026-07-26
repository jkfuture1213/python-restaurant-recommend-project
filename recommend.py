import pandas as pd

# CSV 읽기
df = pd.read_csv(
    "restaurants.csv"
)

def recommend(
        category=None,
        time=0,
):
    result = df.copy()

    # 음식 종류 필터
    if category:
        if category == "아무거나":
            result = df.sample(5)
        else:
            result = result[
                result["category"]
                .str.contains(
                    category,
                    na=False
                )
            ]

    # 거리 필터
    if time:
        result = result[
            result["walk_time"]
            <= time
        ]

    # 추천 점수 계산

    result["score"] = (
        (1 /
         (result["walk_time"]+1))
        * 100
        * 0.3
    )

    return result.sort_values(
        "score",
        ascending=False
    ).reset_index(drop=True) # 데이터프레임 인덱스 초기화



# 실행

recommend_result = recommend(

    category="한식",

    time=5

)


print(
    recommend_result[
        [
            "name",
            "category",
            "distance"
        ]
    ]
)