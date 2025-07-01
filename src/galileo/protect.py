from collections.abc import Sequence
from typing import Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.constants.protect import TIMEOUT_SECS
from galileo.resources.api.protect import invoke_protect_invoke_post
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.request import Request as APIRequest
from galileo.resources.models.response import Response as APIResponse
from galileo.utils.catch_log import DecorateAllMethods
from galileo_core.helpers.execution import async_run
from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.request import Request
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.protect.ruleset import Ruleset


class Protect(BaseClientModel, DecorateAllMethods):
    async def ainvoke(
        self,
        payload: Payload,
        prioritized_rulesets: Optional[Sequence[Ruleset]] = None,
        project_id: Optional[UUID4] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[UUID4] = None,
        stage_name: Optional[str] = None,
        stage_version: Optional[int] = None,
        timeout: float = TIMEOUT_SECS,
        metadata: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Optional[Union[Response, HTTPValidationError]]:
        request = Request(
            payload=payload,
            prioritized_rulesets=prioritized_rulesets or [],
            project_id=str(project_id) if project_id is not None else None,
            project_name=project_name,
            stage_id=str(stage_id) if stage_id is not None else None,
            stage_name=stage_name,
            stage_version=stage_version,
            timeout=timeout,
            metadata=metadata,
            headers=headers,
        )
        request_dict = request.model_dump(mode="json")
        request_dict["prioritized_rulesets"] = request_dict.pop("rulesets", [])
        body = APIRequest.from_dict(request_dict)

        response: Optional[Union[APIResponse, HTTPValidationError]] = await invoke_protect_invoke_post.asyncio(
            client=self.client, body=body
        )

        if isinstance(response, APIResponse):
            return Response.model_validate(response.to_dict())
        return response


async def ainvoke(
    payload: Payload,
    prioritized_rulesets: Optional[Sequence[Ruleset]] = None,
    project_id: Optional[UUID4] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[UUID4] = None,
    stage_name: Optional[str] = None,
    stage_version: Optional[int] = None,
    timeout: float = TIMEOUT_SECS,
    metadata: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> Optional[Union[Response, HTTPValidationError]]:
    """Asynchronously invoke Protect with the given payload.

    If using the local stage, the prioritized rulesets should be provided to ensure the
    correct rulesets are used for processing. If using a central stage, the rulesets
    will be fetched from the existing stage definition.

    Project ID and stage name, or stage ID should be provided for all invocations.

    Args:
        payload: Payload to be processed.
        prioritized_rulesets: Prioritized rulesets to be used for processing.
            These should only be provided if using a local stage. Defaults to an
            empty list if None.
        project_id: ID of the project.
        project_name: Name of the project.
        stage_id: ID of the stage.
        stage_name: Name of the stage.
        stage_version: Version of the stage.
        timeout: Timeout for the request in seconds. Defaults to TIMEOUT_SECS.
        metadata: Metadata to be added when responding.
        headers: Headers to be added to the response.

    Returns:
        Protect invoke results.
    """
    return await Protect().ainvoke(
        payload=payload,
        prioritized_rulesets=prioritized_rulesets,
        project_id=project_id,
        project_name=project_name,
        stage_id=stage_id,
        stage_name=stage_name,
        stage_version=stage_version,
        timeout=timeout,
        metadata=metadata,
        headers=headers,
    )


def invoke(
    payload: Payload,
    prioritized_rulesets: Optional[Sequence[Ruleset]] = None,
    project_id: Optional[UUID4] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[UUID4] = None,
    stage_name: Optional[str] = None,
    stage_version: Optional[int] = None,
    timeout: float = TIMEOUT_SECS,
    metadata: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> Optional[Union[Response, HTTPValidationError]]:
    """Invoke Protect with the given payload.

    If using the local stage, the prioritized rulesets should be provided to ensure the
    correct rulesets are used for processing. If using a central stage, the rulesets
    will be fetched from the existing stage definition.

    Project ID and stage name, or stage ID should be provided for all invocations.

    Args:
        payload: Payload to be processed.
        prioritized_rulesets: Prioritized rulesets to be used for processing.
            These should only be provided if using a local stage. Defaults to an
            empty list if None.
        project_id: ID of the project.
        project_name: Name of the project.
        stage_id: ID of the stage.
        stage_name: Name of the stage.
        stage_version: Version of the stage.
        timeout: Timeout for the request in seconds. Defaults to TIMEOUT_SECS.
        metadata: Metadata to be added when responding.
        headers: Headers to be added to the response.

    Returns:
        Protect invoke results.
    """
    return async_run(
        ainvoke(
            payload=payload,
            prioritized_rulesets=prioritized_rulesets,
            project_id=project_id,
            project_name=project_name,
            stage_id=stage_id,
            stage_name=stage_name,
            stage_version=stage_version,
            timeout=timeout,
            metadata=metadata,
            headers=headers,
        )
    )
