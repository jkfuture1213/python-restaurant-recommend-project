import pandas as pd

# 파일 읽기
restaurant_df = pd.read_csv("data/restaurants.csv", encoding="utf-8-sig")
menu_df = pd.read_csv("data/restaurant_menu.csv", encoding="utf-8-sig")

while True:
    print("\n종료하려면 q를 입력하세요.")

    restaurant_name = input("식당 이름 : ").strip()

    if restaurant_name.lower() == "q":
        break

    # restaurant.csv에 존재하는 식당인지 확인
    if restaurant_name not in restaurant_df["name"].values:
        print("data/restaurants.csv에 없는 식당입니다.")
        continue

    # restaurant_menu.csv에 존재하는지 확인
    if restaurant_name not in menu_df["name"].values:
        print("data/restaurant_menu.csv에 없는 식당입니다.")
        continue

    menu = input("메뉴 (|로 구분) : ").strip()
    price = input("가격 (|로 구분) : ").strip()

    # 개수 확인
    menu_list = menu.split("|")
    price_list = price.split("|")

    if len(menu_list) != len(price_list):
        print("메뉴와 가격의 개수가 다릅니다.")
        continue

    # 업데이트
    idx = menu_df[menu_df["name"] == restaurant_name].index

    menu_df.loc[idx, "menu"] = menu
    menu_df.loc[idx, "price"] = price

    # 저장
    menu_df.to_csv("restaurant_menu.csv",
                   index=False,
                   encoding="utf-8-sig")

    print(f"{restaurant_name} 메뉴가 업데이트되었습니다.")