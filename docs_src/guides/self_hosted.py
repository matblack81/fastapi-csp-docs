from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response

STATIC_DIR = Path(__file__).parents[2] / "examples" / "static"

# --8<-- [start:snippet]
from fastapi.staticfiles import StaticFiles

import fastapi_csp_docs

CSP = (
    "default-src 'self'; "
    "style-src 'self' "
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' "
    "'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='; "
    "img-src 'self' data: https://cdn.redoc.ly; "
    "worker-src 'self' blob:"
)

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.middleware("http")
async def add_csp_header(request: Request, call_next) -> Response:
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
# --8<-- [end:snippet]


@app.get("/items")
def list_items():
    return {"items": []}
