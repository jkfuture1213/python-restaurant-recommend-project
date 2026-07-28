import pandas as pd
import os

INPUT_FILE = "data/restaurants.csv"
OUTPUT_FILE = "data/restaurant_menu.csv"

# ---------------------------------
# 예상 메뉴 데이터
# ---------------------------------

MENU_DB = { # 소분류 -> 대분류 순으로 입력, 메뉴 DB 만들 때 특정 분류를 먼저 쓰고 대분류를 써야 소분류로 먼저 메뉴를 예측함.
    "회": {
        "menu": "광어회|우럭회|모둠회|참돔회|연어회|대방어회|매운탕|회덮밥|물회|해물라면",
        "price": "35000|40000|60000|70000|38000|80000|10000|12000|15000|8000"
    },
    
    "분식": {
        "menu": "김밥|라면|떡볶이|튀김",
        "price": "3500|4000|5000|6000"
    },

    "한식": {
        "menu": "비빔밥|제육볶음|된장찌개|불고기",
        "price": "8000|9000|7000|12000"
    },

    "중식": {
        "menu": "짜장면|짬뽕|탕수육|볶음밥",
        "price": "7000|8000|18000|8000"
    },

    "일식": {
        "menu": "돈까스|초밥|우동|라멘",
        "price": "9000|12000|7000|9000"
    },

    "양식": {
        "menu": "파스타|피자|스테이크",
        "price": "12000|15000|25000"
    },

    "카페": {
        "menu": "아메리카노|카페라떼|케이크",
        "price": "4000|5000|6000"
    },
}

DEFAULT_MENU = {
    "menu": "대표메뉴|세트메뉴",
    "price": "8000|10000"
}

# ---------------------------------
# 카테고리 -> 예상 메뉴
# ---------------------------------

def predict_menu(category):

    category = str(category)

    for key in MENU_DB:

        if key in category:
            return MENU_DB[key]

    return DEFAULT_MENU

# 식당 이름으로 메뉴 예측하는 로직 설계
# 프랜차이즈 메뉴 DB 설계

# ---------------------------------
# 기존 메뉴 파일 확인
# ---------------------------------

if os.path.exists(OUTPUT_FILE):

    print("기존 restaurant_menu.csv 발견")

    menu_df = pd.read_csv(
        OUTPUT_FILE
    )


else:

    print("새로운 메뉴 파일 생성")

    restaurant_df = pd.read_csv(
        INPUT_FILE
    )


    menu_df = restaurant_df.copy()


    menu_df["menu"] = ""
    menu_df["price"] = ""
    menu_df["manual"] = False



# ---------------------------------
# 빈 메뉴만 자동 생성
# ---------------------------------

for idx,row in menu_df.iterrows():

    if (
        pd.isna(row["menu"])
        or row["menu"] == ""
    ):
        result = predict_menu(
            row["category"]
        )

        menu_df.at[idx,"menu"] = result["menu"]

        menu_df.at[idx,"price"] = result["price"]

        menu_df.at[idx,"manual"] = False

# 저장
menu_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print(
    "restaurant_menu.csv 생성 완료"
)