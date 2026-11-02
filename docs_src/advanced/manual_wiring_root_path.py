from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)


# --8<-- [start:snippet]
@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(request: Request) -> HTMLResponse:
    root_path = request.scope.get("root_path", "").rstrip("/")
    return fastapi_csp_docs.get_swagger_ui_html(
        title="Items API reference",
        swagger_ui_init_script_url=f"{root_path}/docs/swagger-initializer.js",
    )


@app.get("/docs/swagger-initializer.js", include_in_schema=False)
async def swagger_ui_init_js(request: Request) -> Response:
    root_path = request.scope.get("root_path", "").rstrip("/")
    return fastapi_csp_docs.get_swagger_ui_init_js(
        openapi_url=f"{root_path}{app.openapi_url}",
        oauth2_redirect_url=f"{root_path}/docs/oauth2-redirect",
    )
# --8<-- [end:snippet]
