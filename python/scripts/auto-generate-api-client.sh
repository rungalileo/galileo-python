
#!/bin/bash

# openapi-python-client generate --path ../openapi.yaml --config ../openapi-client-config.yaml



# Define the paths to the OpenAPI spec and config file
OPENAPI_SPEC_PATH="../openapi.yaml"
CONFIG_PATH="../openapi-client-config.yaml"
OUTPUT_PATH="../galileo/resources"
CLIENT_DIR_NAME="galileo_api_server_client"

mv "$OUTPUT_PATH"  "$OUTPUT_PATH"_backup

# Run the OpenAPI Python client generator
openapi-python-client generate --path "$OPENAPI_SPEC_PATH" --output-path "$OUTPUT_PATH"
# --config "$CONFIG_PATH" 

rm "$OUTPUT_PATH"/README.md
rm "$OUTPUT_PATH"/pyproject.toml
rm "$OUTPUT_PATH"/.gitignore
rm -r "$OUTPUT_PATH"/.ruff_cache
cp -r "$OUTPUT_PATH"/"$CLIENT_DIR_NAME"/* "$OUTPUT_PATH"
rm -r "$OUTPUT_PATH"_backup

echo "OpenAPI Python client generated."