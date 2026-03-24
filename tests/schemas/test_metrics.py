import pytest
from pydantic import ValidationError

from galileo.schema.metrics import GalileoMetricNames, GalileoMetrics, Metric
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName


def test_metric_validator_preset_with_version() -> None:
    """Test that creating a Metric with a preset name and version raises a ValidationError"""
    # Get a valid value from the ScorerName enum
    # First, get all the available enum values
    preset_names = [scorer.value for scorer in ScorerName]
    # Make sure there's at least one value
    assert preset_names, "No values found in ScorerName enum"
    preset_name = preset_names[0]

    # Attempt to create a Metric with a preset name and a version
    with pytest.raises(ValidationError) as exc_info:
        Metric(name=preset_name, version=1)

    # Verify the error message
    assert f"Galileo metric's '{preset_name}' do not support versioning at this time" in str(exc_info.value)


def test_metric_validator_preset_no_version() -> None:
    """Test that creating a Metric with a preset name and no version is valid"""
    # Get a valid value from the ScorerName enum
    preset_names = [scorer.value for scorer in ScorerName]
    assert preset_names, "No values found in ScorerName enum"
    preset_name = preset_names[0]

    # Create a Metric with a preset name and no version
    metric = Metric(name=preset_name)

    # Verify the metric is created correctly
    assert metric.name == preset_name
    assert metric.version is None


def test_metric_validator_custom_with_version() -> None:
    """Test that creating a Metric with a custom name and version is valid"""
    # Create a Metric with a custom name and a version
    metric = Metric(name="my_custom_metric", version=2)

    # Verify the metric is created correctly
    assert metric.name == "my_custom_metric"
    assert metric.version == 2


def test_metric_validator_custom_no_version() -> None:
    """Test that creating a Metric with a custom name and no version is valid"""
    # Create a Metric with a custom name and no version
    metric = Metric(name="my_custom_metric")

    # Verify the metric is created correctly
    assert metric.name == "my_custom_metric"
    assert metric.version is None


def test_galileo_metric_names_members_exist_in_galileo_metrics() -> None:
    """Every GalileoMetricNames member name has a corresponding GalileoMetrics member."""
    # Given: the full set of GalileoMetricNames members
    metric_names_members = list(GalileoMetricNames)

    # When/Then: each member name resolves in GalileoMetrics (including aliases)
    for member in metric_names_members:
        assert member.name in GalileoMetrics.__members__, (
            f"GalileoMetricNames.{member.name} has no corresponding GalileoMetrics member"
        )


def test_galileo_metric_names_values_are_nonempty_strings() -> None:
    """All GalileoMetricNames values are non-empty human-readable strings."""
    # Given: all members of GalileoMetricNames
    for member in GalileoMetricNames:
        # Then: each value is a non-empty string
        assert isinstance(member.value, str), f"{member.name} value is not a string"
        assert len(member.value.strip()) > 0, f"{member.name} has an empty value"


def test_galileo_metric_names_is_str_compatible() -> None:
    """GalileoMetricNames members are str-compatible (usable as plain strings)."""
    # Given: an arbitrary member
    member = GalileoMetricNames.correctness

    # Then: it behaves as a string
    assert isinstance(member, str)
    assert member == "Correctness"
    assert f"Metric: {member}" == "Metric: Correctness"
