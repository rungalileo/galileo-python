# Galileo Python SDK

This package is still under development, so the instructions below are tailored to project contributors.

## Getting Started

### Pre-Requisites

1. Clone this repo locally.
2. Install [pyenv](https://github.com/pyenv/pyenv).
3. Install [`poetry`](https://python-poetry.org/): `curl -sSL https://install.python-poetry.org | python3 -`

### Setup

1. Setup a virtual environment:

```sh
pyenv install 3.10.13
pyenv local 3.10.13
```

`poetry` will create a virtual environment using that Python version when it installs dependencies. You can validate that with:

```sh
poetry shell
poetry run python --version
```

which should print out `Python 3.10.13`.

2. Install dependencies and setup pre-commit hooks:

```sh
pip3 install --upgrade invoke
inv setup
```

3. Copy .env.example to .env and populate the values.

## Testing the API

You can modify the main.py file to test the API locally:

```sh
python main.py
```
