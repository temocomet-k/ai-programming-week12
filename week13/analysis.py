from pathlib import Path

import pandas as pd


폴더 = Path(__file__).resolve().parent


def 읽기(파일명, 인코딩="utf-8"):
    return pd.read_csv(폴더 / 파일명, encoding=인코딩, dtype={"학번": str})


def 정제(df):
    자료 = df.copy()
    print("시작:", len(자료))
    # 점수가 없는 행을 제외한다.
    자료 = 자료.dropna(subset=["점수"])
    print("빈 점수 제거:", len(자료))
    # 모든 열이 같은 기록은 첫 번째 행만 남긴다.
    자료 = 자료.drop_duplicates().copy()
    print("중복 제거:", len(자료))
    # 같은 반과 과목이 공백 때문에 나뉘지 않게 한다.
    자료["반"] = 자료["반"].str.strip()
    자료["과목"] = 자료["과목"].str.strip()
    print("공백 정리:", len(자료))
    # 점수 범위에는 0점과 100점도 포함된다.
    자료 = 자료[자료["점수"].between(0, 100)]
    print("범위 밖 제거:", len(자료))
    return 자료


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


if __name__ == "__main__":
    원본 = 읽기("scores_2026.csv")
    print("행과 열:", 원본.shape)
    print("빈 점수와 중복:", 원본["점수"].isna().sum(), 원본.duplicated().sum())
    print("반:", 원본["반"].unique().tolist(), "과목:", 원본["과목"].unique().tolist())
    print("점수 최솟값과 최댓값:", 원본["점수"].min(), 원본["점수"].max())
    자료 = 정제(원본)

    수학 = 자료[자료["과목"] == "수학"]
    상위 = 자료[(자료["반"] == "1반") & (자료["점수"] >= 90)]
    print("수학:", len(수학), "/ 1반 90점 이상:", len(상위))
    print("반별 평균:", 반별평균(자료).to_dict())
    print(자료.groupby(["과목", "반"])["점수"].agg(["count", "mean"]).round(2))
    print(자료.groupby("반")["점수"].agg(["count", "mean", "median", "max", "sum"]).round(2))
    print("전체 점수 합:", 자료["점수"].sum())
    print("1반 수학 점수:", 수학.loc[수학["반"] == "1반", "점수"].tolist())
    미니 = 정제(읽기("mini.csv"))
    print("미니 반별 평균:", 반별평균(미니).to_dict())
