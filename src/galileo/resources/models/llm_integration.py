from enum import Enum


class LLMIntegration(str, Enum):
    ANTHROPIC = "anthropic"
    AWS_BEDROCK = "aws_bedrock"
    AWS_SAGEMAKER = "aws_sagemaker"
    AZURE = "azure"
    DATABRICKS = "databricks"
    MISTRAL = "mistral"
    NVIDIA = "nvidia"
    OPENAI = "openai"
    VEGAS_GATEWAY = "vegas_gateway"
    VERTEX_AI = "vertex_ai"
    WRITER = "writer"

    def __str__(self) -> str:
        return str(self.value)
