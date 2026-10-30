from fastapi import FastAPI

# --8<-- [start:snippet]
import fastapi_csp_docs

sub_app = FastAPI(docs_url=None, redoc_url=None)
fastapi_csp_docs.setup(sub_app)

app = FastAPI()
app.mount("/api", sub_app)
# --8<-- [end:snippet]
