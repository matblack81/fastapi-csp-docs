from fastapi import FastAPI, Request
from fastapi.responses import Response

# --8<-- [start:snippet]
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
# --8<-- [end:snippet]


@app.get("/items")
def list_items():
    return {"items": []}
