## Collection of Python galileo examples

### Preconditions

Install `uv`, we use inline dependency inside scripts.

### How to use/run?

First of all create `.env` file and add required env vars based on `.env.sample`.

Then just run `uv`:

```bash
uv run --env-file=examples/langgraph/.env examples/langgraph/with_openai.py
```

or

#### [basic_langgraph.py]
```bash
uv run --env-file=examples/langgraph/.env examples/langgraph/basic_langgraph.py
```
