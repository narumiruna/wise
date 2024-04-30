import functools

import httpx

get = functools.partial(httpx.get, timeout=10)
