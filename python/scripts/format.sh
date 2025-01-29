#!/bin/sh -ex

pre-commit run black --all-files
pre-commit run isort --all-files
