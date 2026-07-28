import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# CSV 읽기
df = pd.read_csv(
    "data/restaurant_menu.csv"
)

def get_time_slot():    # 시간대 정의
    hour = 12 # datetime.now().hour
    
    if 6 <= hour < 10:
        return "breakfast"
    elif 10 <= hour < 15:
        return "lunch"
    elif 15 <= hour < 18:
        return "dessert"
    elif 18 <= hour < 22:
        return "dinner"
    else:
        return "late"
    
TIME_KEYWORDS = {

    "breakfast": {
        "국": 3,
        "죽": 5,
        "김밥": 5,
        "토스트": 5,
        "샌드위치": 4
    },

    "lunch": {
        "국밥": 5,
        "백반": 5,
        "국수": 5,
        "돈까스": 5,
        "덮밥": 4,
        "찌개": 4,
        "분식": 4,
        "회": 2,
        "고기": 2
    },

    "dessert": {
        "카페": 5,
        "디저트": 5,
        "베이커리": 4,
        "빙수": 5,
        "아이스크림": 5
    },

    "dinner": {
        "고기": 5,
        "치킨": 5,
        "족발": 5,
        "회": 5,
        "삼겹살": 5,
        "술집": 4
    },

    "late": {
        "치킨": 5,
        "분식": 4,
        "야식": 5,
        "편의점": 3
    }
}

def time_score(category):

    slot = get_time_slot()
    keyword_scores = TIME_KEYWORDS[slot]

    print("현재 시간대:", slot)
    print("카테고리:", category)

    score = 0

    for keyword, value in keyword_scores.items():
        print(keyword, keyword in category)

        if keyword in category:
            score = max(score, value)

    print("점수:", score)
    print("----------------")

    return score

def load_menu_price(menu_df):    # 음식점에 있는 메뉴 평균 가격 계산
    df = menu_df.copy()
    
    # | 기준으로 분리
    df["price"] = df["price"].astype(str).str.split("|")

    # 리스트를 여러 행으로 변환
    df = df.explode("price")

    # 숫자로 변환
    df["price"] = pd.to_numeric(df["price"])

    # 음식점별 평균 메뉴 가격
    restaurant_price = (
        df.groupby("name")["price"]
        .mean()
        .reset_index()
    )

    restaurant_price.rename(
        columns={"price": "avg_price"},
        inplace=True
    )
    return restaurant_price

def price_score(avg_price, budget): # 음식점별 예산에 맞는지 점수 계산

    if avg_price <= budget:
        # 예산 이하라면 높은 점수
        return 1 - ((budget-avg_price)/budget)*0.3
    else:
        # 예산 초과는 강한 패널티
        return max(1 - ((avg_price-budget)/budget), 0)

def recommend(
        category=None,
        time=0,
        position="정문",
        cost=5000
):
    WALK_SPEED = 80      # m/min
    DETOUR_RATIO = 1.35  # 실제 도보거리 / 직선거리
    
    result = df.copy()
    
    menu_price = load_menu_price(result)
    
    result = result.merge(
        menu_price,
        left_on="name",
        right_on="name",
        how="left"
    )
    
    """
    result["price_score"] = result.apply(
        lambda x:
            price_score(
                x["avg_price"],
                cost
            ),
        axis=1
    )
    """
    
    # 위치 필터
    if position:
        result = result[
            result["university"]
            .str.contains(
                position,
                na=False
            )
        ]

    # 음식 종류 필터
    if category:
        if category == "아무거나":
            result = result.sample(5)
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
        
    # -----------------------------------
    # 예산 점수
    # -----------------------------------
    result["price_score"] = (
        1 - result["avg_price"] / cost
    ) * 100
    print(result["avg_price"])
    print(result["price_score"])
        
    # -----------------------------------
    # 거리 점수
    # -----------------------------------
    result["distance_score"] = (
        1 - result["distance"] / time
    ) * 100

    result["time_score"] = result["category"].apply(time_score)
    
    # -----------------------------------
    # TF-IDF + 코사인 유사도
    # -----------------------------------
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(result["category"])
    user = vectorizer.transform([category])
    sim = cosine_similarity(user, X)[0]
    
    result["similarity"] = sim * 100
    
    # -----------------------------------
    # 정규화
    # -----------------------------------
    scaler = MinMaxScaler()
    result[[
        "distance_score",
        "price_score",
        "time_score",
        "similarity"
    ]] = scaler.fit_transform(
        result[[
            "distance_score",
            "price_score",
            "time_score",
            "similarity"
        ]]
    ) * 100

    # -----------------------------------
    # 최종 AI 점수
    # -----------------------------------
    result["score"] = (
        0.30 * result["distance_score"]
        + 0.15 * result["price_score"]
        + 0.20 * result["time_score"]
        + 0.35 * result["similarity"]
    )
    print(result[["name", "distance_score", "price_score", "time_score", "similarity", "score"]].sort_values(
        "score", ascending=False).reset_index(drop=True))

    return result.sort_values(
        "score",
        ascending=False
    ).reset_index(drop=True) # 데이터프레임 인덱스 초기화
    