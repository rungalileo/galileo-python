from unittest.mock import ANY, Mock, patch

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
def test_list_all_scorers(list_scorers_mock: Mock):
    list_scorers_mock.sync.return_value = list_scorers_all()
    results = Scorers().list()
    actual = {}
    for r in results:
        actual[r.name] = r.scorer_type.name
    # mock return only PRESET types
    assert actual == {
        "agentic_workflow_success": "PRESET",
        "dummy_llm": "LLM",
    }
    list_scorers_mock.sync.assert_called_once_with(client=ANY, body=ListScorersRequest(filters=[]))


@patch("galileo.scorers.list_scorers_with_filters_scorers_list_post")
def test_list_all_scorers_preset_filter(list_scorers_mock: Mock):
    Scorers().list(types=[ScorerTypes.LLM])
    list_scorers_mock.sync.assert_called_once_with(client=ANY, body=ListScorersRequest(filters=[ScorerTypeFilter(operator=ScorerTypeFilterOperator.EQ, value=ScorerTypes.LLM)]))