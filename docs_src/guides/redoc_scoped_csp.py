from fastapi import FastAPI, Request
from fastapi.responses import Response

import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)

# --8<-- [start:snippet]
CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' https://cdn.jsdelivr.net; "
    "img-src 'self' data: https://fastapi.tiangolo.com; "
    "connect-src 'self' https://cdn.jsdelivr.net"
)
REDOC_CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' https://fonts.googleapis.com "
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' "
    "'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' https://fastapi.tiangolo.com https://cdn.redoc.ly; "
    "connect-src 'self' https://cdn.jsdelivr.net; "
    "worker-src 'self' blob:"
)


@app.middleware("http")
async def add_csp_header(request: Request, call_next) -> Response:
    response = await call_next(request)
    policy = REDOC_CSP if request.url.path == "/redoc" else CSP
    response.headers["Content-Security-Policy"] = policy
    return response
# --8<-- [end:snippet]


fastapi_csp_docs.setup(app)
