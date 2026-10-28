"""
Fully self-hosted docs, one unavoidable external origin for ReDoc's own logo.

fastapi_csp_docs.setup() wires the same routes as in the assisted examples, but its asset
URLs point at the vendor bundles served from /static instead of the CDN, so script-src stays
'self' with no external origins at all. Asset paths that start with "/" get the request's
root_path in front, so this keeps working when the app is mounted under a prefix. For the
same assets wired by hand, see self_hosted_manual_app.py.

Vendor bundles (swagger-ui-bundle.js, swagger-ui.css, redoc.standalone.js, favicon.png) are
committed under examples/static/ — nothing to download.

Run:

    uvicorn examples.self_hosted_app:app --reload

Then open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/redoc: both render fully, with
img-src the only directive listing an external origin (see REDOC_LOGO_URL below).
"""

from collections.abc import Awaitable, Callable
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

import fastapi_csp_docs

STATIC_DIR = Path(__file__).parent / "static"

# ReDoc's UI is built with styled-components, which injects <style> tags into the page at
# runtime regardless of how its HTML/CSS are served -- a ReDoc rendering requirement,
# unrelated to the inline <script>/<style> tags fastapi_csp_docs removes from FastAPI's own
# generated HTML. Allowed here via a CSP hash allowlist (capture the exact 'sha256-...'
# values Chrome reports as blocked, e.g. via DevTools console or a report-to endpoint), not
# 'unsafe-inline' -- this has to be redone whenever the ReDoc version changes. script-src
# stays 'self' with zero external origins, which is what "fully self-hosted" refers to here.
REDOC_STYLE_HASHES = (
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='",
    "'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='",
)

# ReDoc's "API docs by Redocly" logo hardcodes an absolute cdn.redoc.ly URL with no override
# option (https://github.com/Redocly/redoc/issues/2141). There's no CSP hash mechanism for
# images (hash-source only applies to script-src/style-src), so whitelisting the origin in
# img-src is the only way to allow it -- and since data: is already needed there for the small
# SVG icons the Swagger UI bundle inlines, adding one more explicit origin costs nothing extra
# in practice. This ends up being the one external origin in an otherwise fully self-hosted CSP.
REDOC_LOGO_URL = "https://cdn.redoc.ly/redoc/logo-mini.svg"

CSP = (
    "default-src 'self'; script-src 'self'; "
    f"style-src 'self' {' '.join(REDOC_STYLE_HASHES)}; "
    f"img-src 'self' data: {REDOC_LOGO_URL}; "
    # ReDoc runs its search indexing in a Web Worker instantiated from a blob: URL (the
    # worker's whole source is inlined as a string in redoc.standalone.js, there's no separate
    # file to point a real URL at instead), true regardless of whether redoc.standalone.js
    # itself is self-hosted or CDN-hosted. blob: is not an external origin. To drop it, wire
    # ReDoc by hand with get_redoc_html(disable_search=True) instead, as
    # self_hosted_manual_app.py does -- see the README section on worker-src.
    "worker-src 'self' blob:"
)

app = FastAPI(
    title="Self-Hosted CSP Docs API",
    docs_url=None,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.middleware("http")
async def add_csp_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = CSP
    return response


fastapi_csp_docs.setup(
    app,
    swagger_js_url="/static/swagger-ui-bundle.js",
    swagger_css_url="/static/swagger-ui.css",
    swagger_favicon_url="/static/favicon.png",
    redoc_js_url="/static/redoc.standalone.js",
    redoc_favicon_url="/static/favicon.png",
    google_fonts_css_url="/static/fonts.css",
)


@app.get("/items")
def list_items() -> dict[str, list[str]]:
    return {"items": []}
