#!/bin/bash

#
# Generates an OpenAPI Python client from the provided OpenAPI spec and config file.
#

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
openapi-python-client generate --meta none  --path "$OPENAPI_SPEC_PATH" --output-path "$OUTPUT_PATH" --custom-template-path ../codegen_templates --config "$CONFIG_PATH"

# Remove the backup directory
rm -r "$OUTPUT_PATH"_backup

# Lint and format the generated code
ruff check "$OUTPUT_PATH"/ --fix
ruff format "$OUTPUT_PATH"/

echo "OpenAPI Python client generated."
