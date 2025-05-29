from src.galileo.gcd import gcd_recursive


def test_append_lists() -> None:
    assert gcd_recursive(2, 4) == 2
    assert gcd_recursive(51, 85) == 17
