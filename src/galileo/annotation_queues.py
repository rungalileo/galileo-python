from __future__ import annotations

import builtins
import datetime
from typing import TypeAlias, cast, overload

from galileo.config import GalileoPythonConfig
from galileo.exceptions import NotFoundError
from galileo.resources.api.annotation_queue import (
    create_annotation_queue_annotation_queues_post,
    create_queue_template_annotation_queues_queue_id_templates_post,
    delete_annotation_queue_annotation_queues_queue_id_delete,
    delete_queue_template_annotation_queues_queue_id_templates_template_id_delete,
    get_annotation_queue_annotation_queues_queue_id_get,
    get_queue_templates_annotation_queues_queue_id_templates_get,
    list_annotation_queue_users_annotation_queues_queue_id_users_get,
    query_annotation_queues_annotation_queues_query_post,
    remove_annotation_queue_user_annotation_queues_queue_id_users_user_id_delete,
    share_annotation_queue_with_users_annotation_queues_queue_id_users_post,
    update_annotation_queue_annotation_queues_queue_id_patch,
    update_annotation_queue_user_role_annotation_queues_queue_id_users_user_id_patch,
    update_queue_template_annotation_queues_queue_id_templates_template_id_patch,
)
from galileo.resources.api.annotation_queue_records import (
    add_records_to_annotation_queue_annotation_queues_queue_id_records_post,
    remove_records_from_annotation_queue_annotation_queues_queue_id_records_remove_post,
)
from galileo.resources.models.add_records_to_queue_request import AddRecordsToQueueRequest
from galileo.resources.models.add_records_to_queue_response import AddRecordsToQueueResponse
from galileo.resources.models.annotation_queue_name_filter import AnnotationQueueNameFilter
from galileo.resources.models.annotation_queue_name_filter_operator import AnnotationQueueNameFilterOperator
from galileo.resources.models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
from galileo.resources.models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs
from galileo.resources.models.annotation_queue_response import AnnotationQueueResponse
from galileo.resources.models.annotation_queue_updated_at_sort import AnnotationQueueUpdatedAtSort
from galileo.resources.models.annotation_queue_user_collaborator_create import AnnotationQueueUserCollaboratorCreate
from galileo.resources.models.annotation_queue_user_collaborator_update import AnnotationQueueUserCollaboratorUpdate
from galileo.resources.models.annotation_template_create import AnnotationTemplateCreate
from galileo.resources.models.annotation_template_db import AnnotationTemplateDB
from galileo.resources.models.annotation_template_update import AnnotationTemplateUpdate
from galileo.resources.models.choice_constraints import ChoiceConstraints
from galileo.resources.models.collaborator_role import CollaboratorRole
from galileo.resources.models.create_annotation_queue_request import CreateAnnotationQueueRequest
from galileo.resources.models.create_queue_template_request import CreateQueueTemplateRequest
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.like_dislike_constraints import LikeDislikeConstraints
from galileo.resources.models.list_annotation_queue_collaborators_response import (
    ListAnnotationQueueCollaboratorsResponse,
)
from galileo.resources.models.list_annotation_queue_params import ListAnnotationQueueParams
from galileo.resources.models.list_annotation_queue_response import ListAnnotationQueueResponse
from galileo.resources.models.name import Name
from galileo.resources.models.permission import Permission
from galileo.resources.models.remove_records_from_queue_request import RemoveRecordsFromQueueRequest
from galileo.resources.models.remove_records_from_queue_response import RemoveRecordsFromQueueResponse
from galileo.resources.models.score_constraints import ScoreConstraints
from galileo.resources.models.star_constraints import StarConstraints
from galileo.resources.models.tags_constraints import TagsConstraints
from galileo.resources.models.text_constraints import TextConstraints
from galileo.resources.models.tree_choice_constraints import TreeChoiceConstraints
from galileo.resources.models.tree_choice_db_constraints import TreeChoiceDBConstraints
from galileo.resources.models.update_annotation_queue_request import UpdateAnnotationQueueRequest
from galileo.resources.models.user_annotation_queue_collaborator import UserAnnotationQueueCollaborator
from galileo.resources.models.user_info import UserInfo
from galileo.resources.types import UNSET, Unset
from galileo.utils.exceptions import APIException


class AnnotationQueuesAPIException(APIException):
    pass


AnnotationTemplateConstraints: TypeAlias = (
    ChoiceConstraints
    | LikeDislikeConstraints
    | ScoreConstraints
    | StarConstraints
    | TagsConstraints
    | TextConstraints
    | TreeChoiceConstraints
)
_AnnotationTemplateResponseConstraints: TypeAlias = AnnotationTemplateConstraints | TreeChoiceDBConstraints
AnnotationQueueRecordSelector: TypeAlias = AnnotationQueueRecordsByRecordIDs | AnnotationQueueRecordsByFilterTree


class AnnotationTemplate:
    """Represents an annotation template in an annotation queue."""

    id: str
    name: str
    include_explanation: bool
    constraints: AnnotationTemplateConstraints
    created_at: datetime.datetime
    created_by: str | None
    position: int
    usage_count: int
    criteria: str | None | Unset

    def __init__(self, template: AnnotationTemplateDB) -> None:
        self.id = template.id
        self.name = template.name
        self.include_explanation = template.include_explanation
        self.constraints = _to_annotation_template_constraints(template.constraints)
        self.created_at = template.created_at
        self.created_by = template.created_by
        self.position = template.position
        self.usage_count = template.usage_count
        self.criteria = template.criteria


class AnnotationQueueUser:
    """Represents a user with access to an annotation queue."""

    id: str
    user_id: str
    annotation_queue_id: str
    role: CollaboratorRole
    created_at: datetime.datetime
    first_name: str | None
    last_name: str | None
    email: str
    permissions: Unset | list[Permission]
    track_progress: Unset | bool
    progress: None | Unset | float

    def __init__(self, collaborator: UserAnnotationQueueCollaborator) -> None:
        self.id = collaborator.id
        self.user_id = collaborator.user_id
        self.annotation_queue_id = collaborator.annotation_queue_id
        self.role = collaborator.role
        self.created_at = collaborator.created_at
        self.first_name = collaborator.first_name
        self.last_name = collaborator.last_name
        self.email = collaborator.email
        self.permissions = collaborator.permissions
        self.track_progress = collaborator.track_progress
        self.progress = collaborator.progress


class AnnotationQueue:
    """
    Represents an annotation queue in the Galileo platform.

    Annotation queues are organization-level resources used to assign log records
    to annotators and track annotation progress.
    """

    id: str
    name: str
    description: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by_user: UserInfo | None
    permissions: Unset | list[Permission]
    num_log_records: Unset | int
    num_annotators: Unset | int
    num_users: Unset | int
    num_templates: Unset | int
    overall_progress: None | Unset | float
    templates: Unset | list[AnnotationTemplate]

    def __init__(self, queue: AnnotationQueueResponse) -> None:
        self.id = queue.id
        self.name = queue.name
        self.description = queue.description
        self.created_at = queue.created_at
        self.updated_at = queue.updated_at
        self.created_by_user = queue.created_by_user
        self.permissions = queue.permissions
        self.num_log_records = queue.num_log_records
        self.num_annotators = queue.num_annotators
        self.num_users = queue.num_users
        self.num_templates = queue.num_templates
        self.overall_progress = queue.overall_progress
        self.templates = (
            UNSET
            if isinstance(queue.templates, Unset)
            else [AnnotationTemplate(template=template) for template in queue.templates]
        )


class AnnotationQueues:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(self, limit: Unset | int = 100) -> list[AnnotationQueue]:
        """
        List annotation queues.

        Parameters
        ----------
        limit : Union[Unset, int]
            The maximum number of annotation queues to return. Default is 100.

        Returns
        -------
        list[AnnotationQueue]
            A list of annotation queues.
        """
        response = query_annotation_queues_annotation_queues_query_post.sync(
            client=self.config.api_client, body=ListAnnotationQueueParams(), limit=limit
        )
        list_response = _to_annotation_queue_list(response)
        return [AnnotationQueue(queue=queue) for queue in list_response.annotation_queues]

    def list_users(self, queue_id: str) -> builtins.list[AnnotationQueueUser]:
        """
        List users who have access to an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.

        Returns
        -------
        list[AnnotationQueueUser]
            A list of annotation queue users.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        users: builtins.list[AnnotationQueueUser] = []
        starting_token: int | None = 0

        while starting_token is not None:
            response = list_annotation_queue_users_annotation_queues_queue_id_users_get.sync(
                queue_id=queue_id, client=self.config.api_client, starting_token=starting_token
            )
            list_response = _to_annotation_queue_user_list(response)
            users.extend(AnnotationQueueUser(collaborator=collaborator) for collaborator in list_response.collaborators)

            if list_response.paginated and list_response.next_starting_token is not None:
                starting_token = list_response.next_starting_token
            else:
                starting_token = None

        return users

    def list_templates(self, queue_id: str) -> builtins.list[AnnotationTemplate]:
        """
        List templates for an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.

        Returns
        -------
        list[AnnotationTemplate]
            A list of annotation templates.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        response = get_queue_templates_annotation_queues_queue_id_templates_get.sync(
            queue_id=queue_id, client=self.config.api_client
        )
        return _to_annotation_template_list(response, "list")

    @overload
    def get(self, *, id: str) -> AnnotationQueue | None: ...

    @overload
    def get(self, *, name: str) -> AnnotationQueue | None: ...

    def get(self, *, id: str | None = None, name: str | None = None) -> AnnotationQueue | None:
        """
        Retrieves an annotation queue by id or name.

        Exactly one of `id` or `name` must be provided.

        Parameters
        ----------
        id : str
            The id of the annotation queue.
        name : str
            The name of the annotation queue.

        Returns
        -------
        AnnotationQueue | None
            The annotation queue, or None if the API returns no matching queue.
        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if id is not None:
            id = id.strip()
            if not id:
                raise ValueError("'id' must be provided.")

            try:
                response = get_annotation_queue_annotation_queues_queue_id_get.sync(
                    queue_id=id, client=self.config.api_client
                )
            except NotFoundError:
                return None
            if response is None:
                return None
            return _to_annotation_queue(response, "get")

        assert name is not None
        name = name.strip()
        if not name:
            raise ValueError("'name' must be provided.")

        filter = AnnotationQueueNameFilter(operator=AnnotationQueueNameFilterOperator.EQ, value=name)
        params = ListAnnotationQueueParams(filters=[filter], sort=AnnotationQueueUpdatedAtSort(ascending=False))
        response = query_annotation_queues_annotation_queues_query_post.sync(
            client=self.config.api_client, body=params, limit=1
        )
        list_response = _to_annotation_queue_list(response)
        if not list_response.annotation_queues:
            return None

        return AnnotationQueue(queue=list_response.annotation_queues[0])

    def create(
        self,
        name: str,
        description: str | None = None,
        annotator_emails: builtins.list[str] | None = None,
        copy_templates_from_queue_id: str | None = None,
    ) -> AnnotationQueue:
        """
        Create an annotation queue.

        Parameters
        ----------
        name : str
            The name of the annotation queue.
        description : str | None
            Optional annotation queue description.
        annotator_emails : list[str] | None
            Optional annotator emails to invite or assign.
        copy_templates_from_queue_id : str | None
            Optional annotation queue ID to copy templates from.

        Returns
        -------
        AnnotationQueue
            The created annotation queue.
        """
        name = name.strip()
        if not name:
            raise ValueError("'name' must be provided.")

        body = CreateAnnotationQueueRequest(
            name=Name(value=name),
            description=description if description is not None else UNSET,
            annotator_emails=annotator_emails if annotator_emails is not None else UNSET,
            copy_templates_from_queue_id=copy_templates_from_queue_id
            if copy_templates_from_queue_id is not None
            else UNSET,
        )

        response = create_annotation_queue_annotation_queues_post.sync(client=self.config.api_client, body=body)
        return _to_annotation_queue(response, "create")

    def add_records(
        self,
        queue_id: str,
        *,
        project_id: str,
        log_stream_id: str | None = None,
        experiment_id: str | None = None,
        record_ids: builtins.list[str] | None = None,
        record_selector: AnnotationQueueRecordSelector | None = None,
    ) -> int:
        """
        Add records to an annotation queue.

        Exactly one of `record_ids` or `record_selector` must be provided.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        project_id : str
            The ID of the project containing the records.
        log_stream_id : str | None
            The ID of the log stream containing the records.
        experiment_id : str | None
            The ID of the experiment containing the records.
        record_ids : list[str] | None
            Optional list of record IDs to add.
        record_selector : AnnotationQueueRecordSelector | None
            Optional generated selector for adding records by record IDs or filter tree.

        Returns
        -------
        int
            The number of records added to the queue.
        """
        queue_id = _validate_required_string("queue_id", queue_id)
        project_id = _validate_required_string("project_id", project_id)
        run_id = _to_annotation_queue_run_id(log_stream_id=log_stream_id, experiment_id=experiment_id)
        selector = _to_annotation_queue_record_selector(record_ids=record_ids, record_selector=record_selector)

        body = AddRecordsToQueueRequest(project_id=project_id, run_id=run_id, record_selector=selector)
        response = add_records_to_annotation_queue_annotation_queues_queue_id_records_post.sync(
            queue_id=queue_id, client=self.config.api_client, body=body
        )
        return _to_add_records_response(response)

    def remove_records(
        self,
        queue_id: str,
        *,
        record_ids: builtins.list[str] | None = None,
        record_selector: AnnotationQueueRecordSelector | None = None,
    ) -> int:
        """
        Remove records from an annotation queue.

        Exactly one of `record_ids` or `record_selector` must be provided.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        record_ids : list[str] | None
            Optional list of record IDs to remove.
        record_selector : AnnotationQueueRecordSelector | None
            Optional generated selector for removing records by record IDs or filter tree.

        Returns
        -------
        int
            The number of records removed from the queue.
        """
        queue_id = _validate_required_string("queue_id", queue_id)
        selector = _to_annotation_queue_record_selector(record_ids=record_ids, record_selector=record_selector)

        body = RemoveRecordsFromQueueRequest(record_selector=selector)
        response = remove_records_from_annotation_queue_annotation_queues_queue_id_records_remove_post.sync(
            queue_id=queue_id, client=self.config.api_client, body=body
        )
        return _to_remove_records_response(response)

    def share(
        self,
        queue_id: str,
        *,
        user_id: str | None = None,
        user_email: str | None = None,
        role: CollaboratorRole = CollaboratorRole.ANNOTATOR,
        track_progress: bool = True,
    ) -> AnnotationQueueUser:
        """
        Share an annotation queue with a user.

        Exactly one of `user_id` or `user_email` must be provided.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        user_id : str | None
            The ID of the user to share with.
        user_email : str | None
            The email of the user to share with.
        role : CollaboratorRole
            The role to grant. Default is CollaboratorRole.ANNOTATOR.
        track_progress : bool
            Whether to track annotation progress for the user.

        Returns
        -------
        AnnotationQueueUser
            The created annotation queue user.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        if (user_id is None) == (user_email is None):
            raise ValueError("Exactly one of 'user_id' or 'user_email' must be provided")

        if user_id is not None:
            user_id = user_id.strip()
            if not user_id:
                raise ValueError("'user_id' must be provided.")

        if user_email is not None:
            user_email = user_email.strip()
            if not user_email:
                raise ValueError("'user_email' must be provided.")

        body = [
            AnnotationQueueUserCollaboratorCreate(
                user_id=user_id if user_id is not None else UNSET,
                user_email=user_email if user_email is not None else UNSET,
                role=role,
                track_progress=track_progress,
            )
        ]
        response = share_annotation_queue_with_users_annotation_queues_queue_id_users_post.sync(
            queue_id=queue_id, client=self.config.api_client, body=body
        )
        return _to_annotation_queue_user_create_response(response)

    def create_template(
        self,
        queue_id: str,
        *,
        name: str,
        constraints: AnnotationTemplateConstraints,
        include_explanation: bool = False,
        criteria: str | None | Unset = UNSET,
    ) -> AnnotationTemplate:
        """
        Create a template in an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        name : str
            The name of the annotation template.
        constraints : AnnotationTemplateConstraints
            The annotation template constraints.
        include_explanation : bool
            Whether annotators should include explanations.
        criteria : str | None | Unset
            Optional annotation criteria. Pass None to clear it; omit to leave unset.

        Returns
        -------
        AnnotationTemplate
            The created annotation template.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        name = name.strip()
        if not name:
            raise ValueError("'name' must be provided.")

        body = CreateQueueTemplateRequest(
            template=AnnotationTemplateCreate(
                name=name, constraints=constraints, include_explanation=include_explanation, criteria=criteria
            )
        )
        response = create_queue_template_annotation_queues_queue_id_templates_post.sync(
            queue_id=queue_id, client=self.config.api_client, body=body
        )
        return _to_annotation_template_create_response(response)

    def update(self, id: str, *, name: str | None = None, description: str | None | Unset = UNSET) -> AnnotationQueue:
        """
        Update an annotation queue.

        Parameters
        ----------
        id : str
            The ID of the annotation queue.
        name : str | None
            Optional new queue name. Omit to leave unchanged.
        description : str | None | Unset
            Optional new description. Pass None to clear it; omit to leave unchanged.

        Returns
        -------
        AnnotationQueue
            The updated annotation queue.
        """
        id = id.strip()
        if not id:
            raise ValueError("'id' must be provided.")

        name_value: Name | None | Unset
        if name is None:
            name_value = UNSET
        else:
            name = name.strip()
            if not name:
                raise ValueError("'name' must not be empty.")
            name_value = Name(value=name)

        if isinstance(name_value, Unset) and isinstance(description, Unset):
            raise ValueError("At least one of 'name' or 'description' must be provided.")

        body = UpdateAnnotationQueueRequest(name=name_value, description=description)
        response = update_annotation_queue_annotation_queues_queue_id_patch.sync(
            queue_id=id, client=self.config.api_client, body=body
        )
        return _to_annotation_queue(response, "update")

    def update_user(
        self, queue_id: str, user_id: str, *, role: CollaboratorRole, track_progress: bool | None | Unset = UNSET
    ) -> AnnotationQueueUser:
        """
        Update a user's role for an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        user_id : str
            The ID of the user.
        role : CollaboratorRole
            The new role for the user.
        track_progress : bool | None | Unset
            Optional progress tracking value.

        Returns
        -------
        AnnotationQueueUser
            The updated annotation queue user.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        user_id = user_id.strip()
        if not user_id:
            raise ValueError("'user_id' must be provided.")

        body = AnnotationQueueUserCollaboratorUpdate(role=role, track_progress=track_progress)
        response = update_annotation_queue_user_role_annotation_queues_queue_id_users_user_id_patch.sync(
            queue_id=queue_id, user_id=user_id, client=self.config.api_client, body=body
        )
        return _to_annotation_queue_user(response, "update")

    def update_template(
        self, queue_id: str, template_id: str, *, name: str, criteria: str | None
    ) -> AnnotationTemplate:
        """
        Update a template in an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        template_id : str
            The ID of the annotation template.
        name : str
            The new name for the annotation template.
        criteria : str | None
            The new criteria for the annotation template.

        Returns
        -------
        AnnotationTemplate
            The updated annotation template.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        template_id = template_id.strip()
        if not template_id:
            raise ValueError("'template_id' must be provided.")

        name = name.strip()
        if not name:
            raise ValueError("'name' must be provided.")

        body = AnnotationTemplateUpdate(name=name, criteria=criteria)
        response = update_queue_template_annotation_queues_queue_id_templates_template_id_patch.sync(
            queue_id=queue_id, template_id=template_id, client=self.config.api_client, body=body
        )
        return _to_annotation_template(response, "update")

    @overload
    def delete(self, *, id: str) -> None: ...

    @overload
    def delete(self, *, name: str) -> None: ...

    def delete(self, *, id: str | None = None, name: str | None = None) -> None:
        """
        Delete an annotation queue by id or name.

        Parameters
        ----------
        id : str
            The ID of the annotation queue.
        name : str
            The name of the annotation queue.
        """
        queue = self.get(id=id, name=name)  # type: ignore[call-overload]
        if not queue:
            queue_identifier = (name or id or "").strip()
            raise ValueError(f"Annotation queue {queue_identifier} not found")

        response = delete_annotation_queue_annotation_queues_queue_id_delete.sync(
            queue_id=queue.id, client=self.config.api_client
        )
        if isinstance(response, HTTPValidationError):
            raise AnnotationQueuesAPIException(
                f"Failed to delete annotation queue: {_format_validation_error(response)}"
            )
        if response is None:
            raise AnnotationQueuesAPIException(f"Failed to delete annotation queue: {queue.id}")
        return

    def remove_user(self, queue_id: str, user_id: str) -> None:
        """
        Remove a user's access to an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        user_id : str
            The ID of the user to remove.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        user_id = user_id.strip()
        if not user_id:
            raise ValueError("'user_id' must be provided.")

        response = remove_annotation_queue_user_annotation_queues_queue_id_users_user_id_delete.sync(
            queue_id=queue_id, user_id=user_id, client=self.config.api_client
        )
        if isinstance(response, HTTPValidationError):
            raise AnnotationQueuesAPIException(
                f"Failed to remove annotation queue user: {_format_validation_error(response)}"
            )
        if response is None:
            raise AnnotationQueuesAPIException(f"Failed to remove annotation queue user: {user_id}")
        return

    def delete_template(self, queue_id: str, template_id: str) -> None:
        """
        Delete a template from an annotation queue.

        Parameters
        ----------
        queue_id : str
            The ID of the annotation queue.
        template_id : str
            The ID of the annotation template.
        """
        queue_id = queue_id.strip()
        if not queue_id:
            raise ValueError("'queue_id' must be provided.")

        template_id = template_id.strip()
        if not template_id:
            raise ValueError("'template_id' must be provided.")

        response = delete_queue_template_annotation_queues_queue_id_templates_template_id_delete.sync(
            queue_id=queue_id, template_id=template_id, client=self.config.api_client
        )
        if isinstance(response, HTTPValidationError):
            raise AnnotationQueuesAPIException(
                f"Failed to delete annotation queue template: {_format_validation_error(response)}"
            )
        if response is None:
            raise AnnotationQueuesAPIException(f"Failed to delete annotation queue template: {template_id}")
        return


def create_annotation_queue(
    name: str,
    description: str | None = None,
    annotator_emails: list[str] | None = None,
    copy_templates_from_queue_id: str | None = None,
) -> AnnotationQueue:
    """Create an annotation queue."""
    queues = AnnotationQueues()
    return queues.create(
        name=name,
        description=description,
        annotator_emails=annotator_emails,
        copy_templates_from_queue_id=copy_templates_from_queue_id,
    )


def create_annotation_queue_template(
    queue_id: str,
    *,
    name: str,
    constraints: AnnotationTemplateConstraints,
    include_explanation: bool = False,
    criteria: str | None | Unset = UNSET,
) -> AnnotationTemplate:
    """Create a template in an annotation queue."""
    queues = AnnotationQueues()
    return queues.create_template(
        queue_id=queue_id,
        name=name,
        constraints=constraints,
        include_explanation=include_explanation,
        criteria=criteria,
    )


def share_annotation_queue(
    queue_id: str,
    *,
    user_id: str | None = None,
    user_email: str | None = None,
    role: CollaboratorRole = CollaboratorRole.ANNOTATOR,
    track_progress: bool = True,
) -> AnnotationQueueUser:
    """Share an annotation queue with a user."""
    queues = AnnotationQueues()
    return queues.share(
        queue_id=queue_id, user_id=user_id, user_email=user_email, role=role, track_progress=track_progress
    )


def add_records_to_annotation_queue(
    queue_id: str,
    *,
    project_id: str,
    log_stream_id: str | None = None,
    experiment_id: str | None = None,
    record_ids: list[str] | None = None,
    record_selector: AnnotationQueueRecordSelector | None = None,
) -> int:
    """Add records to an annotation queue."""
    queues = AnnotationQueues()
    return queues.add_records(
        queue_id=queue_id,
        project_id=project_id,
        log_stream_id=log_stream_id,
        experiment_id=experiment_id,
        record_ids=record_ids,
        record_selector=record_selector,
    )


def remove_records_from_annotation_queue(
    queue_id: str, *, record_ids: list[str] | None = None, record_selector: AnnotationQueueRecordSelector | None = None
) -> int:
    """Remove records from an annotation queue."""
    queues = AnnotationQueues()
    return queues.remove_records(queue_id=queue_id, record_ids=record_ids, record_selector=record_selector)


@overload
def get_annotation_queue(*, id: str) -> AnnotationQueue | None: ...


@overload
def get_annotation_queue(*, name: str) -> AnnotationQueue | None: ...


def get_annotation_queue(*, id: str | None = None, name: str | None = None) -> AnnotationQueue | None:
    """Retrieve an annotation queue by id or name."""
    queues = AnnotationQueues()
    return queues.get(id=id, name=name)  # type: ignore[call-overload]


def list_annotation_queues(limit: Unset | int = 100) -> list[AnnotationQueue]:
    """List annotation queues."""
    queues = AnnotationQueues()
    return queues.list(limit=limit)


def list_annotation_queue_users(queue_id: str) -> list[AnnotationQueueUser]:
    """List users who have access to an annotation queue."""
    queues = AnnotationQueues()
    return queues.list_users(queue_id=queue_id)


def list_annotation_queue_templates(queue_id: str) -> list[AnnotationTemplate]:
    """List templates for an annotation queue."""
    queues = AnnotationQueues()
    return queues.list_templates(queue_id=queue_id)


def update_annotation_queue(
    id: str, *, name: str | None = None, description: str | None | Unset = UNSET
) -> AnnotationQueue:
    """Update an annotation queue."""
    queues = AnnotationQueues()
    return queues.update(id=id, name=name, description=description)


def update_annotation_queue_user(
    queue_id: str, user_id: str, *, role: CollaboratorRole, track_progress: bool | None | Unset = UNSET
) -> AnnotationQueueUser:
    """Update a user's role for an annotation queue."""
    queues = AnnotationQueues()
    return queues.update_user(queue_id=queue_id, user_id=user_id, role=role, track_progress=track_progress)


def update_annotation_queue_template(
    queue_id: str, template_id: str, *, name: str, criteria: str | None
) -> AnnotationTemplate:
    """Update a template in an annotation queue."""
    queues = AnnotationQueues()
    return queues.update_template(queue_id=queue_id, template_id=template_id, name=name, criteria=criteria)


@overload
def delete_annotation_queue(*, id: str) -> None: ...


@overload
def delete_annotation_queue(*, name: str) -> None: ...


def delete_annotation_queue(*, id: str | None = None, name: str | None = None) -> None:
    """Delete an annotation queue by id or name."""
    queues = AnnotationQueues()
    return queues.delete(id=id, name=name)  # type: ignore[call-overload]


def remove_annotation_queue_user(queue_id: str, user_id: str) -> None:
    """Remove a user's access to an annotation queue."""
    queues = AnnotationQueues()
    return queues.remove_user(queue_id=queue_id, user_id=user_id)


def delete_annotation_queue_template(queue_id: str, template_id: str) -> None:
    """Delete a template from an annotation queue."""
    queues = AnnotationQueues()
    return queues.delete_template(queue_id=queue_id, template_id=template_id)


def _to_annotation_queue(
    response: AnnotationQueueResponse | HTTPValidationError | None, operation: str
) -> AnnotationQueue:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to {operation} annotation queue: {_format_validation_error(response)}"
        )
    if response is None:
        raise AnnotationQueuesAPIException(f"Failed to {operation} annotation queue: no response")
    return AnnotationQueue(queue=response)


def _to_annotation_queue_list(
    response: ListAnnotationQueueResponse | HTTPValidationError | None,
) -> ListAnnotationQueueResponse:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(f"Failed to list annotation queues: {_format_validation_error(response)}")
    if response is None:
        return ListAnnotationQueueResponse(annotation_queues=[])
    return response


def _to_annotation_queue_user_list(
    response: ListAnnotationQueueCollaboratorsResponse | HTTPValidationError | None,
) -> ListAnnotationQueueCollaboratorsResponse:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to list annotation queue users: {_format_validation_error(response)}"
        )
    if response is None:
        return ListAnnotationQueueCollaboratorsResponse(collaborators=[])
    return response


def _validate_required_string(field_name: str, value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"'{field_name}' must be provided.")
    return value


def _to_annotation_queue_run_id(*, log_stream_id: str | None, experiment_id: str | None) -> str:
    if (log_stream_id is None) == (experiment_id is None):
        raise ValueError("Exactly one of 'log_stream_id' or 'experiment_id' must be provided")

    if log_stream_id is not None:
        return _validate_required_string("log_stream_id", log_stream_id)

    assert experiment_id is not None
    return _validate_required_string("experiment_id", experiment_id)


def _to_annotation_queue_record_selector(
    *, record_ids: list[str] | None, record_selector: AnnotationQueueRecordSelector | None
) -> AnnotationQueueRecordSelector:
    if (record_ids is None) == (record_selector is None):
        raise ValueError("Exactly one of 'record_ids' or 'record_selector' must be provided")

    if record_selector is not None:
        return record_selector

    assert record_ids is not None
    clean_record_ids = [record_id.strip() for record_id in record_ids]
    if not clean_record_ids or any(not record_id for record_id in clean_record_ids):
        raise ValueError("'record_ids' must contain at least one non-empty record ID.")

    return AnnotationQueueRecordsByRecordIDs(record_ids=clean_record_ids)


def _to_add_records_response(response: AddRecordsToQueueResponse | HTTPValidationError | None) -> int:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to add records to annotation queue: {_format_validation_error(response)}"
        )
    if response is None:
        raise AnnotationQueuesAPIException("Failed to add records to annotation queue: no response")
    return response.num_records_added


def _to_remove_records_response(response: RemoveRecordsFromQueueResponse | HTTPValidationError | None) -> int:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to remove records from annotation queue: {_format_validation_error(response)}"
        )
    if response is None:
        raise AnnotationQueuesAPIException("Failed to remove records from annotation queue: no response")
    return response.num_records_removed


def _to_annotation_queue_user_create_response(
    response: list[UserAnnotationQueueCollaborator] | HTTPValidationError | None,
) -> AnnotationQueueUser:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(f"Failed to share annotation queue: {_format_validation_error(response)}")
    if not response:
        raise AnnotationQueuesAPIException("Failed to share annotation queue: no response")
    return AnnotationQueueUser(collaborator=response[0])


def _to_annotation_queue_user(
    response: UserAnnotationQueueCollaborator | HTTPValidationError | None, operation: str
) -> AnnotationQueueUser:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to {operation} annotation queue user: {_format_validation_error(response)}"
        )
    if response is None:
        raise AnnotationQueuesAPIException(f"Failed to {operation} annotation queue user: no response")
    return AnnotationQueueUser(collaborator=response)


def _to_annotation_template_create_response(
    response: list[AnnotationTemplateDB] | HTTPValidationError | None,
) -> AnnotationTemplate:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to create annotation queue template: {_format_validation_error(response)}"
        )
    if not response:
        raise AnnotationQueuesAPIException("Failed to create annotation queue template: no response")
    return AnnotationTemplate(template=response[0])


def _to_annotation_template_list(
    response: list[AnnotationTemplateDB] | HTTPValidationError | None, operation: str
) -> list[AnnotationTemplate]:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to {operation} annotation queue templates: {_format_validation_error(response)}"
        )
    if response is None:
        return []
    return [AnnotationTemplate(template=template) for template in response]


def _to_annotation_template(
    response: AnnotationTemplateDB | HTTPValidationError | None, operation: str
) -> AnnotationTemplate:
    if isinstance(response, HTTPValidationError):
        raise AnnotationQueuesAPIException(
            f"Failed to {operation} annotation queue template: {_format_validation_error(response)}"
        )
    if response is None:
        raise AnnotationQueuesAPIException(f"Failed to {operation} annotation queue template: no response")
    return AnnotationTemplate(template=response)


def _to_annotation_template_constraints(
    constraints: _AnnotationTemplateResponseConstraints,
) -> AnnotationTemplateConstraints:
    if isinstance(constraints, TreeChoiceDBConstraints):
        return TreeChoiceConstraints(
            annotation_type=constraints.annotation_type,
            choices_tree=constraints.choices_tree,
            choices_tree_yaml=constraints.choices_tree_yaml,
        )
    return cast(AnnotationTemplateConstraints, constraints)


def _format_validation_error(error: HTTPValidationError) -> str:
    if isinstance(error.detail, Unset):
        return "validation error"

    messages = [detail.msg for detail in error.detail if detail.msg]
    if not messages:
        return "validation error"
    return "; ".join(cast(list[str], messages))
