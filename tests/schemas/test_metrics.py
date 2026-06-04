from galileo.schema.metrics import SplunkAOMetrics, Metric


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
    """All SplunkAOMetrics values are non-empty human-readable strings."""
    for member in SplunkAOMetrics:
        assert isinstance(member.value, str), f"{member.name} value is not a string"
        assert len(member.value.strip()) > 0, f"{member.name} has an empty value"


def test_galileo_metrics_is_str_compatible() -> None:
    """SplunkAOMetrics members are str-compatible (usable as plain strings)."""
    member = SplunkAOMetrics.correctness
    assert isinstance(member, str)
    assert member == "Correctness"
    assert member.value == "Correctness"


def test_galileo_metrics_naming_convention() -> None:
    """Base names map to LLM versions, _luna suffix maps to SLM versions."""
    # LLM versions (base names) should NOT have "(SLM)" in the label
    assert "(SLM)" not in SplunkAOMetrics.input_pii.value
    assert "(SLM)" not in SplunkAOMetrics.input_tone.value
    assert "(SLM)" not in SplunkAOMetrics.output_pii.value
    assert "(SLM)" not in SplunkAOMetrics.output_tone.value
    assert "(SLM)" not in SplunkAOMetrics.correctness.value

    # SLM versions (_luna suffix) should have "(SLM)" in the label
    assert "(SLM)" in SplunkAOMetrics.input_pii_luna.value
    assert "(SLM)" in SplunkAOMetrics.input_tone_luna.value
    assert "(SLM)" in SplunkAOMetrics.output_pii_luna.value
    assert "(SLM)" in SplunkAOMetrics.output_tone_luna.value
    assert "(SLM)" in SplunkAOMetrics.completeness_luna.value
