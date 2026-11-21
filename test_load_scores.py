import pytest
from load_scores import load_scores


def csv_file(tmp_path, body):
    path = tmp_path / "input.csv"
    path.write_text("name,score\n" + body, encoding="utf-8")
    return path


def test_normal():
    kept, skipped = load_scores("scores.csv")
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91),
                    ("윤보람", 64), ("서한별", 95)]
    assert [row[0] for row in skipped] == [3, 4, 7, 8, 9]


def test_blank(tmp_path):
    result = load_scores(csv_file(tmp_path, "가,80\n\n나,70\n"))
    assert result == ([("가", 80), ("나", 70)], [])


def test_comma(tmp_path):
    result = load_scores(csv_file(tmp_path, '"최,네번",77\n'))
    assert result == ([("최,네번", 77)], [])


def test_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header():
    assert load_scores("empty.csv") == ([], [])


@pytest.mark.parametrize("score", [0, 100, 101])
def test_boundary(tmp_path, score):
    kept, skipped = load_scores(csv_file(tmp_path, f"가,{score}\n"))
    if score <= 100:
        assert kept == [("가", score)] and skipped == []
    else:
        assert kept == [] and skipped == [(2, "가,101", "점수가 0~100 밖")]


def test_empty_name(tmp_path):
    kept, skipped = load_scores(csv_file(tmp_path, ",90\n"))
    assert kept == []
    assert skipped == [(2, ",90", "이름이 비어 있음")]


def test_command_line():
    import subprocess
    import sys

    output = subprocess.check_output(
        [sys.executable, "load_scores.py", "scores.csv"], text=True)
    assert "읽은 줄 : 5개" in output
    assert "건너뛴 줄 : 5개" in output
