---
description: Serve the Swagger UI and ReDoc bundles from your own app, with script-src 'self' and no CDN.
---

# Fully self-hosted docs

Serve the vendor files from your app and pass their URLs to `setup()`. `script-src` then falls back to `default-src 'self'`, with no external origin:

```python
--8<-- "docs_src/guides/self_hosted.py:snippet"
```

`STATIC_DIR` holds these files. [`examples/static/`](https://github.com/matblack81/fastapi-csp-docs/tree/main/examples/static) has a copy of each, at the versions `setup()` loads by default:

| File | `setup()` parameter |
|---|---|
| `swagger-ui-bundle.js` | `swagger_js_url` |
| `swagger-ui.css` | `swagger_css_url` |
| `redoc.standalone.js` | `redoc_js_url` |
| `favicon.png` | `swagger_favicon_url`, `redoc_favicon_url` |
| `fonts.css` and `fonts/` | `google_fonts_css_url` |

The only external origin left in the policy is `https://cdn.redoc.ly` in `img-src`, for [ReDoc's logo](redoc-csp.md#logo-image). The two hashes and `worker-src 'self' blob:` serve [ReDoc's own runtime](redoc-csp.md), wherever its bundle comes from.

## URLs under a prefix

`setup()` puts the request's ASGI `root_path` in front of an asset URL that starts with a single `/`. With the app mounted under `/api`, `/static/swagger-ui-bundle.js` becomes `/api/static/swagger-ui-bundle.js`. FastAPI's own docs functions use asset URLs as given.

Absolute (`https://...`), protocol-relative (`//...`) and relative URLs are used as given.

The full app is [`examples/self_hosted_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_app.py).
