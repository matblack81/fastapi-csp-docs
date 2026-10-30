from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

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
# --8<-- [end:snippet]
