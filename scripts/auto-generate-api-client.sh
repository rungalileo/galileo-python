#!/bin/bash

#
# Generates an OpenAPI Python client from the provided OpenAPI spec and config file.
#

# Define the paths to the OpenAPI spec and config file
OPENAPI_SPEC_PATH="../openapi.yaml"
CONFIG_PATH="../openapi-client-config.yaml"
OUTPUT_PATH="../src/galileo/resources"
CLIENT_DIR_NAME="fast_api_client"

HOME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "$HOME_DIR"

cd "$HOME_DIR"

# Backup the current output path
mv "$OUTPUT_PATH"  "$OUTPUT_PATH"_backup

# Run the OpenAPI Python client generator
openapi-python-client generate --path "$OPENAPI_SPEC_PATH" --output-path "$OUTPUT_PATH" --custom-template-path ../codegen_templates --config "$CONFIG_PATH"

# Remove unnecessary files
rm "$OUTPUT_PATH"/pyproject.toml
rm "$OUTPUT_PATH"/.gitignore

# Flatten the structure by moving the client directory to the output path
cp -r "$OUTPUT_PATH"/"$CLIENT_DIR_NAME"/* "$OUTPUT_PATH"
rm -r "$OUTPUT_PATH"/"$CLIENT_DIR_NAME"

# Remove the backup directory
rm -r "$OUTPUT_PATH"_backup

echo "OpenAPI Python client generated."
