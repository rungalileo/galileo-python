import warnings

import pytest

from galileo_core.schemas.shared.scorers.scorer_name import ScorerName


def test_galileo_scorers_attribute_access_emits_deprecation_warning():
    """Accessing GalileoScorers.<name> should emit a DeprecationWarning."""
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        from galileo.schema.metrics import GalileoScorers

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
    from galileo.schema.metrics import GalileoScorers

    # Value-based lookup uses the ScorerName value (internal name)
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member = GalileoScorers("correctness")
        assert member is ScorerName.correctness

    # Name-based lookup uses the member name
    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        member2 = GalileoScorers["correctness"]
        assert member2 is ScorerName.correctness

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        assert ScorerName.correctness in GalileoScorers


def test_galileo_scorers_isinstance_check():
    """isinstance checks with GalileoScorers should work — delegates to ScorerName."""
    from galileo.schema.metrics import GalileoScorers

    assert isinstance(ScorerName.correctness, GalileoScorers)
    assert not isinstance("not a scorer", GalileoScorers)


def test_galileo_scorers_issubclass_check():
    """issubclass checks with GalileoScorers should work — delegates to ScorerName."""
    from galileo.schema.metrics import GalileoScorers

    assert issubclass(type(ScorerName.correctness), GalileoScorers)


def test_galileo_scorers_returns_scorer_name_members():
    """GalileoScorers attribute access should return ScorerName enum members."""
    from galileo.schema.metrics import GalileoScorers

    with pytest.warns(DeprecationWarning, match="GalileoScorers is deprecated"):
        scorer = GalileoScorers.correctness
        assert scorer is ScorerName.correctness
        assert scorer.value == "correctness"
