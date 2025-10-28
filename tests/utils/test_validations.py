import pytest

from galileo.utils.validations import ValidationError, require_exactly_one


class TestRequireExactlyOne:
    """Test suite for the require_exactly_one decorator."""

    @pytest.mark.parametrize(
        ("kwargs", "should_succeed", "error_match"),
        [
            # 0 parameters provided
            ({}, False, "neither was defined"),
            # 1 parameter provided (success cases)
            ({"project_id": "123"}, True, None),
            ({"project_name": "MyProject"}, True, None),
            ({"project_id": ""}, True, None),  # Empty string is not None
            ({"project_id": 0}, True, None),  # Zero is not None
            # 2 parameters provided
            ({"project_id": "123", "project_name": "test"}, False, "both were defined"),
            # 3 parameters (extra param ignored, but still validates the decorated ones)
            ({"project_id": "123", "project_name": "test", "extra": "value"}, False, "both were defined"),
            # 4 parameters (extra params ignored, but still validates the decorated ones)
            ({"project_id": "123", "project_name": "test", "extra1": "v1", "extra2": "v2"}, False, "both were defined"),
        ],
    )
    def test_two_parameter_validation(self, kwargs: dict, should_succeed: bool, error_match: str) -> None:
        """Test require_exactly_one with two parameter options."""

        @require_exactly_one("project_id", "project_name")
        def func(*, project_id=None, project_name=None, **extra) -> str:
            return f"id={project_id}, name={project_name}"

        if should_succeed:
            result = func(**kwargs)
            assert isinstance(result, str)
        else:
            with pytest.raises(ValidationError, match=error_match):
                func(**kwargs)

    @pytest.mark.parametrize(
        ("kwargs", "should_succeed", "error_match"),
        [
            # 0 parameters provided
            ({}, False, "neither was defined"),
            # 1 parameter provided (success cases)
            ({"id": "1"}, True, None),
            ({"name": "test"}, True, None),
            ({"slug": "my-slug"}, True, None),
            ({"id": False}, True, None),  # False is not None
            # 2 parameters provided
            ({"id": "1", "name": "test"}, False, "both were defined"),
            ({"name": "test", "slug": "my-slug"}, False, "both were defined"),
            # 3 parameters provided
            ({"id": "1", "name": "test", "slug": "my-slug"}, False, "many were defined: id, name, slug"),
            # 4 parameters (extra param ignored, validates the 3 decorated ones)
            ({"id": "1", "name": "test", "slug": "s", "extra": "value"}, False, "many were defined: id, name, slug"),
        ],
    )
    def test_three_parameter_validation(self, kwargs: dict, should_succeed: bool, error_match: str) -> None:
        """Test require_exactly_one with three parameter options."""

        @require_exactly_one("id", "name", "slug")
        def func(*, id=None, name=None, slug=None, **extra) -> str:
            return "success"

        if should_succeed:
            result = func(**kwargs)
            assert result == "success"
        else:
            with pytest.raises(ValidationError, match=error_match):
                func(**kwargs)
