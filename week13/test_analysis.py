from analysis import 반별평균, 읽기, 정제


본 = 정제(읽기("scores_2026.csv"))
미니 = 정제(읽기("mini.csv"))


def test_clean_count():
    assert len(본) == 100


def test_class_labels():
    assert sorted(본["반"].unique()) == ["1반", "2반"]


def test_group_sum():
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()


def test_mini_average():
    assert 반별평균(미니)["1반"] == 80.0
