import pytest

from load_scores import load_scores


@pytest.fixture
def write_scores(tmp_path):
    def write(contents):
        path = tmp_path / "scores.csv"
        path.write_text(contents, encoding="utf-8")
        return path

    return write


def test_valid_rows_keep_duplicates_and_input_order(write_scores):
    path = write_scores(
        "\ufeff이름,점수\n 민지 , 80 \n민지,95\n\"김,철수\",70\n"
    )
    assert load_scores(path) == ([("민지", 80), ("민지", 95), ("김,철수", 70)], [])


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize("contents", ["", "이름,점수\n", "이름,점수\n\n\n"])
def test_no_data_rows(write_scores, contents):
    assert load_scores(write_scores(contents)) == ([], [])


@pytest.mark.parametrize(
    ("raw_score", "expected_kept", "expected_skipped"),
    [
        ("-1", [], [(2, "민지,-1", "점수가 0~100 밖")]),
        ("0", [("민지", 0)], []),
        ("100", [("민지", 100)], []),
        ("101", [], [(2, "민지,101", "점수가 0~100 밖")]),
    ],
)
def test_score_boundaries(write_scores, raw_score, expected_kept, expected_skipped):
    path = write_scores(f"이름,점수\n민지,{raw_score}\n")
    assert load_scores(path) == (expected_kept, expected_skipped)


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("민지", "열 개수가 2가 아님"),
        ("민지,70,기타", "열 개수가 2가 아님"),
        (",70", "이름이 비어 있음"),
        ("   ,70", "이름이 비어 있음"),
        ("민지,", "점수가 비어 있음"),
        ("민지,   ", "점수가 비어 있음"),
        ("민지,결시", "점수가 정수가 아님"),
        ("민지,89.5", "점수가 정수가 아님"),
    ],
)
def test_invalid_row_records_number_original_and_reason(write_scores, row, reason):
    path = write_scores(f"이름,점수\n{row}\n")
    assert load_scores(path) == ([], [(2, row, reason)])


def test_mixed_rows_continue_after_errors_and_count_blank_lines(write_scores):
    path = write_scores("이름,점수\n가을,20\n\n겨울,결시\n봄,30\n여름,\n")
    assert load_scores(path) == (
        [("가을", 20), ("봄", 30)],
        [(4, "겨울,결시", "점수가 정수가 아님"), (6, "여름,", "점수가 비어 있음")],
    )
