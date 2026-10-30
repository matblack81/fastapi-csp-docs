from fastapi import FastAPI

import fastapi_csp_docs

# --8<-- [start:snippet]
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    swagger_ui_parameters={"docExpansion": "none", "tryItOutEnabled": True},
    swagger_ui_init_oauth={"clientId": "docs-client", "usePkceWithAuthorizationCodeGrant": True},
    swagger_ui_oauth2_redirect_url="/auth/callback",
)

fastapi_csp_docs.setup(app)
# --8<-- [end:snippet]
