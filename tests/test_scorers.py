import uuid
from unittest.mock import ANY, Mock, patch

from src.galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse

from galileo.resources.models import (
    ListScorersRequest,
    ListScorersResponse,
    ScorerTypeFilter,
    ScorerTypeFilterOperator,
    ScorerTypes,
)
from galileo.scorers import Scorers


def list_scorers_all():
    return ListScorersResponse.from_dict(
        {
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "scorers": [
                {
                    "label": "Action Advancement",
                    "id": "f7933a6d-7a65-4ce3-bfe4-b863109a04ee",
                    "name": "agentic_workflow_success",
                    "scorer_type": "preset",
                    "tags": ["preset", "agents"],
                    "created_at": "2025-03-28T18:54:02.848267+00:00",
                    "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
                    "defaults": {"filters": None, "model_name": "GPT-4o", "num_judges": 5},
                    "description": "Detects whether the user successfully accomplished or advanced towards their goal.",
                    "included_fields": ["model_name", "num_judges", "filters"],
                    "latest_version": None,
                    "updated_at": "2025-03-28T18:54:02.848269+00:00",
                },
                {
                    "label": "dummy",
                    "id": "a7933a6d-7a65-4ce3-bfe4-b863109a0412",
                    "name": "dummy_llm",
                    "scorer_type": "llm",
                    "tags": ["llm"],
                    "created_at": "2025-03-28T18:54:02.848267+00:00",
                    "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
                    "updated_at": "2025-03-28T18:54:02.848269+00:00",
                },
            ],
            "starting_token": 0,
        }
    )


@patch("galileo.scorers.list_scorers_with_filters_scorers_list_post")
def test_list_all_scorers(list_scorers_mock: Mock) -> None:
    list_scorers_mock.sync.return_value = list_scorers_all()
    results = Scorers().list()
    actual = {}
    for r in results:
        actual[r.name] = r.scorer_type.name
    assert actual == {"agentic_workflow_success": "PRESET", "dummy_llm": "LLM"}
    list_scorers_mock.sync.assert_called_once_with(client=ANY, body=ListScorersRequest(filters=[]), starting_token=0)


@patch("galileo.scorers.list_scorers_with_filters_scorers_list_post")
def test_list_all_scorers_preset_filter(list_scorers_mock: Mock) -> None:
    list_scorers_mock.sync.return_value = list_scorers_all()
    Scorers().list(types=[ScorerTypes.LLM])
    list_scorers_mock.sync.assert_called_once_with(
        client=ANY,
        body=ListScorersRequest(
            filters=[ScorerTypeFilter(operator=ScorerTypeFilterOperator.EQ, value=ScorerTypes.LLM)]
        ),
        starting_token=0,
    )


def list_scorers_paginated_page_1():
    return ListScorersResponse.from_dict(
        {
            "limit": 2,
            "next_starting_token": 2,
            "paginated": True,
            "scorers": [
                {
                    "label": "Tool Selection Quality",
                    "id": "f7933a6d-7a65-4ce3-bfe4-b863109a04ee",
                    "name": "tool_selection_quality",
                    "scorer_type": "preset",
                    "tags": ["preset", "tools"],
                    "created_at": "2025-03-28T18:54:02.848267+00:00",
                    "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
                    "defaults": {"filters": None, "model_name": "GPT-4o", "num_judges": 3},
                    "description": "Evaluates tool selection quality.",
                    "included_fields": ["model_name", "num_judges", "filters"],
                    "latest_version": None,
                    "updated_at": "2025-03-28T18:54:02.848269+00:00",
                },
                {
                    "label": "Tool Error Rate",
                    "id": "a7933a6d-7a65-4ce3-bfe4-b863109a0412",
                    "name": "tool_error_rate",
                    "scorer_type": "preset",
                    "tags": ["preset", "tools"],
                    "created_at": "2025-03-28T18:54:02.848267+00:00",
                    "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
                    "defaults": {"filters": None, "model_name": "GPT-4o", "num_judges": 3},
                    "description": "Evaluates tool error rate.",
                    "included_fields": ["model_name", "num_judges", "filters"],
                    "latest_version": None,
                    "updated_at": "2025-03-28T18:54:02.848269+00:00",
                },
            ],
            "starting_token": 0,
        }
    )


def list_scorers_paginated_page_2():
    return ListScorersResponse.from_dict(
        {
            "limit": 2,
            "next_starting_token": None,
            "paginated": True,
            "scorers": [
                {
                    "label": "Final Scorer",
                    "id": "c7933a6d-7a65-4ce3-bfe4-b863109a0413",
                    "name": "final_scorer",
                    "scorer_type": "preset",
                    "tags": ["preset", "final"],
                    "created_at": "2025-03-28T18:54:02.848267+00:00",
                    "created_by": "d351012a-dd92-4d0c-a356-57161b1377cd",
                    "defaults": {"filters": None, "model_name": "GPT-4o", "num_judges": 3},
                    "description": "Final scorer.",
                    "included_fields": ["model_name", "num_judges", "filters"],
                    "latest_version": None,
                    "updated_at": "2025-03-28T18:54:02.848269+00:00",
                }
            ],
            "starting_token": 2,
        }
    )


@patch("galileo.scorers.list_scorers_with_filters_scorers_list_post")
def test_list_scorers_with_pagination(list_scorers_mock: Mock) -> None:
    """Test that Scorers().list() correctly handles pagination by fetching all pages."""

    # Setup mock to return different responses for different starting tokens
    def mock_sync_side_effect(*args, **kwargs):
        starting_token = kwargs.get("starting_token", 0)
        if starting_token == 0:
            return list_scorers_paginated_page_1()
        elif starting_token == 2:
            return list_scorers_paginated_page_2()
        else:
            raise ValueError(f"Unexpected starting_token: {starting_token}")

    list_scorers_mock.sync.side_effect = mock_sync_side_effect

    # Execute the method
    results = Scorers().list()

    # Verify results contain scorers from both pages
    actual = {r.name: r.scorer_type.name for r in results}
    assert actual == {"tool_selection_quality": "PRESET", "tool_error_rate": "PRESET", "final_scorer": "PRESET"}

    # Verify both pages were fetched
    assert list_scorers_mock.sync.call_count == 2
    list_scorers_mock.sync.assert_any_call(client=ANY, body=ListScorersRequest(filters=[]), starting_token=0)
    list_scorers_mock.sync.assert_any_call(client=ANY, body=ListScorersRequest(filters=[]), starting_token=2)


def create_mock_version_response():
    return BaseScorerVersionResponse.from_dict(
        {
            "id": "b8933a6d-7a65-4ce3-bfe4-b863109a0425",
            "version": 2,
            "model_name": "GPT-4o",
            "num_judges": 3,
            "created_at": "2025-03-28T18:54:02.848267+00:00",
            "updated_at": "2025-03-28T18:54:02.848269+00:00",
            "generated_scorer": {
                "id": "c7933a6d-7a65-4ce3-bfe4-b863109a0499",
                "name": "test_generated_scorer",
                "instructions": "Evaluate the response quality",
                "chain_poll_template": {
                    "name": "quality_check",
                    "prompt": "Rate the quality on a scale of 1-10",
                    "template_type": "standard",
                },
            },
            "registered_scorer": None,
        }
    )


class MockHTTPError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f"HTTP Error: {status_code}")


@patch("galileo.scorers.get_scorer_version_or_latest_scorers_scorer_id_version_get")
def test_get_scorer_version_success(get_scorer_version_mock: Mock) -> None:
    # Setup
    mock_response = create_mock_version_response()
    get_scorer_version_mock.sync.return_value = mock_response
    scorer_id = uuid.UUID("b8933a6d-7a65-4ce3-bfe4-b863109a0425")
    version = 2

    # Execute
    result = Scorers().get_scorer_version(scorer_id=scorer_id, version=version)

    # Verify
    assert result == mock_response
    get_scorer_version_mock.sync.assert_called_once_with(scorer_id=scorer_id, version=version, client=ANY)
    assert result.id == "b8933a6d-7a65-4ce3-bfe4-b863109a0425"
    assert result.version == 2
    # Access properties from additional_properties instead
    assert result.model_name == "GPT-4o"
    assert result.num_judges == 3
    # Access generated_scorer as a dictionary
    assert result.generated_scorer["name"] == "test_generated_scorer"
    assert result.registered_scorer is None
