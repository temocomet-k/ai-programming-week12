import pytest

from bug3_logic import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param([8, 3, 4], 8, id="maximum-first"),
        pytest.param([3, 8, 4], 8, id="maximum-middle"),
        pytest.param([3, 4, 8], 8, id="maximum-last"),
        pytest.param([-8, -2, -5], -2, id="all-negative"),
        pytest.param([7, 7, 2], 7, id="repeated-maximum"),
        pytest.param([0], 0, id="single-score"),
        pytest.param([1, 2], 2, id="two-scores-increasing"),
        pytest.param([2, 1], 2, id="two-scores-decreasing"),
    ],
)
def test_find_max(scores, expected):
    assert find_max(scores) == expected


def test_empty_scores_raise_index_error():
    with pytest.raises(IndexError):
        find_max([])
