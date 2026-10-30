from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

# --8<-- [start:swagger]
import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    return fastapi_csp_docs.get_swagger_ui_html(
        title="Items API reference",
        swagger_ui_init_script_url="/docs/swagger-initializer.js",
    )


@app.get("/docs/swagger-initializer.js", include_in_schema=False)
async def swagger_ui_init_js() -> Response:
    return fastapi_csp_docs.get_swagger_ui_init_js(
        openapi_url=app.openapi_url,
        oauth2_redirect_url="/docs/oauth2-redirect",
    )
# --8<-- [end:swagger]


# --8<-- [start:oauth2]
@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def oauth2_redirect_html() -> HTMLResponse:
    return fastapi_csp_docs.get_swagger_ui_oauth2_redirect_html(
        oauth2_redirect_script_url="/docs/oauth2-redirect.js",
    )


@app.get("/docs/oauth2-redirect.js", include_in_schema=False)
async def oauth2_redirect_js() -> Response:
    return fastapi_csp_docs.get_swagger_ui_oauth2_redirect_js()
# --8<-- [end:oauth2]


# --8<-- [start:redoc]
@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    return fastapi_csp_docs.get_redoc_html(
        openapi_url=app.openapi_url,
        title="Items API guide",
        redoc_css_url="/redoc/redoc.css",
        disable_search=True,
    )


@app.get("/redoc/redoc.css", include_in_schema=False)
async def redoc_css() -> Response:
    return fastapi_csp_docs.get_redoc_css()
# --8<-- [end:redoc]
