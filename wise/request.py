import functools

import requests

get = functools.partial(requests.get, timeout=10)
