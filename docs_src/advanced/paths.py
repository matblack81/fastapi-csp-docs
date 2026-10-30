from fastapi import FastAPI

import fastapi_csp_docs

# --8<-- [start:snippet]
app = FastAPI(docs_url=None, redoc_url=None)

fastapi_csp_docs.setup(app, docs_url="/api-docs", redoc_url=None)
# --8<-- [end:snippet]
