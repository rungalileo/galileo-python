#!/bin/bash

#
# Fetches the OpenAPI JSON from the provided HOST_URL and converts it to YAML,
# while filtering out sensitive default values.
#

# Ensure the user provides a HOST_URL
if [ -z "$1" ]; then
  echo "Usage: $0 <HOST_URL>"
  exit 1
fi

# Normalize the URL to ensure it doesn't end with a slash
HOST_URL="${1%/}"

HOME_DIR="$(cd .. && pwd)"

# Create a more robust Python script to filter sensitive defaults
cat > /tmp/filter_openapi.py << 'EOF'
import sys
import json
import yaml

def filter_sensitive_defaults(data):
    # Get the schemas section
    schemas = data.get('components', {}).get('schemas', {})
    
    # List of schemas and their properties with sensitive defaults to remove
    sensitive_paths = [
        ('AgenticWorkflowSuccessTemplate', ['metric_system_prompt', 'template']),
        ('CustomizedAgenticWorkflowSuccessGPTScorer', ['metric_system_prompt']),
        ('CustomizedFactualityGPTScorer', ['metric_system_prompt']),
        ('CustomizedGroundTruthAdherenceGPTScorer', ['metric_system_prompt']),
        ('CustomizedGroundednessGPTScorer', ['metric_system_prompt']),
        ('CustomizedInstructionAdherenceGPTScorer', ['metric_system_prompt']),
        ('CustomizedToolErrorRateGPTScorer', ['metric_system_prompt']),
        ('CustomizedToolSelectionQualityGPTScorer', ['metric_system_prompt']),
        ('FactualityTemplate', ['metric_system_prompt', 'template', 'metric_few_shot_examples']),
        ('GroundTruthAdherenceTemplate', ['metric_system_prompt', 'template']),
        ('InstructionAdherenceTemplate', ['metric_system_prompt', 'template']),
        ('ToolErrorRateTemplate', ['metric_system_prompt', 'template']),
        ('ToolSelectionQualityTemplate', ['metric_system_prompt', 'template']),
        # Add more schema/property combinations as needed
    ]
    
    # Process each schema and its properties
    for schema_name, properties in sensitive_paths:
        if schema_name in schemas and 'properties' in schemas[schema_name]:
            schema_props = schemas[schema_name]['properties']
            for prop in properties:
                if prop in schema_props:
                    # Remove direct values if present
                    if 'default' in schema_props[prop]:
                        print(f"Removing default value from {schema_name}.{prop}", file=sys.stderr)
                        del schema_props[prop]['default']
                        
                    # If the property contains examples with sensitive content
                    if 'examples' in schema_props[prop]:
                        print(f"Removing examples from {schema_name}.{prop}", file=sys.stderr)
                        del schema_props[prop]['examples']
                    
                    # Handle const values if present
                    if 'const' in schema_props[prop]:
                        print(f"Removing const value from {schema_name}.{prop}", file=sys.stderr)
                        del schema_props[prop]['const']
                        
    # Also check for any properties named 'metric_few_shot_examples' in any schema
    for schema_name, schema in schemas.items():
        if 'properties' in schema:
            for prop_name, prop in schema['properties'].items():
                # Remove default examples from all example-related properties
                if 'metric_few_shot_examples' == prop_name and 'default' in prop:
                    print(f"Removing default examples from {schema_name}.{prop_name}", file=sys.stderr)
                    del prop['default']
                
                # Handle the case where examples are nested in other properties
                if isinstance(prop, dict) and 'properties' in prop:
                    for nested_prop_name, nested_prop in prop['properties'].items():
                        if nested_prop_name == 'metric_few_shot_examples' and 'default' in nested_prop:
                            print(f"Removing nested examples from {schema_name}.{prop_name}.{nested_prop_name}", file=sys.stderr)
                            del nested_prop['default']
    
    return data

# Read JSON from stdin
data = json.load(sys.stdin)

# Filter out sensitive defaults
filtered = filter_sensitive_defaults(data)

# Output as YAML with proper formatting
yaml.safe_dump(filtered, sys.stdout, sort_keys=False)
EOF

echo "Fetching and filtering OpenAPI spec from ${HOST_URL}..."

# Fetch the OpenAPI JSON, filter it, and save as YAML
curl -s "${HOST_URL}/openapi.json" | python3 /tmp/filter_openapi.py > "$HOME_DIR/openapi.yaml"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "Filtered OpenAPI YAML saved to $HOME_DIR/openapi.yaml"
  rm /tmp/filter_openapi.py
else
  echo "Failed to fetch and convert OpenAPI JSON"
  rm /tmp/filter_openapi.py
  exit 1
fi