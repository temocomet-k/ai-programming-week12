import pytest

from load_scores import load_scores


def write_csv(tmp_path, *rows):
    path = tmp_path / "성적.csv"
    path.write_text("\n".join(("name,score", *rows)) + "\n", encoding="utf-8")
    return path


def assert_skipped(entry, line_number, raw_line):
    actual_number, actual_line, reason = entry
    assert actual_number == line_number
    # 줄 종결자의 보관 여부와 무관하게 공백을 포함한 원문을 확인한다.
    assert actual_line.removesuffix("\n").removesuffix("\r") == raw_line
    assert isinstance(reason, str) and reason.strip()


def test_valid_rows_keep_order_duplicates_and_integer_scores(tmp_path):
    path = write_csv(
        tmp_path,
        "  지민  ,  0  ",
        '"김, 민수",100',
        "지민,76",
        "지민,76",
    )

    kept, skipped = load_scores(path)

    assert kept == [("지민", 0), ("김, 민수", 100), ("지민", 76), ("지민", 76)]
    assert all(type(score) is int for _, score in kept)
    assert skipped == []


@pytest.mark.parametrize(
    "row",
    [
        pytest.param("민수", id="too-few-columns"),
        pytest.param("민수,20,30", id="too-many-columns"),
        pytest.param(",60", id="empty-name"),
        pytest.param("   ,60", id="whitespace-only-name"),
        pytest.param("민수,", id="empty-score"),
        pytest.param("민수,   ", id="whitespace-only-score"),
        pytest.param("민수,구십", id="text-score"),
        pytest.param("민수,6.5", id="fractional-score"),
        pytest.param("민수,-1", id="below-minimum"),
        pytest.param("민수,101", id="above-maximum"),
    ],
)
def test_invalid_row_is_logged_and_excluded(tmp_path, row):
    path = write_csv(tmp_path, row)
    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    assert_skipped(skipped[0], 2, row)


def test_mixed_rows_report_physical_line_numbers(tmp_path):
    path = write_csv(
        tmp_path,
        "",
        "유리,41",
        "  민수 , 잘못된 값  ",
        "",
        "유리,",
        "",
        "유리,42",
    )

    kept, skipped = load_scores(path)

    assert kept == [("유리", 41), ("유리", 42)]
    assert len(skipped) == 2
    assert_skipped(skipped[0], 4, "  민수 , 잘못된 값  ")
    assert_skipped(skipped[1], 6, "유리,")


@pytest.mark.parametrize("rows", [(), ("", "")], ids=["header-only", "blank-lines"])
def test_no_data_rows(tmp_path, rows):
    assert load_scores(write_csv(tmp_path, *rows)) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "없는파일.csv")
