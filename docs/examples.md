---
description: Complete FastAPI apps that use fastapi-csp-docs, runnable with uvicorn from the repository.
---

# Examples

Each file is a complete app in the [`examples/`](https://github.com/matblack81/fastapi-csp-docs/tree/main/examples) directory. From a clone of the repository, run one with:

```bash
uvicorn examples.assisted_app:app --reload
```

| File | Description |
|---|---|
| [`assisted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/assisted_app.py) | `setup()` with the CDN-hosted bundles and a CSP that lists the exact files |
| [`self_hosted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_app.py) | `setup()` with the vendor files in `examples/static/` |
| [`self_hosted_manual_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_manual_app.py) | The same files with every route written by hand, custom page titles and `disable_search=True` |
| [`mounted_subapp_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/mounted_subapp_app.py) | `setup()` on a sub-app mounted under `/api` |
| [`oauth2_redirect_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/oauth2_redirect_app.py) | OAuth2 "Authorize" flow through the redirect page |
| [`redoc_disable_search_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/redoc_disable_search_app.py) | `setup()` for Swagger UI and a manual ReDoc route with `disable_search=True` |
