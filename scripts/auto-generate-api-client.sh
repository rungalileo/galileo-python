#!/bin/bash

#
# Generates an OpenAPI Python client from the provided OpenAPI spec and config file.
#

set -euo pipefail

# Define the paths to the OpenAPI spec and config file
OPENAPI_SPEC_PATH="../openapi.yaml"
CONFIG_PATH="../openapi-client-config.yaml"
OUTPUT_PATH="../src/galileo/resources"

HOME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "$HOME_DIR"

cd "$HOME_DIR"

# Backup the current output path
mv "$OUTPUT_PATH"  "$OUTPUT_PATH"_backup

# Run the OpenAPI Python client generator
poetry run openapi-python-client generate --meta none  --path "$OPENAPI_SPEC_PATH" --output-path "$OUTPUT_PATH" --custom-template-path ../codegen_templates --config "$CONFIG_PATH" --overwrite

# Remove the backup directory
rm -r "$OUTPUT_PATH"_backup

# Post-generation patch: rewrite HTTPValidationError.from_dict so plain-string
# `detail` payloads (e.g. invalid model alias) don't crash. Exits 2 on template
# drift, which `set -e` propagates to fail the regen.
poetry run python "$HOME_DIR/patch_http_validation_error.py" "$HOME_DIR/$OUTPUT_PATH/models/http_validation_error.py"

echo "OpenAPI Python client generated."
