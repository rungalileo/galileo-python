import pytest
from pydantic import ValidationError

from galileo.schema.metrics import Metric
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
