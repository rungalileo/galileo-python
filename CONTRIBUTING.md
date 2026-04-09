# Contributing to the Galileo Python SDK

## Local Installation

### Pre-Requisites

1. Clone this repo locally.
2. Install [pyenv](https://github.com/pyenv/pyenv).
3. Install [`poetry`](https://python-poetry.org/): `curl -sSL https://install.python-poetry.org | python3 -`

### Setup

1. Setup a virtual environment:

   ```sh
   pyenv install 3.13
   pyenv local 3.13
   ```

   `poetry` will create a virtual environment using that Python version when it installs dependencies. You can validate that with:

   > **_NOTE:_** since The `shell` command was moved to a plugin: [poetry-plugin-shell](https://github.com/python-poetry/poetry-plugin-shell)

   The easiest way to install the shell plugin is via the self add command of Poetry:

   ```shell
   poetry self add poetry-plugin-shell
   ```

   ```sh
   poetry shell
   poetry run python --version
   ```

   which should print out `Python 3.13.x`.

1. Install dependencies and setup pre-commit hooks:

   ```sh
   pip3 install --upgrade invoke
   inv setup
   ```

## Auto-generating the API client

1. Run `./scripts/import-openapi-yaml.sh https://api.galileo.ai/client` to update the openapi.yml file with the latest client spec
2. Run `./scripts/auto-generate-api-client.sh` to generate the API client
