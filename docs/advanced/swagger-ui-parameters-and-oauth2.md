---
description: The FastAPI app settings setup() reads for Swagger UI, from swagger_ui_parameters to the OAuth2 redirect URL.
---

# Swagger UI parameters and OAuth2

`setup()` has no Swagger UI options of its own: it reads FastAPI's app settings, so you configure them as in [FastAPI's guide](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/):

```python
--8<-- "docs_src/advanced/swagger_ui_options.py:snippet"
```

| App setting | Effect |
|---|---|
| `swagger_ui_parameters` | Merged over FastAPI's default parameters in `swagger-initializer.js` |
| `swagger_ui_init_oauth` | Passed to `ui.initOAuth()` |
| `swagger_ui_oauth2_redirect_url` | Path of the OAuth2 redirect page |

Every value reaches the script [JSON-escaped](../how-it-works.md#5-how-values-are-escaped).

## `swagger_ui_oauth2_redirect_url`

The redirect script is served next to the page, at the same path plus `.js`. The app above serves `/auth/callback` and `/auth/callback.js`, and `/docs/oauth2-redirect` returns 404.

With `swagger_ui_oauth2_redirect_url=None`, `setup()` registers neither route and the script omits `oauth2RedirectUrl`.

`setup()` registers the routes when it runs, so set this value before calling it. `swagger_ui_parameters` and `swagger_ui_init_oauth` are read on each request.

The full "Authorize" flow is in [`examples/oauth2_redirect_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/oauth2_redirect_app.py).
