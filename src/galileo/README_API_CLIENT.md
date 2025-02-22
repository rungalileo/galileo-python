# Galileo API client

A client library for accessing the Galileo platform API

## Usage

First, create a client:

```python
from galileo.api_client import GalileoApiClient

# Make sure you've set the GALILEO_CONSOLE_URL and GALILEO_API_KEY env vars
# Optionally, you can specify both base_url and api_key
client = GalileoApiClient()
```

Now call your endpoint and use your models:

```python
from galileo.resources.models import MyDataModel
from galileo.resources.api.my_tag import get_my_data_model
from galileo.resources.types import Response

my_data: MyDataModel = get_my_data_model.sync(client=client)
# or if you need more info (e.g. status_code)
response: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from galileo.resources.models import MyDataModel
from galileo.resources.api.my_tag import get_my_data_model
from galileo.resources.types import Response

my_data: MyDataModel = await get_my_data_model.asyncio(client=client)
# or if you need more info (e.g. status_code)
response: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = GalileoApiClient(
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = GalileoApiClient(verify_ssl=False)
```

Things to know:

1. Every path/method combo becomes a Python module with four functions:

   1. `sync`: Blocking request that returns parsed data (if successful) or `None`
   1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
   1. `asyncio`: Like `sync` but async instead of blocking
   1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `galileo.api.default`

## Advanced customizations

There are more settings on the `GalileoApiClient` class which let you control more runtime behavior, check out the docstring on that class for more info. You can also customize the underlying `httpx.Client` or `httpx.AsyncClient` (depending on your use-case):

```python
from galileo.api_client import GalileoApiClient

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = GalileoApiClient(
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client() or client.get_async_httpx_client()
```

You can even set the httpx client directly, but beware that this will override any existing settings (e.g., base_url):

```python
import httpx
from galileo.api_client import GalileoApiClient

client = GalileoApiClient()
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url=base_url, proxies="http://localhost:8030"))
```
