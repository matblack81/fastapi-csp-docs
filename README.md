<p align="center">
  <img src="https://raw.githubusercontent.com/matblack81/fastapi-csp-docs/main/docs/assets/images/logo.svg" alt="FastAPI CSP Docs logo" width="128">
</p>

<h1 align="center">
  <img src="https://raw.githubusercontent.com/matblack81/fastapi-csp-docs/main/docs/assets/images/wordmark.png" alt="FastAPI CSP Docs" width="480">
</h1>

<p align="center">
  <a href="https://github.com/matblack81/fastapi-csp-docs/actions"><img src="https://github.com/matblack81/fastapi-csp-docs/workflows/Test/badge.svg" alt="Build Status"></a>
  <a href="https://codecov.io/gh/matblack81/fastapi-csp-docs"><img src="https://codecov.io/gh/matblack81/fastapi-csp-docs/graph/badge.svg" alt="codecov"></a>
  <a href="https://pypi.org/project/fastapi-csp-docs/"><img src="https://img.shields.io/pypi/v/fastapi-csp-docs?color=%2334D058&label=pypi%20package" alt="pypi package"></a>
  <a href="https://pypi.org/project/fastapi-csp-docs/"><img src="https://img.shields.io/pypi/pyversions/fastapi-csp-docs.svg?color=%2334D058" alt="Supported Python versions"></a>
  <a href="https://github.com/matblack81/fastapi-csp-docs/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
</p>

FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect pages embed inline `<script>`/`<style>` tags, so they break under a Content-Security-Policy without `'unsafe-inline'`. Following FastAPI's own ["Custom Docs UI Static Assets"](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) recipe only swaps the CDN URLs for local ones; the inline content stays. `fastapi-csp-docs` replaces all three pages with versions that load every script and stylesheet from a separate endpoint, with no inline content anywhere.

Documentation: https://fastapi-csp-docs.matblack81.com/

---

## Features

- **Drop-in `setup()`**: one call replaces the `/docs`, `/redoc`, and OAuth2 redirect wiring. See the [Quick start](https://fastapi-csp-docs.matblack81.com/quickstart/).
- **Fails at startup on misconfiguration**: `setup()` raises `RuntimeError` if the app's built-in docs are still enabled.
- **CDN or self-hosted**: the default asset URLs point at jsdelivr, and [your own static files](https://fastapi-csp-docs.matblack81.com/guides/self-hosted/) replace them with `script-src 'self'`.
- **Reverse proxy and sub-app support**: URLs include the ASGI `root_path` of each request, so [a mount or `--root-path`](https://fastapi-csp-docs.matblack81.com/advanced/reverse-proxy-and-sub-apps/) needs no configuration.
- **Independent paths**: `docs_url` and `redoc_url` are [`setup()` parameters](https://fastapi-csp-docs.matblack81.com/advanced/paths/), and `None` skips either page.
- **Public content generators**: the functions `setup()` uses are exported for [routes you write yourself](https://fastapi-csp-docs.matblack81.com/advanced/manual-wiring/).

---

## Requirements

- Python >= 3.10
- FastAPI >= 0.120.0

---

## Installation

```bash
pip install fastapi-csp-docs
# or
uv add fastapi-csp-docs
```

---

## Quick start

Create the app with its built-in docs disabled, send your Content-Security-Policy, and call `setup()`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import Response

import fastapi_csp_docs

CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com "
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' "
    "'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.redoc.ly; "
    "connect-src 'self' https://cdn.jsdelivr.net; "
    "worker-src 'self' blob:"
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.middleware("http")
async def add_csp_header(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = CSP
    return response


fastapi_csp_docs.setup(app)


@app.get("/items")
def list_items():
    return {"items": []}
```

The directives of this policy, self-hosted assets and the other options are in the [documentation](https://fastapi-csp-docs.matblack81.com/).

---

## Release Notes

[Release notes](https://fastapi-csp-docs.matblack81.com/changelog/)

---

## License

[MIT](https://github.com/matblack81/fastapi-csp-docs/blob/main/LICENSE)
