from typing import Literal, cast

LLMIntegration = Literal[
    "anthropic",
    "aws_bedrock",
    "aws_sagemaker",
    "azure",
    "databricks",
    "mistral",
    "nvidia",
    "openai",
    "vegas_gateway",
    "vertex_ai",
    "writer",
]

LLM_INTEGRATION_VALUES: set[LLMIntegration] = {
    "anthropic",
    "aws_bedrock",
    "aws_sagemaker",
    "azure",
    "databricks",
    "mistral",
    "nvidia",
    "openai",
    "vegas_gateway",
    "vertex_ai",
    "writer",
}


def check_llm_integration(value: str) -> LLMIntegration:
    if value in LLM_INTEGRATION_VALUES:
        return cast(LLMIntegration, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LLM_INTEGRATION_VALUES!r}")
