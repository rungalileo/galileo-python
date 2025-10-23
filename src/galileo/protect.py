import logging
import sys
from collections.abc import Sequence
from typing import Optional, Union

from pydantic import UUID4

from galileo.config import GalileoPythonConfig
from galileo.constants.protect import TIMEOUT_SECS
from galileo.resources.api.protect import invoke_protect_invoke_post
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.protect_request import ProtectRequest as APIRequest
from galileo.resources.models.protect_response import ProtectResponse as APIResponse
from galileo.utils.catch_log import DecorateAllMethods
from galileo_core.helpers.execution import async_run
from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.request import Request
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.protect.ruleset import Ruleset

_logger = logging.getLogger(__name__)

# Ensure at least WARNING messages are visible even if user hasn't configured logging
if not logging.root.handlers:
    _console_handler = logging.StreamHandler(sys.stderr)
    _console_handler.setLevel(logging.WARNING)
    _console_handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    logging.root.addHandler(_console_handler)
    logging.root.setLevel(logging.WARNING)


class Protect(DecorateAllMethods):
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

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
        _logger.debug(
            "Invoking Protect: project_name=%s, project_id=%s, stage_name=%s, stage_id=%s, "
            "stage_version=%s, timeout=%s, num_rulesets=%s",
            project_name,
            project_id,
            stage_name,
            stage_id,
            stage_version,
            timeout,
            len(prioritized_rulesets) if prioritized_rulesets else 0,
        )

        try:
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
            _logger.debug("Protect request created successfully")
        except Exception as e:
            _logger.error("Failed to create Protect request: %s", e, exc_info=True)
            raise

        try:
            request_dict = request.model_dump(mode="json")
            request_dict["prioritized_rulesets"] = request_dict.pop("rulesets", [])
            body = APIRequest.from_dict(request_dict)
            _logger.debug("Protect API request body prepared")
        except Exception as e:
            _logger.error("Failed to prepare API request body: %s", e, exc_info=True)
            raise

        try:
            _logger.debug("Sending Protect API request to %s", self.config.console_url)
            response: Optional[Union[APIResponse, HTTPValidationError]] = await invoke_protect_invoke_post.asyncio(
                client=self.config.api_client, body=body
            )
            _logger.debug("Protect API request completed, response type: %s", type(response).__name__)
        except Exception as e:
            _logger.error(
                "Protect API request failed: %s. Check network connectivity, API key, and endpoint availability.",
                e,
                exc_info=True,
            )
            raise

        if response is None:
            error_msg = (
                f"Protect API returned None for project '{project_name}' and stage '{stage_name}'. "
                f"This may indicate a network issue, timeout, or API error. "
                f"Console URL: {self.config.console_url}. "
                f"Check API key configuration and network connectivity."
            )
            _logger.error(error_msg)
            # Also use warnings module to ensure visibility
            import warnings

            warnings.warn(error_msg, RuntimeWarning, stacklevel=2)
            return None

        if isinstance(response, HTTPValidationError):
            _logger.error(
                "Protect API returned validation error: %s. Check request parameters: "
                "project_name=%s, stage_name=%s, num_rulesets=%s",
                response,
                project_name,
                stage_name,
                len(prioritized_rulesets) if prioritized_rulesets else 0,
            )
            return response

        if isinstance(response, APIResponse):
            _logger.debug("Protect invocation successful, converting response")
            return Response.model_validate(response.to_dict())

        _logger.warning("Unexpected response type from Protect API: %s", type(response).__name__)
        return response


async def ainvoke_protect(
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

    Parameters
    ----------
    payload
        Payload to be processed.
    prioritized_rulesets
        Prioritized rulesets to be used for processing.
        These should only be provided if using a local stage. Defaults to an
        empty list if None.
    project_id
        ID of the project.
    project_name
        Name of the project.
    stage_id
        ID of the stage.
    stage_name
        Name of the stage.
    stage_version
        Version of the stage.
    timeout
        Timeout for the request in seconds. Defaults to TIMEOUT_SECS.
    metadata
        Metadata to be added when responding.
    headers
        Headers to be added to the response.

    Returns
    -------
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


def invoke_protect(
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

    Parameters
    ----------
    payload
        Payload to be processed.
    prioritized_rulesets
        Prioritized rulesets to be used for processing.
        These should only be provided if using a local stage. Defaults to an
        empty list if None.
    project_id
        ID of the project.
    project_name
        Name of the project.
    stage_id
        ID of the stage.
    stage_name
        Name of the stage.
    stage_version
        Version of the stage.
    timeout
        Timeout for the request in seconds. Defaults to TIMEOUT_SECS.
    metadata
        Metadata to be added when responding.
    headers
        Headers to be added to the response.

    Returns
    -------
    Protect invoke results.
    """
    return async_run(
        ainvoke_protect(
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
