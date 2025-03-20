from galileo.utils.nop_logger import galileo_logging_enabled


def test_galileo_logging_enabled(monkeypatch):
    assert galileo_logging_enabled() is False

    monkeypatch.setenv("GALILEO_LOGGING_DISABLED", "true")
    assert galileo_logging_enabled() is True

    monkeypatch.setenv("GALILEO_LOGGING_DISABLED", "1")
    assert galileo_logging_enabled() is True
