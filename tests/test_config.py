from unittest.mock import patch

from galileo.config import GalileoPythonConfig


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
