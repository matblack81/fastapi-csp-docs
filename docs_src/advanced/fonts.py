from fastapi import FastAPI

import fastapi_csp_docs

app = FastAPI(docs_url=None, redoc_url=None)

# --8<-- [start:snippet]
fastapi_csp_docs.setup(app, with_google_fonts=False)
# --8<-- [end:snippet]
