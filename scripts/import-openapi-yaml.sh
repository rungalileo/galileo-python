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
curl -s "${HOST_URL}/openapi.json" | poetry run python -c 'import sys, json, yaml; yaml.safe_dump(json.load(sys.stdin), sys.stdout, default_flow_style=False, sort_keys=False)' > "$HOME_DIR/openapi.yaml"

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
#   - Document.properties.page_content -> Document.properties.content (Fix field name mismatch with API)
#   - Rename long schema titles to shorter ones (Windows filename length fix - prevents "Filename too long" errors):
#     - AndNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____.title = "AndNodeLogRecordsFilter"
#     - FilterExpression_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____.title = "FilterExpressionLogRecordsFilter"
#     - FilterLeaf_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____.title = "FilterLeafLogRecordsFilter"
#     - NotNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____.title = "NotNodeLogRecordsFilter"
#     - OrNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____.title = "OrNodeLogRecordsFilter"
#   - StepType.enum += ["control"] |= unique: server omits this value from the spec but returns it for some log-stream columns (sc-62628); unique deduplicates if the server spec is later fixed
#   - Rename duplicate search/filter schema titles emitted for experiments/log streams
#   - Rename duplicate prompt bulk-delete and custom integration model property titles
#   - ExperimentSearchRequest.properties.sort.default = "None"
#   - LogStreamSearchRequest.properties.sort.default = "None"
#   - ListAnnotationQueueParams.properties.sort.default = "None"
#   - Rename duplicate annotation feedback rating schema titles
#   - Replace recursive JsonValue schema with a permissive client-generation schema
#
# If you run into related issues with the auto-generate-api-client.sh script, add the openapi.yaml patches here.

# Apply all patches using yq in a single command
poetry run python -m yq --in-place -Y '.components.schemas.api__schemas__project_v2__GetProjectsPaginatedResponse.title = "GetProjectsPaginatedResponseV2" | .components.schemas.galileo_core__schemas__shared__message__Message.title = "MessagesListItem" | .components.schemas.galileo_core__schemas__shared__message_role__MessageRole.title = "MessagesListItemRole" | .components.schemas.ListDatasetParams.properties.sort.default = "None" | .components.schemas.ListPromptTemplateParams.properties.sort.default = "None" | .components.schemas.ProjectCollectionParams.properties.sort.default = "None" | .components.schemas.galileo_core__schemas__shared__scorers__scorer_name__ScorerName.title = "CoreScorerName" | .components.schemas.galileo_core__schemas__shared__scorers__scorer_name__ScorerName.enum |= unique | .paths["/llm_integrations/projects/{project_id}/runs/{run_id}"].get.responses["200"].content["application/json"].schema.title = "GetRunIntegrationsResponse" | .components.schemas.Document.properties.content = .components.schemas.Document.properties.page_content | del(.components.schemas.Document.properties.page_content) | .components.schemas.Document.properties.content.title = "Content" | .components.schemas.Document.required = ["content"] | .components.schemas["AndNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____"].title = "AndNodeLogRecordsFilter" | .components.schemas["FilterExpression_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____"].title = "FilterExpressionLogRecordsFilter" | .components.schemas["FilterLeaf_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____"].title = "FilterLeafLogRecordsFilter" | .components.schemas["NotNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____"].title = "NotNodeLogRecordsFilter" | .components.schemas["OrNode_Annotated_Union_LogRecordsIDFilter__LogRecordsDateFilter__LogRecordsNumberFilter__LogRecordsBooleanFilter__LogRecordsCollectionFilter__LogRecordsTextFilter__LogRecordsFullyAnnotatedFilter___FieldInfo_annotation_NoneType__required_True__discriminator__type____"].title = "OrNodeLogRecordsFilter" | .components.schemas.StepType.enum += ["control"] | .components.schemas.StepType.enum |= unique'  "$HOME_DIR/openapi.yaml"

poetry run python - <<'PY'
from pathlib import Path

import yaml

openapi_path = Path("openapi.yaml")
with openapi_path.open() as openapi_file:
    openapi = yaml.safe_load(openapi_file)

schemas = openapi["components"]["schemas"]

for schema_name in (
    "LogStreamCreatedAtFilter",
    "LogStreamCreatedAtSort",
    "LogStreamCreatedByFilter",
    "LogStreamIDFilter",
    "LogStreamNameFilter",
    "LogStreamNameSort",
    "LogStreamUpdatedAtFilter",
    "LogStreamUpdatedAtSort",
    "ExperimentCreatedAtFilter",
    "ExperimentCreatedAtSort",
    "ExperimentCreatedByFilter",
    "ExperimentIDFilter",
    "ExperimentNameFilter",
    "ExperimentNameSort",
    "ExperimentUpdatedAtFilter",
    "ExperimentUpdatedAtSort",
):
    if schema_name in schemas:
        schemas[schema_name]["title"] = schema_name

title_patches = {
    "api__schemas__content__prompt__BulkDeleteFailure": "PromptBulkDeleteFailure",
    "api__schemas__integration__llm_integration__ModelProperties": "LLMIntegrationModelProperties",
    "promptgalileo__schemas__config__custom__ModelProperties": "CustomIntegrationModelProperties",
    "libs__python__schemas__log_records__feedback__ChoiceRating": "LogRecordsChoiceRating",
    "libs__python__schemas__log_records__feedback__LikeDislikeRating": "LogRecordsLikeDislikeRating",
    "libs__python__schemas__log_records__feedback__ScoreRating": "LogRecordsScoreRating",
    "libs__python__schemas__log_records__feedback__StarRating": "LogRecordsStarRating",
    "libs__python__schemas__log_records__feedback__TagsRating": "LogRecordsTagsRating",
    "libs__python__schemas__log_records__feedback__TextRating": "LogRecordsTextRating",
    "libs__python__schemas__log_records__feedback__TreeChoiceRating": "LogRecordsTreeChoiceRating",
}
for schema_name, title in title_patches.items():
    if schema_name in schemas:
        schemas[schema_name]["title"] = title

for schema_name in ("ExperimentSearchRequest", "LogStreamSearchRequest", "ListAnnotationQueueParams"):
    schema = schemas.get(schema_name)
    if schema:
        schema.get("properties", {}).get("sort", {})["default"] = "None"

if "JsonValue" in schemas:
    schemas["JsonValue"] = {
        "title": "JsonValue",
        "description": "Arbitrary JSON value. Patched for client generation because recursive schemas are not supported.",
        "additionalProperties": True,
    }

with openapi_path.open("w") as openapi_file:
    yaml.safe_dump(openapi, openapi_file, default_flow_style=False, sort_keys=False)
PY

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "OpenAPI YAML saved to $HOME_DIR/openapi.yaml"
else
  echo "Failed to fetch and convert OpenAPI JSON"
  exit 1
fi
