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

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "OpenAPI YAML saved to $HOME_DIR/openapi.yaml"
else
  echo "Failed to fetch and convert OpenAPI JSON"
  exit 1
fi
