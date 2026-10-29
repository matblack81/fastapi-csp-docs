# FastAPI CSP Docs

[![Build Status](https://github.com/matblack81/fastapi-csp-docs/workflows/Test/badge.svg)](https://github.com/matblack81/fastapi-csp-docs/actions)
[![codecov](https://codecov.io/gh/matblack81/fastapi-csp-docs/graph/badge.svg)](https://codecov.io/gh/matblack81/fastapi-csp-docs)
[![pypi package](https://img.shields.io/pypi/v/fastapi-csp-docs?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-csp-docs/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fastapi-csp-docs.svg?color=%2334D058)](https://pypi.org/project/fastapi-csp-docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect pages embed inline `<script>`/`<style>` tags, so they break under a Content-Security-Policy without `'unsafe-inline'`. Following FastAPI's own ["Custom Docs UI Static Assets"](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) recipe only swaps the CDN URLs for local ones; it doesn't remove any inline content: `get_swagger_ui_html()` still embeds the Swagger UI bootstrap script inline, `get_redoc_html()` still embeds a `<style>` reset inline, and `get_swagger_ui_oauth2_redirect_html()` still embeds the OAuth2 redirect logic inline. `fastapi-csp-docs` replaces all three pages with versions that load every script and stylesheet from a separate endpoint, with no inline content anywhere.

## Features

- **Drop-in `setup()`**: one call replaces FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect wiring, with no inline script or style left anywhere.
- **Fails fast on misconfiguration**: raises `RuntimeError` if the app's built-in docs aren't disabled first, instead of silently letting them shadow the CSP-safe routes.
- **CDN or fully self-hosted**: works with the default jsdelivr CDN (`script-src 'self' <cdn-host>`) or entirely offline with your own static assets (`script-src 'self'`, zero external origins).
- **Reverse-proxy / sub-app aware**: doc URLs include the ASGI `root_path` computed per request, so mounting under a prefix (`app.mount("/api", sub_app)`) and running behind a reverse proxy that strips a prefix (server started with `--root-path`, see FastAPI's [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)) work out of the box.
- **Independently configurable mount paths**: `docs_url`/`redoc_url` are explicit `setup()` parameters, each can be disabled on its own by passing `None`.
- **Content generators exported for manual wiring**: the same building blocks `setup()` uses internally are public, for routes you want to write yourself.

## Requirements

- Python >= 3.10
- FastAPI >= 0.120.0

## Installation

```bash
pip install fastapi-csp-docs
# or
uv add fastapi-csp-docs
```

## Quick start

### Assisted mode (CDN-hosted Swagger UI / ReDoc)

```python
from fastapi import FastAPI, Request
from fastapi.responses import Response

import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)


@app.middleware("http")
async def add_csp_header(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' https://cdn.jsdelivr.net"
    )
    return response


fastapi_csp_docs.setup(app)
```

`docs_url`/`redoc_url` must already be `None` on the app for whichever mode you're enabling. `setup()` raises `RuntimeError` otherwise, so FastAPI's built-in inline-script docs can't silently shadow the routes it registers.

The default asset URLs pin exact releases: `swagger-ui-dist@5.34.0` and `redoc@2.5.4` on jsdelivr. FastAPI's own defaults use the floating `@5`/`@2` tags instead. With a pinned version, the files the browser loads only change when you upgrade `fastapi-csp-docs`, so the CSP entries that depend on them (full file URLs, as listed in [`examples/_csp.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/_csp.py), and the ReDoc style hashes) keep matching until then. When you upgrade, check the release notes for a version bump and update those entries.

Full runnable version: [`examples/assisted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/assisted_app.py).

### Fully self-hosted mode (no CDN at all)

For a CSP with zero external script or style origins (`script-src 'self'`), serve the vendor bundles yourself and point `setup()` at them:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

fastapi_csp_docs.setup(
    app,
    swagger_js_url="/static/swagger-ui-bundle.js",
    swagger_css_url="/static/swagger-ui.css",
    swagger_favicon_url="/static/favicon.png",
    redoc_js_url="/static/redoc.standalone.js",
    redoc_favicon_url="/static/favicon.png",
    google_fonts_css_url="/static/fonts.css",
)
```

An asset URL that starts with a single `/` is a path on the app, so `setup()` puts the request's ASGI `root_path` in front of it, as it does for the docs routes: with the app mounted under `/api`, `/static/swagger-ui-bundle.js` is served as `/api/static/swagger-ui-bundle.js`. FastAPI's own docs functions use asset URLs as given. Absolute (`https://...`), protocol-relative (`//...`) and relative URLs are used as given here too.

Full runnable version, including the vendor assets and the CSP: [`examples/self_hosted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_app.py).

### Manual wiring

`setup()` is optional. The content generators listed in the [reference](#content-generators-manual-wiring) build the same pages, so you can register the routes yourself, with the same mechanics as FastAPI's own ["Custom Docs UI Static Assets"](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) recipe but without inline content in the OAuth2 redirect page either:

```python
@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return fastapi_csp_docs.get_swagger_ui_html(
        title=f"{app.title} - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_init_script_url="/docs/swagger-initializer.js",
    )
```

Each page then needs its companion route too (`swagger-initializer.js`, `redoc.css`, the OAuth2 redirect script), and the `root_path` handling `setup()` does is up to you. In exchange you can pass what `setup()` doesn't, such as `disable_search=True` for ReDoc or your own page titles. [`examples/self_hosted_manual_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_manual_app.py) wires every route this way, and [`examples/redoc_disable_search_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/redoc_disable_search_app.py) only the ReDoc one.

## ReDoc and Content-Security-Policy

Beyond the inline `<script>`/`<style>` tags this package removes from FastAPI's own generated HTML, ReDoc's *own* runtime does three more things that need explicit CSP entries. Both examples above already handle these (`examples/_csp.py` for the CDN-based ones, `examples/self_hosted_app.py` for the fully self-hosted one); this section explains why.

**Inline styles (`style-src`)**: ReDoc is built with `styled-components`, which injects `<style>` tags into the page at runtime instead of shipping one static stylesheet. This is unrelated to the inline content `fastapi-csp-docs` removes: it's ReDoc's own rendering mechanism, and this package can't eliminate it. A CSP hash allowlist is used to allow them without `'unsafe-inline'`: open DevTools, note the exact `'sha256-...'` value(s) the browser reports as blocked, and add them to `style-src`. These hashes are tied to the exact ReDoc build, so they need to be recaptured whenever `redoc.standalone.js` is upgraded.

**Web Worker (`worker-src`)**: ReDoc runs its search indexing in a Web Worker, instantiated from a `blob:` URL rather than a separate `.js` file: the worker's entire source is inlined as a string inside `redoc.standalone.js`, so there's no real file URL to point `worker-src` at instead. Worker instantiation is governed by `worker-src`, not `script-src`; without it set explicitly, browsers fall back to `script-src`, which never matches a `blob:` URL, so search breaks the first time it's used (`Creating a worker from 'blob:...' violates ... worker-src`). Two ways to fix it:
- Allow it explicitly: `worker-src 'self' blob:`, which is what `assisted_app.py`, `self_hosted_app.py` and the other `setup()`-based examples do, since `setup()` has no CSP-specific parameters and no way to turn search off.
- Or skip the worker (and the search box) entirely by not using `setup()` for the ReDoc route: pass `redoc_url=None` to `setup()` and wire `/redoc` yourself with `get_redoc_html(disable_search=True)` instead, so no `blob:` is needed in `worker-src`. See [`examples/redoc_disable_search_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/redoc_disable_search_app.py).

**Logo image (`img-src`)**: ReDoc's "API docs by Redocly" attribution logo hardcodes an absolute `cdn.redoc.ly` URL, with no supported way to override it or point it at a local file. There's no CSP hash mechanism for images (hash-source only applies to `script-src`/`style-src`), so the only way to allow it is whitelisting that origin in `img-src`; both examples do this, since it's a small, non-code image request and doesn't weaken `script-src`/`style-src` at all. It's the one external origin left in `self_hosted_app.py`'s otherwise fully self-hosted CSP.

**Scoping these entries to the ReDoc page**: all three are needed only by the ReDoc page, and the browser enforces the CSP sent with that HTML response, not the one sent with the scripts and stylesheets it loads. An app that already sets its CSP in a middleware can add them only to the response for `redoc_url` (`/redoc` by default) and keep every other route on the stricter policy. The examples send one policy with every response to stay short.

## Reference

### `setup(app, *, docs_url="/docs", redoc_url="/redoc", ...)`

| Parameter              | Type          | Default   | Description |
|------------------------|---------------|-----------|-------------|
| `app`                  | `FastAPI`     | required  | The app to wire the CSP-safe docs routes onto. Must be created with `docs_url=None`/`redoc_url=None` for whichever of the two this call sets up. |
| `docs_url`             | `str \| None` | `"/docs"` | Path to serve Swagger UI at, or `None` to skip it. |
| `redoc_url`            | `str \| None` | `"/redoc"`| Path to serve ReDoc at, or `None` to skip it. |
| `swagger_js_url`       | `str`         | `"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui-bundle.js"` | URL of the Swagger UI JavaScript bundle. |
| `swagger_css_url`      | `str`         | `"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui.css"` | URL of the Swagger UI CSS. |
| `swagger_favicon_url`  | `str`         | `"https://fastapi.tiangolo.com/img/favicon.png"` | URL of the Swagger UI page's favicon. |
| `redoc_js_url`         | `str`         | `"https://cdn.jsdelivr.net/npm/redoc@2.5.4/bundles/redoc.standalone.js"` | URL of the ReDoc JavaScript bundle. |
| `redoc_favicon_url`    | `str`         | `"https://fastapi.tiangolo.com/img/favicon.png"` | URL of the ReDoc page's favicon. |
| `with_google_fonts`    | `bool`        | `True`    | Whether the ReDoc page loads the stylesheet at `google_fonts_css_url`. |
| `google_fonts_css_url` | `str`         | `"https://fonts.googleapis.com/css?family=Montserrat:300,400,700\|Roboto:300,400,700"` | URL of the Montserrat/Roboto stylesheet for ReDoc. |

The asset URLs that start with a single `/` get the request's ASGI `root_path` in front of them, see [Fully self-hosted mode](#fully-self-hosted-mode-no-cdn-at-all).

Raises `RuntimeError` if `app.docs_url`/`app.redoc_url` is still set for the mode being enabled.

### Content generators (manual wiring)

| Function                                | Returns                          | Purpose                                                                    |
|------------------------------------------|-----------------------------------|-----------------------------------------------------------------------------|
| `get_swagger_ui_html`                    | `HTMLResponse`                   | Swagger UI page, referencing an external init script instead of inline JS. |
| `get_swagger_ui_init_js`                 | `Response` (`text/javascript`)   | Swagger UI bootstrap script, with HTML-escaped JSON config.                |
| `get_swagger_ui_oauth2_redirect_html`     | `HTMLResponse`                   | OAuth2 redirect page, referencing an external script instead of inline JS. |
| `get_swagger_ui_oauth2_redirect_js`       | `Response` (`text/javascript`)   | OAuth2 redirect handshake logic.                                           |
| `get_redoc_html`                         | `HTMLResponse`                   | ReDoc page, referencing an external stylesheet instead of inline `<style>`. Takes `disable_search` to drop the search box/Web Worker, see "ReDoc and Content-Security-Policy" above. |
| `get_redoc_css`                          | `Response` (`text/css`)          | Minimal CSS reset ReDoc needs.                                             |

## Examples

| File                                                                                                                      | Description                                                                                     |
|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [`examples/assisted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/assisted_app.py)             | `setup()` + CDN-hosted Swagger UI/ReDoc bundles, CSP header set via middleware.                    |
| [`examples/self_hosted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_app.py)       | Fully self-hosted docs (no CDN): `setup()` with asset URLs pointing at the vendor assets served from `examples/static/`. |
| [`examples/self_hosted_manual_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_manual_app.py) | The same self-hosted assets with every route wired by hand, for ReDoc's `disable_search=True` (no `blob:` in `worker-src`) and custom page titles. |
| [`examples/mounted_subapp_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/mounted_subapp_app.py) | `setup()` on a sub-app mounted under a prefix (`app.mount("/api", sub_app)`), so doc URLs resolve correctly via the ASGI `root_path`. |
| [`examples/oauth2_redirect_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/oauth2_redirect_app.py) | OAuth2 "Authorize" flow with a real security scheme, exercising the `/docs/oauth2-redirect` endpoint `setup()` registers. |
| [`examples/redoc_disable_search_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/redoc_disable_search_app.py) | `setup()` for Swagger UI + manual ReDoc wiring with `disable_search=True`, avoiding `worker-src 'self' blob:` entirely. |

## Release Notes

See [RELEASE_NOTES](https://github.com/matblack81/fastapi-csp-docs/blob/main/release-notes.md).

## License

MIT. See [LICENSE](https://github.com/matblack81/fastapi-csp-docs/blob/main/LICENSE).
