from galileo.schema.metrics import GalileoMetrics, Metric


def test_metric_custom_with_version() -> None:
    """Test that creating a Metric with a custom name and version is valid."""
    metric = Metric(name="my_custom_metric", version=2)
    assert metric.name == "my_custom_metric"
    assert metric.version == 2


def test_metric_custom_no_version() -> None:
    """Test that creating a Metric with a custom name and no version is valid."""
    metric = Metric(name="my_custom_metric")
    assert metric.name == "my_custom_metric"
    assert metric.version is None


def test_galileo_metrics_values_are_nonempty_strings() -> None:
    """All GalileoMetrics values are non-empty human-readable strings."""
    for member in GalileoMetrics:
        assert isinstance(member.value, str), f"{member.name} value is not a string"
        assert len(member.value.strip()) > 0, f"{member.name} has an empty value"


def test_galileo_metrics_is_str_compatible() -> None:
    """GalileoMetrics members are str-compatible (usable as plain strings)."""
    member = GalileoMetrics.correctness
    assert isinstance(member, str)
    assert member == "Correctness"
    assert member.value == "Correctness"


def test_galileo_metrics_naming_convention() -> None:
    """Base names map to LLM versions, _luna suffix maps to SLM versions."""
    # LLM versions (base names) should NOT have "(SLM)" in the label
    assert "(SLM)" not in GalileoMetrics.input_pii.value
    assert "(SLM)" not in GalileoMetrics.input_tone.value
    assert "(SLM)" not in GalileoMetrics.output_pii.value
    assert "(SLM)" not in GalileoMetrics.output_tone.value
    assert "(SLM)" not in GalileoMetrics.correctness.value

    # SLM versions (_luna suffix) should have "(SLM)" in the label
    assert "(SLM)" in GalileoMetrics.input_pii_luna.value
    assert "(SLM)" in GalileoMetrics.input_tone_luna.value
    assert "(SLM)" in GalileoMetrics.output_pii_luna.value
    assert "(SLM)" in GalileoMetrics.output_tone_luna.value
    assert "(SLM)" in GalileoMetrics.completeness_luna.value
