from unittest.mock import patch

import pytest

from galileo.config import GalileoPythonConfig
from galileo.shared.exceptions import ConfigurationError


@patch("galileo_core.schemas.base_config.GalileoConfig.set_validated_api_client", new=lambda x: x)
@patch("galileo_core.schemas.base_config.GalileoConfig.get_jwt_token")
def test_default_console_url(mock_get_jwt_token) -> None:
    """
    Test that the default console_url is used when GALILEO_CONSOLE_URL is not set.
    """
    mock_get_jwt_token.return_value = ("mock_jwt_token", "mock_refresh_token")

    # Unset the environment variable to ensure we test the default
    with patch.dict("os.environ", {}, clear=True):
        # Reset the global config object to force re-initialization
        GalileoPythonConfig.get().reset()
        config = GalileoPythonConfig.get(api_key="mock_api_key")

        assert str(config.console_url) == "https://app.galileo.ai/"
        assert str(config.api_url) == "https://api.galileo.ai/"


def test_missing_api_key_raises_clear_error(monkeypatch) -> None:
    """Test that a clear error message is raised when GALILEO_API_KEY is not set."""
    # Given: no API key in environment and no cached instance
    monkeypatch.delenv("GALILEO_API_KEY", raising=False)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)

    # When/Then: calling get() without credentials raises ConfigurationError
    with pytest.raises(ConfigurationError, match="GALILEO_API_KEY not detected"):
        GalileoPythonConfig.get()


def test_alternative_auth_kwargs_bypass_api_key_check(monkeypatch) -> None:
    """Test that passing alternative auth kwargs does not raise ConfigurationError."""
    # Given: no API key in environment and no cached instance
    monkeypatch.delenv("GALILEO_API_KEY", raising=False)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)

    # When/Then: passing username= does not raise ConfigurationError (it may fail downstream, but the guard passes)
    with pytest.raises(Exception) as exc_info:
        GalileoPythonConfig.get(username="user", password="pass")
    assert not isinstance(exc_info.value, ConfigurationError)
