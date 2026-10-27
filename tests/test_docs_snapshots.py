from inline_snapshot import snapshot

import fastapi_csp_docs

# What each generator emits with its default arguments. None of it depends on the FastAPI or
# Pydantic version, so it holds across the whole matrix; get_swagger_ui_init_js is left out
# because it embeds FastAPI's swagger_ui_default_parameters. Regenerate with
# `pytest tests/test_docs_snapshots.py --inline-snapshot=fix` and read the diff.
PAGES = snapshot(
    {
        "swagger_ui_html": """\

    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Test - Swagger UI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    </head>
    <body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script src="/docs/swagger-initializer.js" charset="UTF-8"></script>
    </body>
    </html>
    \
""",
        "redoc_html": """\

    <!DOCTYPE html>
    <html>
    <head>
    <title>Test - ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    \n\
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    \n\
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <link rel="stylesheet" type="text/css" href="/redoc/redoc.css">
    <!--
    ReDoc doesn't change outer page styles
    -->
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="/openapi.json"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js"> </script>
    </body>
    </html>
    \
""",
        "redoc_html_disable_search": """\

    <!DOCTYPE html>
    <html>
    <head>
    <title>Test - ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    \n\
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    \n\
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <link rel="stylesheet" type="text/css" href="/redoc/redoc.css">
    <!--
    ReDoc doesn't change outer page styles
    -->
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="/openapi.json" disable-search="true"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js"> </script>
    </body>
    </html>
    \
""",
        "swagger_ui_oauth2_redirect_html": """\

    <!doctype html>
    <html lang="en-US">
    <head>
        <title>Swagger UI: OAuth2 Redirect</title>
    </head>
    <body>
    <script src="oauth2-redirect.js"></script>
    </body>
    </html>
    \
""",
        "swagger_ui_oauth2_redirect_js": '"use strict";function run(){var e,r,t,a=window.opener.swaggerUIRedirectOauth2,o=a.state,n=a.redirectUrl;if((t=(r=/code|token|error/.test(window.location.hash)?window.location.hash.substring(1).replace("?","&"):location.search.substring(1)).split("&")).forEach((function(e,r,t){t[r]=\'"\'+e.replace("=",\'":"\')+\'"\'})),e=(r=r?JSON.parse("{"+t.join()+"}",(function(e,r){return""===e?r:decodeURIComponent(r)})):{}).state===o,"accessCode"!==a.auth.schema.get("flow")&&"authorizationCode"!==a.auth.schema.get("flow")&&"authorization_code"!==a.auth.schema.get("flow")||a.auth.code)a.callback({auth:a.auth,token:r,isValid:e,redirectUrl:n});else if(e||a.errCb({authId:a.auth.name,source:"auth",level:"warning",message:"Authorization may be unsafe, passed state was changed in server Passed state wasn\'t returned from auth server"}),r.code)delete a.state,a.auth.code=r.code,a.callback({auth:a.auth,redirectUrl:n});else{let e;r.error&&(e="["+r.error+"]: "+(r.error_description?r.error_description+". ":"no accessCode received from the server. ")+(r.error_uri?"More info: "+r.error_uri:"")),a.errCb({authId:a.auth.name,source:"auth",level:"error",message:e||"[Authorization failed]: no accessCode received from the server"})}window.close()}"loading"!==document.readyState?run():document.addEventListener("DOMContentLoaded",(function(){run()}));',
    }
)


def _generated_pages() -> dict[str, str]:
    responses = {
        "swagger_ui_html": fastapi_csp_docs.get_swagger_ui_html(title="Test - Swagger UI"),
        "redoc_html": fastapi_csp_docs.get_redoc_html(openapi_url="/openapi.json", title="Test - ReDoc"),
        "redoc_html_disable_search": fastapi_csp_docs.get_redoc_html(
            openapi_url="/openapi.json", title="Test - ReDoc", disable_search=True
        ),
        "swagger_ui_oauth2_redirect_html": fastapi_csp_docs.get_swagger_ui_oauth2_redirect_html(),
        "swagger_ui_oauth2_redirect_js": fastapi_csp_docs.get_swagger_ui_oauth2_redirect_js(),
    }
    return {name: bytes(response.body).decode() for name, response in responses.items()}


def test_generated_pages_match_snapshot():
    assert _generated_pages() == PAGES
