#!/bin/bash

#
# Fetches the OpenAPI JSON from the provided HOST_URL and converts it to YAML.
#

# Ensure the user provides a HOST_URL
if [ -z "$1" ]; then
  echo "Usage: $0 <HOST_URL>"
  exit 1
fi

# Normalize the URL to ensure it doesn't end with a slash
HOST_URL="${1%/}"

HOME_DIR="$(pwd)"

# Fetch the OpenAPI JSON and convert it to YAML
curl -s "${HOST_URL}/openapi.json" | python3 -c 'import sys, json, yaml; yaml.safe_dump(json.load(sys.stdin), sys.stdout)' > "$HOME_DIR/openapi.yaml"

# **Patch the OpenAPI YAML to fix some schema issues**
# OpenAPI doesn't respect aliases in the router code specifically for Pydantic-based models.
#   So if two models have the same name but one is aliased as something else on import, the OpenAPI spec
#   will create two schemas with the same title, which will make client generation fail. It also doesn't handle
#   default values for query parameters in some cases.
#
#
#   The following patches fix these issues:
#   - api__schemas__project_v2__GetProjectsPaginatedResponse.title = "GetProjectsPaginatedResponseV2"
#   - galileo_core__schemas__shared__message__Message.title = "MessagesListItem"
#   - galileo_core__schemas__shared__message_role__MessageRole.title = "MessagesListItemRole"
#   - ListDatasetParams.properties.sort.default = "None"
#   - ListPromptTemplateParams.properties.sort.default = "None"
#   - ProjectCollectionParams.properties.sort.default = "None"
#   - galileo_core__schemas__shared__scorers__scorer_name__ScorerName.title = "CoreScorerName"
#   - galileo_core__schemas__shared__scorers__scorer_name__ScorerName.enum |= unique
#   - /llm_integrations/projects/{project_id}/runs/{run_id}.get.responses[200].schema.title = "GetRunIntegrationsResponse" (Windows filename length fix)
#
# If you run into related issues with the auto-generate-api-client.sh script, add the openapi.yaml patches here.
python -m yq --in-place -Y '.components.schemas.api__schemas__project_v2__GetProjectsPaginatedResponse.title = "GetProjectsPaginatedResponseV2" | .components.schemas.galileo_core__schemas__shared__message__Message.title = "MessagesListItem" | .components.schemas.galileo_core__schemas__shared__message_role__MessageRole.title = "MessagesListItemRole" | .components.schemas.ListDatasetParams.properties.sort.default = "None" | .components.schemas.ListPromptTemplateParams.properties.sort.default = "None" | .components.schemas.ProjectCollectionParams.properties.sort.default = "None" | .components.schemas.galileo_core__schemas__shared__scorers__scorer_name__ScorerName.title = "CoreScorerName" | .components.schemas.galileo_core__schemas__shared__scorers__scorer_name__ScorerName.enum |= unique | .paths["/llm_integrations/projects/{project_id}/runs/{run_id}"].get.responses["200"].content["application/json"].schema.title = "GetRunIntegrationsResponse"'  "$HOME_DIR/openapi.yaml"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "OpenAPI YAML saved to $HOME_DIR/openapi.yaml"
else
  echo "Failed to fetch and convert OpenAPI JSON"
  exit 1
fi
