"""Decision scorers decode, and the SDK asks the API for them on every scorer endpoint."""

from collections.abc import Callable
from typing import Any
from unittest.mock import Mock, patch

import pytest

from galileo.metric import DecisionMetric, Metric
from galileo.resources.api.data.get_scorer_scorers_scorer_id_get import _get_kwargs as get_scorer_kwargs
from galileo.resources.api.data.list_scorers_with_filters_scorers_list_post import _get_kwargs as list_scorers_kwargs
from galileo.resources.api.datasets.get_dataset_datasets_dataset_id_get import _get_kwargs as dataset_get_kwargs
from galileo.resources.api.integrations.list_integrations_integrations_get import _get_kwargs as integrations_get_kwargs
from galileo.resources.api.log_stream.get_metric_settings_projects_project_id_log_streams_log_stream_id_metric_settings_get import (
    _get_kwargs as log_stream_metric_settings_kwargs,
)
from galileo.resources.api.run_scorer_settings.get_settings_projects_project_id_runs_run_id_scorer_settings_get import (
    _get_kwargs as run_scorer_settings_kwargs,
)
from galileo.resources.models import ListScorersRequest, ListScorersResponse, ModelType, ScorerTypes
from galileo.resources.models.run_scorer_settings_response import RunScorerSettingsResponse
from galileo.scorers import Scorers
from galileo.utils.headers_data import get_scorer_capabilities_header

DECISION_SCORER_ID = "b7933a6d-7a65-4ce3-bfe4-b863109a0413"


def _decision_scorer_row() -> dict[str, Any]:
    return {
        "id": DECISION_SCORER_ID,
        "name": "answers_the_question",
        "label": "Answers the question",
        "scorer_type": "decision",
        "model_type": "decision",
        "tags": ["custom"],
        "created_at": "2026-10-14T18:54:02.848267+00:00",
        "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
        "updated_at": "2026-10-14T18:54:02.848269+00:00",
    }


def _list_response(*rows: dict[str, Any]) -> ListScorersResponse:
    return ListScorersResponse.from_dict(
        {"limit": 100, "next_starting_token": None, "paginated": False, "scorers": list(rows), "starting_token": 0}
    )


def test_scorer_capabilities_header_advertises_decision() -> None:
    # Given: the SDK decodes decision scorers
    # When: building the capability header value
    # Then: it is the scorer_type value the API matches
    assert get_scorer_capabilities_header() == "decision"


@pytest.mark.parametrize(
    "get_kwargs",
    [
        lambda: list_scorers_kwargs(body=ListScorersRequest()),
        lambda: get_scorer_kwargs(scorer_id="scorer-id"),
        lambda: run_scorer_settings_kwargs(project_id="project-id", run_id="run-id"),
        lambda: log_stream_metric_settings_kwargs(project_id="project-id", log_stream_id="log-stream-id"),
    ],
    ids=["list_scorers", "get_scorer", "run_scorer_settings", "log_stream_metric_settings"],
)
def test_scorer_endpoints_advertise_decision_scorers(get_kwargs: Callable[[], dict[str, Any]]) -> None:
    # Given / When: the SDK builds a request whose response carries scorer_type
    headers = get_kwargs()["content_headers"]

    # Then: the request says the SDK can decode decision scorers
    assert headers["X-Galileo-Scorer-Capabilities"] == "decision"
    assert headers["X-Galileo-SDK"].startswith("galileo-python/")


def test_other_endpoints_do_not_advertise_scorer_capabilities() -> None:
    # Given / When: requests whose responses carry no scorers
    requests = [dataset_get_kwargs(dataset_id="dataset-id"), integrations_get_kwargs()]

    # Then: they send no scorer capability header
    assert all("X-Galileo-Scorer-Capabilities" not in kwargs["content_headers"] for kwargs in requests)


def test_list_scorers_response_decodes_a_decision_scorer() -> None:
    # Given / When: the API lists a decision scorer
    response = _list_response(_decision_scorer_row())

    # Then: its type decodes to the enum instead of raising
    assert response.scorers[0].scorer_type == ScorerTypes.DECISION
    assert response.scorers[0].model_type == ModelType.DECISION


@patch("galileo.scorers.list_scorers_with_filters_scorers_list_post")
def test_scorers_list_returns_decision_scorers(list_scorers_mock: Mock) -> None:
    # Given: the API returns a decision scorer
    list_scorers_mock.sync.return_value = _list_response(_decision_scorer_row())

    # When: listing scorers
    results = Scorers().list()

    # Then: the decision scorer is returned
    assert [(result.name, result.scorer_type) for result in results] == [("answers_the_question", ScorerTypes.DECISION)]


@patch("galileo.metric.Scorers")
def test_metric_get_returns_a_decision_metric_for_a_decision_scorer(scorers_class: Mock) -> None:
    # Given: the API has a decision scorer with this name
    scorers_class.return_value.list.return_value = _list_response(_decision_scorer_row()).scorers

    # When: getting the metric by name
    metric = Metric.get(name="answers_the_question")

    # Then: it is a DecisionMetric of type decision, and it renders
    assert isinstance(metric, DecisionMetric)
    assert metric.scorer_type == ScorerTypes.DECISION
    assert "decision" in str(metric)


def test_run_scorer_settings_decode_a_decision_scorer() -> None:
    # Given / When: run scorer settings that enable a decision scorer
    settings = RunScorerSettingsResponse.from_dict(
        {
            "run_id": "c7933a6d-7a65-4ce3-bfe4-b863109a0414",
            "scorers": [{"id": DECISION_SCORER_ID, "name": "answers_the_question", "scorer_type": "decision"}],
        }
    )

    # Then: the scorer decodes instead of raising
    assert settings.scorers[0].scorer_type == ScorerTypes.DECISION
