from unittest.mock import MagicMock, patch

import pytest

from galileo.config import GalileoPythonConfig
from galileo.shared.exceptions import ConfigurationError

# Auth env vars cleared in tests that exercise the missing-auth guard.
_AUTH_ENV_VARS = (
    "GALILEO_API_KEY",
    "GALILEO_SSO_ID_TOKEN",
    "GALILEO_SSO_PROVIDER",
    "GALILEO_USERNAME",
    "GALILEO_PASSWORD",
    "GALILEO_JWT_TOKEN",
)


def _clear_auth_env(monkeypatch) -> None:
    """Clear every auth-related env var so the guard sees a clean slate."""
    for var in _AUTH_ENV_VARS:
        monkeypatch.delenv(var, raising=False)


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


def test_no_auth_configured_raises_with_full_options_listed(monkeypatch) -> None:
    """When no auth is configured anywhere, the error lists every supported method."""
    # Given: no auth env vars and no cached instance
    _clear_auth_env(monkeypatch)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)

    # When/Then: calling get() without credentials raises ConfigurationError
    # listing every supported standalone or paired auth method
    with pytest.raises(ConfigurationError) as exc_info:
        GalileoPythonConfig.get()
    message = str(exc_info.value)
    assert "No Galileo authentication detected" in message
    assert "GALILEO_API_KEY" in message
    assert "GALILEO_SSO_ID_TOKEN" in message
    assert "GALILEO_SSO_PROVIDER" in message
    assert "GALILEO_USERNAME" in message
    assert "GALILEO_PASSWORD" in message


@pytest.mark.parametrize(
    "env_setup",
    [
        # Standalone methods.
        {"GALILEO_API_KEY": "test-api-key"},
        {"GALILEO_JWT_TOKEN": "test-jwt"},
        # Paired methods — both halves required.
        {"GALILEO_SSO_ID_TOKEN": "test-sso-token", "GALILEO_SSO_PROVIDER": "okta"},
        {"GALILEO_USERNAME": "test-user", "GALILEO_PASSWORD": "test-pass"},
    ],
    ids=["api_key", "jwt_token", "sso_id_token_and_provider", "username_and_password"],
)
def test_complete_auth_config_via_env_passes_guard(monkeypatch, env_setup) -> None:
    """A complete auth configuration in environment variables bypasses the guard."""
    # Given: a complete env-var auth configuration, no cached instance, and _get
    # stubbed out so downstream network calls never happen
    _clear_auth_env(monkeypatch)
    for env_var, value in env_setup.items():
        monkeypatch.setenv(env_var, value)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)
    monkeypatch.setattr(GalileoPythonConfig, "_get", lambda *a, **kw: MagicMock(spec=GalileoPythonConfig))

    # When/Then: the guard passes and _get is reached without raising
    GalileoPythonConfig.get()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"api_key": "test-api-key"},
        {"jwt_token": "test-jwt"},
        {"sso_id_token": "test-sso-token", "sso_provider": "okta"},
        {"username": "test-user", "password": "test-pass"},
    ],
    ids=["api_key", "jwt_token", "sso_id_token_and_provider", "username_and_password"],
)
def test_complete_auth_config_via_kwargs_passes_guard(monkeypatch, kwargs) -> None:
    """A complete auth configuration passed as kwargs bypasses the guard."""
    # Given: no auth env vars (kwargs are the only auth source), no cached instance,
    # and _get stubbed out so downstream network calls never happen
    _clear_auth_env(monkeypatch)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)
    monkeypatch.setattr(GalileoPythonConfig, "_get", lambda *a, **kw: MagicMock(spec=GalileoPythonConfig))

    # When/Then: the guard passes and _get is reached without raising
    GalileoPythonConfig.get(**kwargs)


def test_kwargs_and_env_can_be_mixed(monkeypatch) -> None:
    """One half of a paired auth method can come from kwargs, the other from env."""
    # Given: sso_id_token in env, sso_provider in kwargs, no cached instance,
    # and _get stubbed out so downstream network calls never happen
    _clear_auth_env(monkeypatch)
    monkeypatch.setenv("GALILEO_SSO_ID_TOKEN", "test-sso-token")
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)
    monkeypatch.setattr(GalileoPythonConfig, "_get", lambda *a, **kw: MagicMock(spec=GalileoPythonConfig))

    # When/Then: the guard accepts the mixed configuration and _get is reached without raising
    GalileoPythonConfig.get(sso_provider="okta")


@pytest.mark.parametrize(
    "env_setup,expected_missing,expected_present",
    [
        ({"GALILEO_SSO_ID_TOKEN": "test-token"}, "GALILEO_SSO_PROVIDER", "GALILEO_SSO_ID_TOKEN"),
        ({"GALILEO_SSO_PROVIDER": "okta"}, "GALILEO_SSO_ID_TOKEN", "GALILEO_SSO_PROVIDER"),
        ({"GALILEO_USERNAME": "test-user"}, "GALILEO_PASSWORD", "GALILEO_USERNAME"),
        ({"GALILEO_PASSWORD": "test-pass"}, "GALILEO_USERNAME", "GALILEO_PASSWORD"),
    ],
    ids=[
        "sso_id_token_without_provider",
        "sso_provider_without_id_token",
        "username_without_password",
        "password_without_username",
    ],
)
def test_incomplete_auth_config_rejected_with_specific_guidance(
    monkeypatch, env_setup, expected_missing, expected_present
) -> None:
    """Setting only one half of a paired auth method gives a targeted error."""
    # Given: an incomplete paired auth configuration and no cached instance
    _clear_auth_env(monkeypatch)
    for env_var, value in env_setup.items():
        monkeypatch.setenv(env_var, value)
    monkeypatch.setattr(GalileoPythonConfig, "_instance", None)

    # When/Then: the guard rejects with a message identifying both the
    # variable that's set and the one that's missing
    with pytest.raises(ConfigurationError) as exc_info:
        GalileoPythonConfig.get()
    message = str(exc_info.value)
    assert expected_present in message, f"Expected error to reference {expected_present}: {message}"
    assert expected_missing in message, f"Expected error to reference {expected_missing}: {message}"
    assert "is set but" in message, f"Expected targeted incomplete-config phrasing: {message}"
