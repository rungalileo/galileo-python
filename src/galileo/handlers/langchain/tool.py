from collections.abc import Sequence
from typing import Optional

from langchain_core.runnables.base import Runnable
from langchain_core.tools import BaseTool
from pydantic import UUID4, BaseModel, ConfigDict, Field
from pydantic.v1 import BaseModel as BaseModelV1

from galileo.constants.protect import TIMEOUT_SECS
from galileo.protect import ainvoke_protect, invoke_protect
from galileo_core.schemas.protect.execution_status import ExecutionStatus
from galileo_core.schemas.protect.payload import Payload as CorePayload
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.protect.ruleset import Ruleset


class ProtectToolInputSchema(BaseModelV1):
    input: Optional[str] = None
    output: Optional[str] = None


class ProtectTool(BaseTool):
    """A LangChain tool that wraps the Galileo Protect API.

    This tool allows you to integrate Galileo Protect into your LangChain applications
    to scan for and mitigate harmful content in both inputs and outputs. It can be
    configured with specific rulesets and linked to a Galileo project and stage for
    monitoring and management.

    It accepts an input and/or output as arguments (parsed by a Pydantic model) and returns a JSON-serialized ``Response`` object from the Protect API.

    Attributes:
        prioritized_rulesets: An optional sequence of ``Ruleset`` objects to apply.
        project_id: The UUID of the Galileo project this tool is associated with.
        project_name: The name of the Galileo project.
        stage_name: The name of the Protect stage to use for this tool.
        stage_id: The UUID of the Protect stage.
        stage_version: The version of the Protect stage to use.
        timeout: The timeout in seconds for the API request.
    """

    name: str = "GalileoProtect"
    description: str = (
        "Protect your LLM applications from harmful content using Galileo Protect. "
        "This tool is a wrapper around Galileo's Protect API, can be used to scan text "
        "for harmful content, and can be used to trigger actions based on the results."
        "The tool can be used on the input text or output text, and can be configured "
        "with a set of rulesets to evaluate on."
    )
    # langchain requires pydantic v1
    args_schema: type[BaseModelV1] = ProtectToolInputSchema

    prioritized_rulesets: Optional[Sequence[Ruleset]] = None
    project_id: Optional[UUID4] = None
    project_name: Optional[str] = None
    stage_name: Optional[str] = None
    stage_id: Optional[UUID4] = None
    stage_version: Optional[int] = None
    timeout: float = TIMEOUT_SECS

    def _run(self, input: Optional[str] = None, output: Optional[str] = None) -> str:
        """
        Apply the tool synchronously.

        We serialize the response to JSON because that's what `langchain_core` expects
        for tools.
        """
        api_payload = CorePayload(input=input, output=output)
        api_response = invoke_protect(
            payload=api_payload,
            prioritized_rulesets=self.prioritized_rulesets,
            project_name=self.project_name,
            project_id=self.project_id,
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            stage_version=self.stage_version,
            timeout=self.timeout,
        )
        return api_response.model_dump_json()

    async def _arun(self, input: Optional[str] = None, output: Optional[str] = None) -> str:
        """
        Apply the tool asynchronously.

        We serialize the response to JSON because that's what `langchain_core` expects
        for tools.
        """
        api_payload = CorePayload(input=input, output=output)
        api_response = await ainvoke_protect(
            payload=api_payload,
            prioritized_rulesets=self.prioritized_rulesets,
            project_name=self.project_name,
            project_id=self.project_id,
            stage_name=self.stage_name,
            stage_id=self.stage_id,
            stage_version=self.stage_version,
            timeout=self.timeout,
        )
        return api_response.model_dump_json()


class ProtectParser(BaseModel):
    """A LangChain runnable that parses and routes the output of a ``ProtectTool``.

    If the Protect API response is 'triggered', it returns the response text.
    Otherwise, it invokes a fallback chain.

    Attributes:
        chain: The ``Runnable`` to invoke if the Protect invocation is not triggered.
        ignore_trigger: If True, always invoke the fallback chain.
        echo_output: If True, print the raw Protect API response to the console.
    """

    chain: Runnable = Field(..., description="The chain to trigger if the Protect invocation is not triggered.")
    ignore_trigger: bool = Field(
        default=False,
        description="Ignore the status of the Protect invocation and always trigger the rest of the chain.",
    )
    echo_output: bool = Field(default=False, description="Echo the output of the Protect invocation.")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def parser(self, response_raw_json: str) -> str:
        """Parses the JSON response from ``ProtectTool`` and decides the execution path.

        If the response status is 'triggered', the response text is returned. Otherwise,
        the fallback chain is invoked with the text.

        If JSON parsing fails, it assumes the input is not from ``ProtectTool`` and
        invokes the fallback chain directly with the raw input.

        Args:
            response_raw_json: Expects the output from the ``ProtectTool``.

        Returns:
            The text from the Protect response if triggered, or the result of invoking
            the fallback chain.
        """
        try:
            response = Response.model_validate_json(response_raw_json)
        except Exception:
            return self.chain.invoke(response_raw_json)
        text = response.text

        if self.echo_output:
            print(f"> Raw response: {text}")
        if response.status == ExecutionStatus.triggered and not self.ignore_trigger:
            return text
        else:
            return self.chain.invoke(text)
