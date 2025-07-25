import logging
from unittest.mock import Mock, patch

from galileo.projects import Projects


@patch("galileo.projects.get_all_projects_projects_all_get")
def test_get_all_projects_projects_all_get_exc(get_all_projects_projects_all_get, caplog):
    get_all_projects_projects_all_get.sync = Mock(side_effect=ValueError("unable to get all projects"))

    mock_config = Mock()
    mock_client = Mock()
    mock_config.api_client = mock_client
    projects_client = Projects(config=mock_config)
    # it doesn't trough exception, because we catch all and log
    projects_client.list()

    with caplog.at_level(logging.WARNING):
        projects_client.list()
        assert "Error occurred during execution: list: unable to get all projects" in caplog.text
