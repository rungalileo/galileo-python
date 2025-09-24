#!/bin/sh -ex

echo "🔍 Running lint checks (excluding auto-generated files)..."
poetry run pre-commit run ruff --all-files
poetry run pre-commit run mypy --all-files
echo "✅ All lint checks completed successfully!"
