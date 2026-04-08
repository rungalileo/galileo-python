#!/usr/bin/env bash
set -euo pipefail

# Install Poetry via pipx (pipx is pre-installed in Microsoft Python devcontainer images)
pipx install poetry

# Use a container-local virtualenv path to avoid clobbering the host's .venv
poetry config virtualenvs.in-project false
poetry config virtualenvs.path "$HOME/.cache/pypoetry/virtualenvs"

# Install all project dependencies including optional extras
poetry install --all-extras

# Set up pre-commit hooks
poetry run pre-commit install --hook-type pre-commit

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
