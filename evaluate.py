import os
import random
import time

import pandas as pd
import matplotlib.pyplot as plt

from recommend import recommend


# ===============================
# 설정
# ===============================

TEST_COUNT = 500

SAVE_DIR = "result"

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)


categories = [
    "한식",
    "중식",
    "일식",
    "양식",
    "카페",
    "분식"
]


positions = [
    "정문",
    "후문"
]


budgets = [
    5000,
    7000,
    10000,
    15000,
    20000
]


# 결과 저장
records = []



# ===============================
# 테스트 실행
# ===============================

print("성능 평가 시작")


for i in range(TEST_COUNT):

    category = random.choice(categories)

    position = random.choice(positions)

    budget = random.choice(budgets)

    walk_time = random.randint(
        5,
        20
    )


    start = time.perf_counter()


    result = recommend(
        category=category,
        time=walk_time,
        position=position,
        cost=budget,
        verbose=False
    )


    end = time.perf_counter()


    response_time = (
        end - start
    )


    # 추천 결과 없음
    if result.empty:
        continue


    # Top-1
    top1 = result.iloc[0]


    # Top-5
    top5 = result.head(5)



    records.append({

        # 사용자 정보
        "category":
            category,

        "position":
            position,

        "budget":
            budget,

        "limit_time":
            walk_time,


        # 성능
        "response_time":
            response_time,


        # Top1
        "top1_score":
            top1["score"],

        "top1_distance":
            top1["distance"],

        "top1_walk_time":
            top1["walk_time"],

        "top1_price":
            top1["avg_price"],


        # Top5
        "top5_score":
            top5["score"].mean(),

        "top5_distance":
            top5["distance"].mean(),

        "top5_price":
            top5["avg_price"].mean(),


        # 예산 만족
        "budget_success":
            top1["avg_price"] <= budget,


        # 점수 요소
        "distance_score":
            top1["distance_score"],

        "price_score":
            top1["price_score"],

        "time_score":
            top1["time_score"],

        "similarity":
            top1["similarity"]

    })


print("평가 완료")



# ===============================
# CSV 저장
# ===============================

metrics = pd.DataFrame(records)


metrics.to_csv(
    f"{SAVE_DIR}/metrics.csv",
    index=False,
    encoding="utf-8-sig"
)



# ===============================
# 결과 출력
# ===============================


print("\n========== 평가 결과 ==========")


print(
    f"테스트 수 : {len(metrics)}"
)


print(
    f"평균 Top-1 점수 : "
    f"{metrics['top1_score'].mean():.2f}"
)


print(
    f"평균 Top-5 점수 : "
    f"{metrics['top5_score'].mean():.2f}"
)


print(
    f"평균 거리 : "
    f"{metrics['top1_distance'].mean():.1f}m"
)


print(
    f"평균 도보시간 : "
    f"{metrics['top1_walk_time'].mean():.1f}분"
)


print(
    f"평균 응답시간 : "
    f"{metrics['response_time'].mean()*1000:.2f}ms"
)


print(
    f"예산 만족률 : "
    f"{metrics['budget_success'].mean()*100:.2f}%"
)


print("==============================")



# ===============================
# 시각화
# ===============================


plt.rcParams["font.family"] = "AppleGothic"



# 1. 음식 카테고리 분포

plt.figure(figsize=(7,4))

metrics["category"].value_counts().plot(
    kind="bar"
)

plt.title(
    "음식 카테고리 분포"
)

plt.xlabel(
    "카테고리"
)

plt.ylabel(
    "추천 횟수"
)

plt.tight_layout()

plt.savefig(
    f"{SAVE_DIR}/category_distribution.png"
)

plt.close()



# 2. 거리 분포


plt.figure(figsize=(7,4))


metrics["top1_distance"].plot(
    kind="hist",
    bins=20
)


plt.title(
    "추천 음식점 거리 분포"
)


plt.xlabel(
    "거리(m)"
)


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/distance_distribution.png"
)


plt.close()



# 3. 추천 점수 분포


plt.figure(figsize=(7,4))


metrics["top1_score"].plot(
    kind="hist",
    bins=20
)


plt.title(
    "추천 점수 분포"
)


plt.xlabel(
    "Score"
)


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/score_distribution.png"
)


plt.close()



# 4. 응답시간


plt.figure(figsize=(7,4))


plt.plot(
    metrics["response_time"] * 1000
)


plt.title(
    "추천 응답 시간"
)


plt.xlabel(
    "요청 번호"
)


plt.ylabel(
    "ms"
)


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/response_time.png"
)


plt.close()



# 5. 예산 만족도


plt.figure(figsize=(5,5))


metrics["budget_success"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)


plt.title(
    "예산 만족도"
)


plt.ylabel("")


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/budget_satisfaction.png"
)


plt.close()



# 6. 점수 구성 요소 분석


score_component = pd.DataFrame({

    "거리 점수":
        [metrics["distance_score"].mean()],

    "가격 점수":
        [metrics["price_score"].mean()],

    "시간 점수":
        [metrics["time_score"].mean()],

    "카테고리 유사도":
        [metrics["similarity"].mean()]

})


plt.figure(figsize=(7,4))


score_component.T.plot(
    kind="bar",
    legend=False
)


plt.title(
    "추천 점수 구성 요소 평균"
)


plt.ylabel(
    "점수"
)


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/score_component.png"
)


plt.close()



# 7. 거리-점수 관계


plt.figure(figsize=(7,4))


plt.scatter(
    metrics["top1_distance"],
    metrics["top1_score"]
)


plt.xlabel(
    "거리(m)"
)


plt.ylabel(
    "추천 점수"
)


plt.title(
    "거리와 추천 점수 관계"
)


plt.tight_layout()


plt.savefig(
    f"{SAVE_DIR}/distance_score.png"
)


plt.close()



print("\n그래프 생성 완료")
print(f"저장 위치 : {SAVE_DIR}/")