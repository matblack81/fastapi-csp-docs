---
description: Serve Swagger UI and ReDoc at custom paths with docs_url and redoc_url, or skip either page with None.
---

# Paths and disabling a page

`docs_url` and `redoc_url` default to `"/docs"` and `"/redoc"`. Pass another path to move a page, or `None` to skip it:

```python
--8<-- "docs_src/advanced/paths.py:snippet"
```

| URL | Response |
|---|---|
| `/api-docs` | Swagger UI |
| `/api-docs/swagger-initializer.js` | Its startup script |
| `/docs/oauth2-redirect` | OAuth2 redirect page |
| `/docs` | 404 |
| `/redoc` | 404 |

## OAuth2 redirect path

The redirect routes follow `swagger_ui_oauth2_redirect_url`, a FastAPI app setting with the default `"/docs/oauth2-redirect"`, not `docs_url`. To move them too, see [`swagger_ui_oauth2_redirect_url`](swagger-ui-parameters-and-oauth2.md#swagger_ui_oauth2_redirect_url).

## `None` leaves the built-in page alone

`setup()` only checks the pages it sets up. With `FastAPI(docs_url=None)` and `setup(app, redoc_url=None)`, `FastAPI` keeps its default `redoc_url`, so `/redoc` is FastAPI's built-in page with its inline `<style>`, and the browser blocks it under your CSP. Set both to `None` on the app to serve neither.
