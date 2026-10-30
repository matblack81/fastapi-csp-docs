from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

import fastapi_csp_docs

CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com "
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' "
    "'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.redoc.ly; "
    "connect-src 'self' https://cdn.jsdelivr.net"
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.middleware("http")
async def add_csp_header(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = CSP
    return response


# --8<-- [start:snippet]
fastapi_csp_docs.setup(app, redoc_url=None)


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    return fastapi_csp_docs.get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_css_url="/redoc/redoc.css",
        disable_search=True,
    )


@app.get("/redoc/redoc.css", include_in_schema=False)
async def redoc_css() -> Response:
    return fastapi_csp_docs.get_redoc_css()
# --8<-- [end:snippet]
