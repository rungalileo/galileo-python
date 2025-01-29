#!/bin/sh -ex

pre-commit run ruff --all-files
pre-commit run mypy --all-files
