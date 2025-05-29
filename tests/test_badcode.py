from galileo.badcode import gcd_recursive, is_instance_of


def test_append_lists() -> None:
    assert gcd_recursive(2, 4) == 2
    assert gcd_recursive(51, 85) == 17


def test_is_instance_of() -> None:
    class A:
        pass

    class B:
        pass

    obj_a = A()
    assert is_instance_of(obj_a, A) is True
    assert is_instance_of(obj_a, B) is False
