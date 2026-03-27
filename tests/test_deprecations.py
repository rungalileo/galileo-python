import warnings


def test_galileo_metrics_attribute_access_does_not_warn():
    """Accessing GalileoMetrics.<name> should NOT emit a DeprecationWarning."""
    from galileo.schema.metrics import GalileoMetrics

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = GalileoMetrics.correctness
        assert not any(isinstance(x.message, DeprecationWarning) for x in w)
