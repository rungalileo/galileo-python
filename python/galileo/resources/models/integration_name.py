from enum import Enum


class IntegrationName(str, Enum):
    ANTHROPIC = "anthropic"
    AWS_BEDROCK = "aws_bedrock"
    AWS_SAGEMAKER = "aws_sagemaker"
    AZURE = "azure"
    DATABRICKS = "databricks"
    LABELSTUDIO = "labelstudio"
    MISTRAL = "mistral"
    OPENAI = "openai"
    VERTEX_AI = "vertex_ai"
    WRITER = "writer"

    def __str__(self) -> str:
        return str(self.value)
