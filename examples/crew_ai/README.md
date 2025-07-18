# Crew AI Example Project

This is an example project demonstrating how to use Galileo with Crew AI. It includes a simple setup for integrating Crew AI functionalities into a Python application.
Its main purpose is to showcase how to set up a project with open-inference and send traces to Galileo for observability.

## Getting Started

To get started with this project, you'll need to have Python 3.9 or later installed. You can then install the required dependencies using Poetry:

```sync
uv install
```

## Usage

Once the dependencies are installed, you can run the example application:

```bash
uv run src/main.py
```

## Project Structure

The project structure is as follows:

```
crew_ai/
├── src/          # Main application files
│   ├── __init__.py
│   ├── main.py
│   └── observability.py
├── pyproject.toml   # Project configuration file
├── README.md        # Project documentation
└── env.example      # List of environment variables
```
