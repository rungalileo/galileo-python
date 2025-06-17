from collections.abc import Sequence
from typing import Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.constants.protect import TIMEOUT
from galileo.resources.api.protect import invoke_v2_protect_invoke_post
from galileo.resources.models.invoke_response import InvokeResponse
from galileo.resources.models.payload import Payload
from galileo.resources.models.request import Request
from galileo.resources.models.response import Response
from galileo.resources.models.ruleset import Ruleset
from galileo.utils.catch_log import DecorateAllMethods


class Protect(BaseClientModel, DecorateAllMethods):
    def invoke(
        self,
        payload: Payload,
        prioritized_rulesets: Optional[Sequence[Ruleset]] = None,
        project_id: Optional[UUID4] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[UUID4] = None,
        stage_name: Optional[str] = None,
        stage_version: Optional[int] = None,
        timeout: float = TIMEOUT,
        metadata: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        # TODO only ever Response due to InvokeResponse being a superset and the way from_dict works
        # However if we want parity with 1.0 this should just be Response
        # Also if we never actually return InvokeResponse here, why mention it?
    ) -> Union[Response, InvokeResponse]:
        """
        Calls invoke api.

        Returns
        -------
        InvokeResponse
            Various data from api

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        body = Request(
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

        response: Union[Response, InvokeResponse] = invoke_v2_protect_invoke_post.sync(client=self.client, body=body)
        return response


def invoke(
    payload: Payload,
    prioritized_rulesets: Optional[Sequence[Ruleset]] = None,
    project_id: Optional[UUID4] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[UUID4] = None,
    stage_name: Optional[str] = None,
    stage_version: Optional[int] = None,
    timeout: float = TIMEOUT,
    metadata: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> Union[Response, InvokeResponse]:
    """
    Invoke Protect with the given payload.

    If using the local stage, the prioritized rulesets should be provided to ensure the
    correct rulesets are used for processing. If using a central stage, the rulesets
    will be fetched from the existing stage definition.

    Project ID and stage name, or stage ID should be provided for all invocations.

    Parameters
    ----------
    payload : Payload
        Payload to be processed.
    prioritized_rulesets : Optional[Sequence[Ruleset]], optional
        Prioritized rulesets to be used for processing. These should only be provided if
        using a local stage, by default None, i.e. empty list.
    project_id : Optional[UUID4], optional
        Project ID to be used for processing, by default None.
    project_name : Optional[str], optional
        Project name to be used for processing, by default None.
    stage_id : Optional[UUID4], optional
        Stage ID to be used for processing, by default None.
    stage_name : Optional[str], optional
        Stage name to be used for processing, by default None.
    timeout : float, optional
        Timeout for the request, by default 10 seconds.
    metadata : Optional[Dict[str, str]], optional
        Metadata to be added when responding, by default None.
    headers : Optional[Dict[str, str]], optional
        Headers to be added to the response, by default None.

    Returns
    -------
    Union[Response, InvokeResponse]
        Response from the Protect API.
    """
    return Protect().invoke(
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
