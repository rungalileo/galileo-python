import warnings

import pytest


def test_galileo_scorers_attribute_access_emits_deprecation_warning():
    """Accessing GalileoScorers.<name> should emit a DeprecationWarning."""
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        from galileo.schema.metrics import GalileoScorers

        # Access an attribute to trigger the deprecation wrapper
        _ = GalileoScorers.correctness


def test_galileo_metrics_attribute_access_does_not_warn():
    """Accessing GalileoMetrics.<name> should NOT emit a DeprecationWarning."""
    from galileo.schema.metrics import GalileoMetrics

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = GalileoMetrics.correctness
        assert not any(isinstance(x.message, DeprecationWarning) for x in w)


def test_top_level_imported_galileo_scorers_emits_deprecation_on_access():
    """Importing GalileoScorers from the top-level package and accessing attribute should warn."""
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        from galileo import GalileoScorers

        _ = GalileoScorers.correctness


def test_galileo_scorers_callable_and_lookup_delegate():
    """GalileoScorers('correctness') and GalileoScorers['correctness'] should work and warn."""
    from galileo.schema.metrics import GalileoMetrics, GalileoScorers

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member = GalileoScorers("correctness")
        assert member is GalileoMetrics.correctness

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member2 = GalileoScorers["correctness"]
        assert member2 is GalileoMetrics.correctness

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        assert "correctness" in GalileoScorers
