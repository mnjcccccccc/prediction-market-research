"""Small bounded HTTP transport. Retries apply only to public, idempotent GETs."""

import json
import random
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class APIError(RuntimeError):
    pass


class JsonHTTP:
    def __init__(self, timeout: float = 20, retries: int = 2):
        self.timeout = timeout
        self.retries = retries

    def get(self, base: str, params: dict | None = None):
        url = base + ("?" + urlencode(params) if params else "")
        for attempt in range(self.retries + 1):
            try:
                req = Request(
                    url,
                    headers={
                        "User-Agent": "prediction-market-research/0.1 (public research)",
                        "Accept": "application/json",
                    },
                )
                with urlopen(req, timeout=self.timeout) as response:
                    return json.load(response)
            except HTTPError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt == self.retries:
                    raise APIError(f"GET {base}: HTTP {exc.code}") from None
                retry_after = exc.headers.get("Retry-After", "")
                delay = min(float(retry_after), 10) if retry_after.isdigit() else 2**attempt
            except (URLError, TimeoutError, OSError) as exc:
                if attempt == self.retries:
                    raise APIError(f"GET {base}: {type(exc).__name__}") from None
                delay = 2**attempt
            except (ValueError, UnicodeError):
                raise APIError(f"GET {base}: invalid JSON response") from None
            time.sleep(delay + random.uniform(0, 0.2))
        raise APIError("Retry budget exhausted")
