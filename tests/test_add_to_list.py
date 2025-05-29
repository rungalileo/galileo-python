from src.galileo.add_to_list import append_lists


def test_append_lists() -> None:
    assert [1, 2, 3, 4, 5] == append_lists([1, 2, 3], [4, 5])
    assert [1, 2, 3, 4, 5] == append_lists([1], [2, 3, 4, 5])
