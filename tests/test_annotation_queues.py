from datetime import datetime, timezone
from unittest.mock import ANY, Mock, patch

import pytest

from galileo.annotation_queues import (
    AnnotationField,
    AnnotationQueue,
    AnnotationQueues,
    AnnotationQueuesAPIException,
    AnnotationQueueUser,
    add_records_to_annotation_queue,
    create_annotation_queue,
    create_annotation_queue_field,
    delete_annotation_queue,
    delete_annotation_queue_field,
    get_annotation_queue,
    get_annotation_queue_records,
    list_annotation_queue_fields,
    list_annotation_queue_users,
    list_annotation_queues,
    remove_annotation_queue_user,
    remove_records_from_annotation_queue,
    share_annotation_queue,
    update_annotation_queue,
    update_annotation_queue_field,
    update_annotation_queue_user,
)
from galileo.exceptions import NotFoundError
from galileo.resources.models.add_records_to_queue_response import AddRecordsToQueueResponse
from galileo.resources.models.and_node_log_records_filter import AndNodeLogRecordsFilter
from galileo.resources.models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
from galileo.resources.models.annotation_queue_response import AnnotationQueueResponse
from galileo.resources.models.annotation_template_db import AnnotationTemplateDB
from galileo.resources.models.collaborator_role import CollaboratorRole
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.like_dislike_constraints import LikeDislikeConstraints
from galileo.resources.models.list_annotation_queue_collaborators_response import (
    ListAnnotationQueueCollaboratorsResponse,
)
from galileo.resources.models.list_annotation_queue_response import ListAnnotationQueueResponse
from galileo.resources.models.log_records_partial_query_response import LogRecordsPartialQueryResponse
from galileo.resources.models.remove_records_from_queue_response import RemoveRecordsFromQueueResponse
from galileo.resources.models.tree_choice_constraints import TreeChoiceConstraints
from galileo.resources.models.tree_choice_db_constraints import TreeChoiceDBConstraints
from galileo.resources.models.tree_choice_node import TreeChoiceNode
from galileo.resources.models.user_annotation_queue_collaborator import UserAnnotationQueueCollaborator
from galileo.resources.models.validation_error import ValidationError
from galileo.resources.types import UNSET


def make_annotation_queue_response() -> AnnotationQueueResponse:
    return AnnotationQueueResponse(
        id="queue-123",
        name="review queue",
        description="Needs human review",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
        created_by_user=None,
    )


def make_annotation_field_response() -> AnnotationTemplateDB:
    return AnnotationTemplateDB(
        id="field-123",
        name="quality",
        include_explanation=True,
        constraints=LikeDislikeConstraints(annotation_type="like_dislike"),
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        created_by=None,
        position=1,
        usage_count=0,
        criteria="Check quality",
    )


def make_annotation_queue_user_response() -> UserAnnotationQueueCollaborator:
    return UserAnnotationQueueCollaborator(
        id="collab-123",
        role=CollaboratorRole.ANNOTATOR,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        user_id="user-123",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
        annotation_queue_id="queue-123",
        track_progress=True,
        progress=0.5,
    )


@pytest.fixture
def mock_config() -> Mock:
    return Mock(api_client=Mock())


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.create_annotation_queue_annotation_queues_post.sync")
def test_create_annotation_queue_sends_expected_request(mock_create: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful create response
    mock_get_config.return_value = mock_config
    mock_create.return_value = make_annotation_queue_response()

    # When: creating an annotation queue
    queue = create_annotation_queue(
        name=" review queue ",
        description="Needs human review",
        annotator_emails=["person@example.com"],
        copy_fields_from_queue_id="field-source",
    )

    # Then: the generated endpoint receives the expected request body
    assert isinstance(queue, AnnotationQueue)
    assert queue.id == "queue-123"
    mock_create.assert_called_once_with(client=ANY, body=ANY)
    body = mock_create.call_args.kwargs["body"]
    assert body.name.value == "review queue"
    assert body.name.append_suffix_if_duplicate is False
    assert body.description == "Needs human review"
    assert body.annotator_emails == ["person@example.com"]
    assert body.copy_templates_from_queue_id == "field-source"


def test_annotation_queue_wraps_fields():
    # Given: an annotation queue response with generated field models
    response = make_annotation_queue_response()
    response.templates = [make_annotation_field_response()]

    # When: wrapping the response in an SDK annotation queue
    queue = AnnotationQueue(response)

    # Then: fields are exposed as SDK annotation field objects
    assert isinstance(queue.fields[0], AnnotationField)
    assert queue.fields[0].id == "field-123"


def test_annotation_field_converts_tree_choice_db_constraints():
    # Given: a generated field response with response-only tree choice constraints
    response = make_annotation_field_response()
    response.constraints = TreeChoiceDBConstraints(
        annotation_type="tree_choice",
        choices_tree=[TreeChoiceNode(label="Helpful", id="helpful")],
        choices_tree_yaml="- id: helpful\n  label: Helpful",
    )

    # When: wrapping the response in an SDK annotation field
    field = AnnotationField(response)

    # Then: constraints are exposed with the public tree choice type
    assert isinstance(field.constraints, TreeChoiceConstraints)
    assert field.constraints.choices_tree_yaml == "- id: helpful\n  label: Helpful"


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.share_annotation_queue_with_users_annotation_queues_queue_id_users_post.sync")
def test_share_annotation_queue_sends_expected_request(mock_share: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful share response
    mock_get_config.return_value = mock_config
    mock_share.return_value = [make_annotation_queue_user_response()]

    # When: sharing an annotation queue by email
    user = share_annotation_queue(
        " queue-123 ", user_email=" ada@example.com ", role=CollaboratorRole.ANNOTATOR, track_progress=False
    )

    # Then: the generated endpoint receives the expected request body
    assert isinstance(user, AnnotationQueueUser)
    assert user.user_id == "user-123"
    mock_share.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_share.call_args.kwargs["body"]
    assert len(body) == 1
    assert body[0].user_email == "ada@example.com"
    assert body[0].user_id is UNSET
    assert body[0].role == CollaboratorRole.ANNOTATOR
    assert body[0].track_progress is False


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.share_annotation_queue_with_users_annotation_queues_queue_id_users_post.sync")
def test_share_annotation_queue_accepts_user_id(mock_share: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful share response
    mock_get_config.return_value = mock_config
    mock_share.return_value = [make_annotation_queue_user_response()]

    # When: sharing an annotation queue by user ID
    user = share_annotation_queue(" queue-123 ", user_id=" user-123 ", role=CollaboratorRole.OWNER)

    # Then: the generated endpoint receives a user ID collaborator body
    assert isinstance(user, AnnotationQueueUser)
    mock_share.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_share.call_args.kwargs["body"]
    assert len(body) == 1
    assert body[0].user_id == "user-123"
    assert body[0].user_email is UNSET
    assert body[0].role == CollaboratorRole.OWNER


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.create_queue_template_annotation_queues_queue_id_templates_post.sync")
def test_create_annotation_queue_field_sends_expected_request(
    mock_create: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful create field response
    mock_get_config.return_value = mock_config
    existing_field = make_annotation_field_response()
    existing_field.id = "field-existing"
    existing_field.name = "existing"
    mock_create.return_value = [existing_field, make_annotation_field_response()]
    constraints = LikeDislikeConstraints(annotation_type="like_dislike")

    # When: creating an annotation queue field
    field = create_annotation_queue_field(
        " queue-123 ", name=" quality ", constraints=constraints, include_explanation=True, criteria="Check quality"
    )

    # Then: the generated endpoint receives the expected request body
    assert isinstance(field, AnnotationField)
    assert field.id == "field-123"
    mock_create.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_create.call_args.kwargs["body"]
    assert body.template.name == "quality"
    assert body.template.constraints is constraints
    assert body.template.include_explanation is True
    assert body.template.criteria == "Check quality"


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.get_queue_templates_annotation_queues_queue_id_templates_get.sync")
def test_list_annotation_queue_fields_returns_fields(mock_list: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful list fields response
    mock_get_config.return_value = mock_config
    mock_list.return_value = [make_annotation_field_response()]

    # When: listing annotation queue fields
    fields = list_annotation_queue_fields(" queue-123 ")

    # Then: fields are exposed as SDK annotation field objects
    assert len(fields) == 1
    assert isinstance(fields[0], AnnotationField)
    assert fields[0].id == "field-123"
    mock_list.assert_called_once_with(queue_id="queue-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.list_annotation_queue_users_annotation_queues_queue_id_users_get.sync")
def test_list_annotation_queue_users_returns_all_pages(mock_list: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: two pages of annotation queue users
    mock_get_config.return_value = mock_config
    second_user = make_annotation_queue_user_response()
    second_user.id = "collab-456"
    second_user.user_id = "user-456"
    second_user.email = "grace@example.com"
    mock_list.side_effect = [
        ListAnnotationQueueCollaboratorsResponse(
            collaborators=[make_annotation_queue_user_response()], paginated=True, next_starting_token=100
        ),
        ListAnnotationQueueCollaboratorsResponse(collaborators=[second_user]),
    ]

    # When: listing annotation queue users
    users = list_annotation_queue_users(" queue-123 ")

    # Then: the SDK returns users from each page
    assert [user.email for user in users] == ["ada@example.com", "grace@example.com"]
    assert isinstance(users[0], AnnotationQueueUser)
    assert mock_list.call_count == 2
    assert mock_list.call_args_list[0].kwargs["starting_token"] == 0
    assert mock_list.call_args_list[1].kwargs["starting_token"] == 100


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.list_annotation_queue_users_annotation_queues_queue_id_users_get.sync")
def test_list_annotation_queue_users_continues_when_paginated_flag_is_false(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a response with an advancing next token but no paginated flag
    mock_get_config.return_value = mock_config
    second_user = make_annotation_queue_user_response()
    second_user.id = "collab-456"
    second_user.user_id = "user-456"
    second_user.email = "grace@example.com"
    mock_list.side_effect = [
        ListAnnotationQueueCollaboratorsResponse(
            collaborators=[make_annotation_queue_user_response()], paginated=False, next_starting_token=100
        ),
        ListAnnotationQueueCollaboratorsResponse(collaborators=[second_user]),
    ]

    # When: listing annotation queue users
    users = list_annotation_queue_users(" queue-123 ")

    # Then: the SDK treats the advancing token as authoritative
    assert [user.email for user in users] == ["ada@example.com", "grace@example.com"]
    assert mock_list.call_count == 2
    assert mock_list.call_args_list[1].kwargs["starting_token"] == 100


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.list_annotation_queue_users_annotation_queues_queue_id_users_get.sync")
def test_list_annotation_queue_users_stops_when_next_token_is_unset(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a paginated response without a next page token
    mock_get_config.return_value = mock_config
    mock_list.return_value = ListAnnotationQueueCollaboratorsResponse(
        collaborators=[make_annotation_queue_user_response()], paginated=True, next_starting_token=UNSET
    )

    # When: listing annotation queue users
    users = list_annotation_queue_users(" queue-123 ")

    # Then: the SDK returns the page and does not re-request page 0
    assert [user.email for user in users] == ["ada@example.com"]
    mock_list.assert_called_once_with(queue_id="queue-123", client=ANY, starting_token=0)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.list_annotation_queue_users_annotation_queues_queue_id_users_get.sync")
def test_list_annotation_queue_users_stops_when_next_token_does_not_advance(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a paginated response whose next token repeats the current token
    mock_get_config.return_value = mock_config
    mock_list.return_value = ListAnnotationQueueCollaboratorsResponse(
        collaborators=[make_annotation_queue_user_response()], paginated=True, next_starting_token=0
    )

    # When: listing annotation queue users
    users = list_annotation_queue_users(" queue-123 ")

    # Then: the SDK returns the page and does not loop forever
    assert [user.email for user in users] == ["ada@example.com"]
    mock_list.assert_called_once_with(queue_id="queue-123", client=ANY, starting_token=0)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.add_records_to_annotation_queue_annotation_queues_queue_id_records_post.sync")
def test_add_records_to_annotation_queue_sends_expected_request(
    mock_add: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful add records response
    mock_get_config.return_value = mock_config
    mock_add.return_value = AddRecordsToQueueResponse(num_records_added=2)

    # When: adding records to an annotation queue
    count = add_records_to_annotation_queue(
        " queue-123 ",
        project_id=" project-123 ",
        experiment_id=" experiment-123 ",
        record_ids=[" record-1 ", "record-2"],
    )

    # Then: the generated endpoint receives a record IDs selector
    assert count == 2
    mock_add.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_add.call_args.kwargs["body"]
    assert body.project_id == "project-123"
    assert body.run_id == "experiment-123"
    assert body.record_selector.type_ == "record_ids"
    assert body.record_selector.record_ids == ["record-1", "record-2"]


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.add_records_to_annotation_queue_annotation_queues_queue_id_records_post.sync")
def test_add_records_to_annotation_queue_accepts_log_stream_id(
    mock_add: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful add records response
    mock_get_config.return_value = mock_config
    mock_add.return_value = AddRecordsToQueueResponse(num_records_added=1)

    # When: adding log stream records to an annotation queue
    add_records_to_annotation_queue(
        "queue-123", project_id="project-123", log_stream_id=" log-stream-123 ", record_ids=["record-1"]
    )

    # Then: the generated request uses the log stream ID as the API run ID
    body = mock_add.call_args.kwargs["body"]
    assert body.run_id == "log-stream-123"


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.add_records_to_annotation_queue_annotation_queues_queue_id_records_post.sync")
def test_add_records_to_annotation_queue_forwards_filter_selector(
    mock_add: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a generated filter-tree selector
    mock_get_config.return_value = mock_config
    mock_add.return_value = AddRecordsToQueueResponse(num_records_added=3)
    record_selector = AnnotationQueueRecordsByFilterTree(filter_tree=AndNodeLogRecordsFilter(and_=[]))

    # When: adding records by filter tree
    count = add_records_to_annotation_queue(
        "queue-123", project_id="project-123", experiment_id="experiment-123", record_selector=record_selector
    )

    # Then: the generated endpoint receives the selector unchanged
    assert count == 3
    body = mock_add.call_args.kwargs["body"]
    assert body.record_selector is record_selector


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch(
    "galileo.annotation_queues.remove_records_from_annotation_queue_annotation_queues_queue_id_records_remove_post.sync"
)
def test_remove_records_from_annotation_queue_sends_expected_request(
    mock_remove: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful remove records response
    mock_get_config.return_value = mock_config
    mock_remove.return_value = RemoveRecordsFromQueueResponse(num_records_removed=1)

    # When: removing records from an annotation queue
    count = remove_records_from_annotation_queue(" queue-123 ", record_ids=[" record-1 "])

    # Then: the generated endpoint receives a record IDs selector
    assert count == 1
    mock_remove.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_remove.call_args.kwargs["body"]
    assert body.record_selector.type_ == "record_ids"
    assert body.record_selector.record_ids == ["record-1"]


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch(
    "galileo.annotation_queues.remove_records_from_annotation_queue_annotation_queues_queue_id_records_remove_post.sync"
)
def test_remove_records_from_annotation_queue_forwards_filter_selector(
    mock_remove: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a generated filter-tree selector
    mock_get_config.return_value = mock_config
    mock_remove.return_value = RemoveRecordsFromQueueResponse(num_records_removed=3)
    record_selector = AnnotationQueueRecordsByFilterTree(filter_tree=AndNodeLogRecordsFilter(and_=[]))

    # When: removing records by filter tree
    count = remove_records_from_annotation_queue("queue-123", record_selector=record_selector)

    # Then: the generated endpoint receives the selector unchanged
    assert count == 3
    body = mock_remove.call_args.kwargs["body"]
    assert body.record_selector is record_selector


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch(
    "galileo.annotation_queues.partial_search_annotation_queue_records_annotation_queues_queue_id_partial_search_post.sync"
)
def test_get_annotation_queue_records_uses_partial_search(
    mock_partial_search: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful partial search response
    mock_get_config.return_value = mock_config
    response = LogRecordsPartialQueryResponse(starting_token=50, limit=25, records=[])
    mock_partial_search.return_value = response
    filter_tree = AndNodeLogRecordsFilter(and_=[])

    # When: getting records from an annotation queue
    records = get_annotation_queue_records(
        " queue-123 ", starting_token=50, limit=25, previous_last_row_id="row-123", filter_tree=filter_tree
    )

    # Then: the generated partial search endpoint receives the expected request body
    assert records is response
    mock_partial_search.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_partial_search.call_args.kwargs["body"]
    assert body.select_columns.column_ids == ["id", "input", "output"]
    assert body.select_columns.include_all_metrics is True
    assert body.select_columns.include_all_feedback is True
    assert body.starting_token == 50
    assert body.limit == 25
    assert body.previous_last_row_id == "row-123"
    assert body.filter_tree is filter_tree
    assert body.truncate_fields is False
    assert body.include_counts is False


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.update_annotation_queue_annotation_queues_queue_id_patch.sync")
def test_update_annotation_queue_sends_expected_request(mock_update: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful update response
    mock_get_config.return_value = mock_config
    mock_update.return_value = make_annotation_queue_response()

    # When: updating an annotation queue name and clearing its description
    queue = update_annotation_queue(" queue-123 ", name=" renamed queue ", description=None)

    # Then: the generated endpoint receives the expected request body
    assert queue.id == "queue-123"
    mock_update.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_update.call_args.kwargs["body"]
    assert body.name.value == "renamed queue"
    assert body.name.append_suffix_if_duplicate is False
    assert body.description is None


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.update_annotation_queue_annotation_queues_queue_id_patch.sync")
def test_update_annotation_queue_can_update_only_description(
    mock_update: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful update response
    mock_get_config.return_value = mock_config
    mock_update.return_value = make_annotation_queue_response()

    # When: updating only the description
    update_annotation_queue("queue-123", description="New description")

    # Then: the name is omitted from the generated request body
    body = mock_update.call_args.kwargs["body"]
    assert body.name is UNSET
    assert body.description == "New description"


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.update_queue_template_annotation_queues_queue_id_templates_template_id_patch.sync")
def test_update_annotation_queue_field_sends_expected_request(
    mock_update: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful update field response
    mock_get_config.return_value = mock_config
    mock_update.return_value = make_annotation_field_response()

    # When: updating an annotation queue field
    field = update_annotation_queue_field(" queue-123 ", " field-123 ", name=" quality ", criteria=None)

    # Then: the generated endpoint receives the expected request body
    assert isinstance(field, AnnotationField)
    assert field.id == "field-123"
    mock_update.assert_called_once_with(queue_id="queue-123", template_id="field-123", client=ANY, body=ANY)
    body = mock_update.call_args.kwargs["body"]
    assert body.name == "quality"
    assert body.criteria is None


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch(
    "galileo.annotation_queues.update_annotation_queue_user_role_annotation_queues_queue_id_users_user_id_patch.sync"
)
def test_update_annotation_queue_user_sends_expected_request(
    mock_update: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful update user response
    mock_get_config.return_value = mock_config
    mock_update.return_value = make_annotation_queue_user_response()

    # When: updating an annotation queue user
    user = update_annotation_queue_user(" queue-123 ", " user-123 ", role=CollaboratorRole.OWNER, track_progress=True)

    # Then: the generated endpoint receives the expected request body
    assert isinstance(user, AnnotationQueueUser)
    assert user.id == "collab-123"
    mock_update.assert_called_once_with(queue_id="queue-123", user_id="user-123", client=ANY, body=ANY)
    body = mock_update.call_args.kwargs["body"]
    assert body.role == CollaboratorRole.OWNER
    assert body.track_progress is True


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.delete_annotation_queue_annotation_queues_queue_id_delete.sync")
def test_delete_annotation_queue_by_id_returns_none(mock_delete: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful delete response
    mock_get_config.return_value = mock_config
    mock_delete.return_value = {"deleted": True}

    # When: deleting an annotation queue by ID
    result = delete_annotation_queue(id=" queue-123 ")

    # Then: the SDK deletes the queue without an extra lookup
    assert result is None
    mock_delete.assert_called_once_with(queue_id="queue-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.delete_annotation_queue_annotation_queues_queue_id_delete.sync")
def test_delete_annotation_queue_by_id_propagates_not_found(
    mock_delete: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the generated delete endpoint raises 404 for a missing queue
    mock_get_config.return_value = mock_config
    mock_delete.side_effect = NotFoundError(404, b"not found")

    # When/Then: deleting a missing queue raises the SDK-level not found error
    with pytest.raises(NotFoundError):
        delete_annotation_queue(id=" queue-123 ")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.delete_annotation_queue_annotation_queues_queue_id_delete.sync")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_delete_annotation_queue_by_name_resolves_then_deletes(
    mock_query: Mock, mock_delete: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful name lookup and delete response
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(annotation_queues=[make_annotation_queue_response()])
    mock_delete.return_value = {"deleted": True}

    # When: deleting an annotation queue by name
    result = delete_annotation_queue(name=" review queue ")

    # Then: the SDK resolves the queue by name and deletes the matching ID
    assert result is None
    mock_query.assert_called_once_with(client=ANY, body=ANY, limit=1)
    mock_delete.assert_called_once_with(queue_id="queue-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.delete_annotation_queue_annotation_queues_queue_id_delete.sync")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_delete_annotation_queue_by_name_raises_not_found_when_missing(
    mock_query: Mock, mock_delete: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the name lookup returns no matching queues
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(annotation_queues=[])

    # When/Then: deleting a missing queue by name raises NotFoundError
    with pytest.raises(NotFoundError, match="Annotation queue missing queue not found"):
        delete_annotation_queue(name=" missing queue ")

    mock_delete.assert_not_called()


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.remove_annotation_queue_user_annotation_queues_queue_id_users_user_id_delete.sync")
def test_remove_annotation_queue_user_returns_none(mock_remove: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful remove user response
    mock_get_config.return_value = mock_config
    mock_remove.return_value = {"deleted": True}

    # When: removing an annotation queue user
    result = remove_annotation_queue_user(" queue-123 ", " user-123 ")

    # Then: the SDK reports success with no return value
    assert result is None
    mock_remove.assert_called_once_with(queue_id="queue-123", user_id="user-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.delete_queue_template_annotation_queues_queue_id_templates_template_id_delete.sync")
def test_delete_annotation_queue_field_returns_none(mock_delete: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful delete field response
    mock_get_config.return_value = mock_config
    mock_delete.return_value = {"deleted": True}

    # When: deleting an annotation queue field
    result = delete_annotation_queue_field(" queue-123 ", " field-123 ")

    # Then: the SDK reports success with no return value
    assert result is None
    mock_delete.assert_called_once_with(queue_id="queue-123", template_id="field-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.get_annotation_queue_annotation_queues_queue_id_get.sync")
def test_get_annotation_queue_by_id_returns_queue(mock_get_queue: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful get response
    mock_get_config.return_value = mock_config
    mock_get_queue.return_value = make_annotation_queue_response()

    # When: retrieving an annotation queue by ID
    queue = get_annotation_queue(id=" queue-123 ")

    # Then: the generated endpoint receives the trimmed queue ID
    assert queue is not None
    assert queue.id == "queue-123"
    mock_get_queue.assert_called_once_with(queue_id="queue-123", client=ANY)


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.get_annotation_queue_annotation_queues_queue_id_get.sync")
def test_get_annotation_queue_by_id_returns_none_when_missing(
    mock_get_queue: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the generated get endpoint raises 404 for a missing queue
    mock_get_config.return_value = mock_config
    mock_get_queue.side_effect = NotFoundError(404, b"not found")

    # When: retrieving a missing annotation queue by ID
    queue = get_annotation_queue(id=" queue-123 ")

    # Then: the SDK returns None like the name lookup path
    assert queue is None


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_get_annotation_queue_by_name_returns_first_match(mock_query: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful query response with one matching queue
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(annotation_queues=[make_annotation_queue_response()])

    # When: retrieving an annotation queue by name
    queue = get_annotation_queue(name=" review queue ")

    # Then: the generated endpoint receives an exact name filter
    assert queue is not None
    assert queue.name == "review queue"
    mock_query.assert_called_once_with(client=ANY, body=ANY, limit=1)
    body = mock_query.call_args.kwargs["body"]
    assert body.filters[0].operator.value == "eq"
    assert body.filters[0].value == "review queue"
    assert body.sort.name == "updated_at"
    assert body.sort.ascending is False


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_get_annotation_queue_by_name_returns_none_when_missing(
    mock_query: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a query response with no matching queues
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(annotation_queues=[])

    # When: retrieving a missing annotation queue by name
    queue = get_annotation_queue(name="missing queue")

    # Then: the SDK returns None
    assert queue is None


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_list_annotation_queues_returns_all_pages(mock_query: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: two pages of annotation queues
    mock_get_config.return_value = mock_config
    second_queue = make_annotation_queue_response()
    second_queue.id = "queue-456"
    mock_query.side_effect = [
        ListAnnotationQueueResponse(
            annotation_queues=[make_annotation_queue_response()], paginated=True, next_starting_token=100
        ),
        ListAnnotationQueueResponse(annotation_queues=[second_queue]),
    ]

    # When: listing annotation queues
    queues = list_annotation_queues(limit=100)

    # Then: the SDK returns queues from each page
    assert [queue.id for queue in queues] == ["queue-123", "queue-456"]
    assert mock_query.call_count == 2
    assert mock_query.call_args_list[0].kwargs["starting_token"] == 0
    assert mock_query.call_args_list[1].kwargs["starting_token"] == 100


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_list_annotation_queues_continues_when_paginated_flag_is_false(
    mock_query: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a response with an advancing next token but no paginated flag
    mock_get_config.return_value = mock_config
    second_queue = make_annotation_queue_response()
    second_queue.id = "queue-456"
    mock_query.side_effect = [
        ListAnnotationQueueResponse(
            annotation_queues=[make_annotation_queue_response()], paginated=False, next_starting_token=100
        ),
        ListAnnotationQueueResponse(annotation_queues=[second_queue]),
    ]

    # When: listing annotation queues
    queues = list_annotation_queues(limit=100)

    # Then: the SDK treats the advancing token as authoritative
    assert [queue.id for queue in queues] == ["queue-123", "queue-456"]
    assert mock_query.call_count == 2
    assert mock_query.call_args_list[1].kwargs["starting_token"] == 100


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_list_annotation_queues_stops_when_next_token_does_not_advance(
    mock_query: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a paginated annotation queue response whose next token repeats
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(
        annotation_queues=[make_annotation_queue_response()], paginated=True, next_starting_token=0
    )

    # When: listing annotation queues
    queues = list_annotation_queues(limit=100)

    # Then: the SDK returns the page and does not loop forever
    assert [queue.id for queue in queues] == ["queue-123"]
    mock_query.assert_called_once_with(client=ANY, body=ANY, starting_token=0, limit=100)


def test_create_annotation_queue_requires_name():
    # Given: a blank queue name
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: creating the queue raises a validation error
    with pytest.raises(ValueError, match="'name' must be provided"):
        queues.create(name=" ")


def test_update_annotation_queue_requires_a_change():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: updating with no fields raises a validation error
    with pytest.raises(ValueError, match="At least one"):
        queues.update(id="queue-123")


def test_add_records_to_annotation_queue_requires_one_selector():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: adding records without a selector raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.add_records(queue_id="queue-123", project_id="project-123", experiment_id="experiment-123")


def test_add_records_to_annotation_queue_rejects_multiple_selectors():
    # Given: an annotation queue client and two selector inputs
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())
    record_selector = AnnotationQueueRecordsByFilterTree(filter_tree=AndNodeLogRecordsFilter(and_=[]))

    # When/Then: adding records with both selector styles raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.add_records(
            queue_id="queue-123",
            project_id="project-123",
            experiment_id="experiment-123",
            record_ids=["record-1"],
            record_selector=record_selector,
        )


def test_add_records_to_annotation_queue_requires_one_run_source():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: adding records without a log stream or experiment ID raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.add_records(queue_id="queue-123", project_id="project-123", record_ids=["record-1"])


def test_remove_records_from_annotation_queue_rejects_empty_record_ids():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: removing records with an empty record ID raises a validation error
    with pytest.raises(ValueError, match="'record_ids' must contain"):
        queues.remove_records(queue_id="queue-123", record_ids=[" "])


def test_get_annotation_queue_records_requires_queue_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: getting records with a blank queue ID raises a validation error
    with pytest.raises(ValueError, match="'queue_id' must be provided"):
        queues.get_records(queue_id=" ")


def test_create_annotation_queue_field_requires_name():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: creating a field with a blank name raises a validation error
    with pytest.raises(ValueError, match="'name' must be provided"):
        queues.create_field(
            queue_id="queue-123", name=" ", constraints=LikeDislikeConstraints(annotation_type="like_dislike")
        )


def test_update_annotation_queue_field_requires_field_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: updating a field with a blank field ID raises a validation error
    with pytest.raises(ValueError, match="'field_id' must be provided"):
        queues.update_field(queue_id="queue-123", field_id=" ", name="quality", criteria=None)


def test_list_annotation_queue_fields_requires_queue_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: listing fields with a blank queue ID raises a validation error
    with pytest.raises(ValueError, match="'queue_id' must be provided"):
        queues.list_fields(queue_id=" ")


def test_share_annotation_queue_requires_exactly_one_user_identifier():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: sharing with no user identifier raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.share(queue_id="queue-123")

    # When/Then: sharing with both user identifiers raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.share(queue_id="queue-123", user_id="user-123", user_email="ada@example.com")


def test_remove_annotation_queue_user_requires_user_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: removing with a blank user ID raises a validation error
    with pytest.raises(ValueError, match="'user_id' must be provided"):
        queues.remove_user(queue_id="queue-123", user_id=" ")


def test_get_annotation_queue_requires_exactly_one_identifier():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: getting with no identifier raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.get()

    # When/Then: getting with both identifiers raises a validation error
    with pytest.raises(ValueError, match="Exactly one"):
        queues.get(id="queue-123", name="review queue")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.create_annotation_queue_annotation_queues_post.sync")
def test_create_annotation_queue_raises_for_http_validation_error(
    mock_create: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_create.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["body", "name"], msg="Name already exists", type_="value_error")]
    )

    # When/Then: creating the queue raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Name already exists"):
        create_annotation_queue(name="review queue")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.create_queue_template_annotation_queues_queue_id_templates_post.sync")
def test_create_annotation_queue_field_raises_for_http_validation_error(
    mock_create: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_create.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["body", "template", "name"], msg="Name already exists", type_="value_error")]
    )

    # When/Then: creating the field raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Name already exists"):
        create_annotation_queue_field(
            queue_id="queue-123", name="quality", constraints=LikeDislikeConstraints(annotation_type="like_dislike")
        )


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.share_annotation_queue_with_users_annotation_queues_queue_id_users_post.sync")
def test_share_annotation_queue_raises_for_http_validation_error(
    mock_share: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_share.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["body", "user_email"], msg="Invalid email", type_="value_error")]
    )

    # When/Then: sharing the queue raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid email"):
        share_annotation_queue(queue_id="queue-123", user_email="bad-email")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.get_queue_templates_annotation_queues_queue_id_templates_get.sync")
def test_list_annotation_queue_fields_raises_for_http_validation_error(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_list.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["path", "queue_id"], msg="Invalid queue", type_="value_error")]
    )

    # When/Then: listing fields raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid queue"):
        list_annotation_queue_fields("queue-123")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.query_annotation_queues_annotation_queues_query_post.sync")
def test_list_annotation_queues_raises_for_http_validation_error(
    mock_query: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_query.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["query", "limit"], msg="Invalid limit", type_="value_error")]
    )

    # When/Then: listing queues raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid limit"):
        list_annotation_queues()


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.list_annotation_queue_users_annotation_queues_queue_id_users_get.sync")
def test_list_annotation_queue_users_raises_for_http_validation_error(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_list.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["query", "limit"], msg="Invalid limit", type_="value_error")]
    )

    # When/Then: listing queue users raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid limit"):
        list_annotation_queue_users("queue-123")


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch(
    "galileo.annotation_queues.partial_search_annotation_queue_records_annotation_queues_queue_id_partial_search_post.sync"
)
def test_get_annotation_queue_records_raises_for_http_validation_error(
    mock_partial_search: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_partial_search.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["query", "limit"], msg="Invalid limit", type_="value_error")]
    )

    # When/Then: getting queue records raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid limit"):
        get_annotation_queue_records("queue-123")
