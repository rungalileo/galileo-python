from datetime import UTC, datetime
from unittest.mock import ANY, Mock, patch

import pytest

from galileo.annotation_queues import (
    AnnotationQueue,
    AnnotationQueues,
    AnnotationQueuesAPIException,
    AnnotationQueueUser,
    AnnotationTemplate,
    create_annotation_queue,
    create_annotation_queue_template,
    delete_annotation_queue,
    delete_annotation_queue_template,
    get_annotation_queue,
    list_annotation_queue_templates,
    list_annotation_queue_users,
    list_annotation_queues,
    remove_annotation_queue_user,
    share_annotation_queue,
    update_annotation_queue,
    update_annotation_queue_template,
    update_annotation_queue_user,
)
from galileo.resources.models.annotation_queue_response import AnnotationQueueResponse
from galileo.resources.models.annotation_template_db import AnnotationTemplateDB
from galileo.resources.models.collaborator_role import CollaboratorRole
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.like_dislike_constraints import LikeDislikeConstraints
from galileo.resources.models.list_annotation_queue_collaborators_response import (
    ListAnnotationQueueCollaboratorsResponse,
)
from galileo.resources.models.list_annotation_queue_response import ListAnnotationQueueResponse
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
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        updated_at=datetime(2026, 1, 2, tzinfo=UTC),
        created_by_user=None,
    )


def make_annotation_template_response() -> AnnotationTemplateDB:
    return AnnotationTemplateDB(
        id="template-123",
        name="quality",
        include_explanation=True,
        constraints=LikeDislikeConstraints(annotation_type="like_dislike"),
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        created_by=None,
        position=1,
        usage_count=0,
        criteria="Check quality",
    )


def make_annotation_queue_user_response() -> UserAnnotationQueueCollaborator:
    return UserAnnotationQueueCollaborator(
        id="collab-123",
        role=CollaboratorRole.ANNOTATOR,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
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
        copy_templates_from_queue_id="template-source",
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
    assert body.copy_templates_from_queue_id == "template-source"


def test_annotation_queue_wraps_templates():
    # Given: an annotation queue response with generated template models
    response = make_annotation_queue_response()
    response.templates = [make_annotation_template_response()]

    # When: wrapping the response in an SDK annotation queue
    queue = AnnotationQueue(response)

    # Then: templates are exposed as SDK annotation template objects
    assert isinstance(queue.templates[0], AnnotationTemplate)
    assert queue.templates[0].id == "template-123"


def test_annotation_template_converts_tree_choice_db_constraints():
    # Given: a generated template response with response-only tree choice constraints
    response = make_annotation_template_response()
    response.constraints = TreeChoiceDBConstraints(
        annotation_type="tree_choice",
        choices_tree=[TreeChoiceNode(label="Helpful", id="helpful")],
        choices_tree_yaml="- id: helpful\n  label: Helpful",
    )

    # When: wrapping the response in an SDK annotation template
    template = AnnotationTemplate(response)

    # Then: constraints are exposed with the public tree choice type
    assert isinstance(template.constraints, TreeChoiceConstraints)
    assert template.constraints.choices_tree_yaml == "- id: helpful\n  label: Helpful"


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
@patch("galileo.annotation_queues.create_queue_template_annotation_queues_queue_id_templates_post.sync")
def test_create_annotation_queue_template_sends_expected_request(
    mock_create: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful create template response
    mock_get_config.return_value = mock_config
    mock_create.return_value = [make_annotation_template_response()]
    constraints = LikeDislikeConstraints(annotation_type="like_dislike")

    # When: creating an annotation queue template
    template = create_annotation_queue_template(
        " queue-123 ", name=" quality ", constraints=constraints, include_explanation=True, criteria="Check quality"
    )

    # Then: the generated endpoint receives the expected request body
    assert isinstance(template, AnnotationTemplate)
    assert template.id == "template-123"
    mock_create.assert_called_once_with(queue_id="queue-123", client=ANY, body=ANY)
    body = mock_create.call_args.kwargs["body"]
    assert body.template.name == "quality"
    assert body.template.constraints is constraints
    assert body.template.include_explanation is True
    assert body.template.criteria == "Check quality"


@patch("galileo.annotation_queues.GalileoPythonConfig.get")
@patch("galileo.annotation_queues.get_queue_templates_annotation_queues_queue_id_templates_get.sync")
def test_list_annotation_queue_templates_returns_templates(mock_list: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful list templates response
    mock_get_config.return_value = mock_config
    mock_list.return_value = [make_annotation_template_response()]

    # When: listing annotation queue templates
    templates = list_annotation_queue_templates(" queue-123 ")

    # Then: templates are exposed as SDK annotation template objects
    assert len(templates) == 1
    assert isinstance(templates[0], AnnotationTemplate)
    assert templates[0].id == "template-123"
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
def test_update_annotation_queue_template_sends_expected_request(
    mock_update: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful update template response
    mock_get_config.return_value = mock_config
    mock_update.return_value = make_annotation_template_response()

    # When: updating an annotation queue template
    template = update_annotation_queue_template(" queue-123 ", " template-123 ", name=" quality ", criteria=None)

    # Then: the generated endpoint receives the expected request body
    assert isinstance(template, AnnotationTemplate)
    assert template.id == "template-123"
    mock_update.assert_called_once_with(queue_id="queue-123", template_id="template-123", client=ANY, body=ANY)
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
@patch("galileo.annotation_queues.get_annotation_queue_annotation_queues_queue_id_get.sync")
def test_delete_annotation_queue_by_id_returns_none(
    mock_get_queue: Mock, mock_delete: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: a successful get and delete response
    mock_get_config.return_value = mock_config
    mock_get_queue.return_value = make_annotation_queue_response()
    mock_delete.return_value = {"deleted": True}

    # When: deleting an annotation queue by ID
    result = delete_annotation_queue(id=" queue-123 ")

    # Then: the SDK resolves the queue and deletes it
    assert result is None
    mock_get_queue.assert_called_once_with(queue_id="queue-123", client=ANY)
    mock_delete.assert_called_once_with(queue_id="queue-123", client=ANY)


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
def test_delete_annotation_queue_template_returns_none(mock_delete: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a successful delete template response
    mock_get_config.return_value = mock_config
    mock_delete.return_value = {"deleted": True}

    # When: deleting an annotation queue template
    result = delete_annotation_queue_template(" queue-123 ", " template-123 ")

    # Then: the SDK reports success with no return value
    assert result is None
    mock_delete.assert_called_once_with(queue_id="queue-123", template_id="template-123", client=ANY)


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
def test_list_annotation_queues_returns_one_page(mock_query: Mock, mock_get_config: Mock, mock_config: Mock):
    # Given: a paginated annotation queue response
    mock_get_config.return_value = mock_config
    mock_query.return_value = ListAnnotationQueueResponse(
        annotation_queues=[make_annotation_queue_response()], paginated=True, next_starting_token=100
    )

    # When: listing annotation queues
    queues = list_annotation_queues(limit=100)

    # Then: the SDK returns only the requested page
    assert [queue.id for queue in queues] == ["queue-123"]
    mock_query.assert_called_once_with(client=ANY, body=ANY, limit=100)


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


def test_create_annotation_queue_template_requires_name():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: creating a template with a blank name raises a validation error
    with pytest.raises(ValueError, match="'name' must be provided"):
        queues.create_template(
            queue_id="queue-123", name=" ", constraints=LikeDislikeConstraints(annotation_type="like_dislike")
        )


def test_update_annotation_queue_template_requires_template_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: updating a template with a blank template ID raises a validation error
    with pytest.raises(ValueError, match="'template_id' must be provided"):
        queues.update_template(queue_id="queue-123", template_id=" ", name="quality", criteria=None)


def test_list_annotation_queue_templates_requires_queue_id():
    # Given: an annotation queue client
    queues = AnnotationQueues.__new__(AnnotationQueues)
    queues.config = Mock(api_client=Mock())

    # When/Then: listing templates with a blank queue ID raises a validation error
    with pytest.raises(ValueError, match="'queue_id' must be provided"):
        queues.list_templates(queue_id=" ")


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
def test_create_annotation_queue_template_raises_for_http_validation_error(
    mock_create: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_create.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["body", "template", "name"], msg="Name already exists", type_="value_error")]
    )

    # When/Then: creating the template raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Name already exists"):
        create_annotation_queue_template(
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
def test_list_annotation_queue_templates_raises_for_http_validation_error(
    mock_list: Mock, mock_get_config: Mock, mock_config: Mock
):
    # Given: the API returns an HTTP validation error
    mock_get_config.return_value = mock_config
    mock_list.return_value = HTTPValidationError(
        detail=[ValidationError(loc=["path", "queue_id"], msg="Invalid queue", type_="value_error")]
    )

    # When/Then: listing templates raises an SDK API exception
    with pytest.raises(AnnotationQueuesAPIException, match="Invalid queue"):
        list_annotation_queue_templates("queue-123")


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
