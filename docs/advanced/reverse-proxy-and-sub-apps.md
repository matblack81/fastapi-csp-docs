---
description: How the docs pages follow the ASGI root_path when the app is mounted under a prefix or runs behind a reverse proxy.
---

# Reverse proxy and sub-apps

Each request builds its URLs from the ASGI `root_path`, so `setup()` takes no prefix parameter.

## Mounted sub-apps

Call `setup()` on the sub-app. It doesn't need to know where it gets mounted:

```python
--8<-- "docs_src/advanced/sub_app.py:snippet"
```

| URL | Response |
|---|---|
| `/api/docs` | Swagger UI, loading `/api/docs/swagger-initializer.js` |
| `/api/docs/swagger-initializer.js` | Script with the schema at `/api/openapi.json` and the redirect at `/api/docs/oauth2-redirect` |
| `/api/redoc` | ReDoc, with the schema at `/api/openapi.json` and the CSS at `/api/redoc/redoc.css` |

The full app is [`examples/mounted_subapp_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/mounted_subapp_app.py).

## Behind a reverse proxy

For a proxy that strips a path prefix, start the server with that prefix, as FastAPI's [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) guide describes:

```bash
uvicorn main:app --root-path /api
```

The pages then produce the same URLs as under a mount.

## Asset URLs

Asset URLs that start with a single `/` get the prefix too. See [URLs under a prefix](../guides/self-hosted.md#urls-under-a-prefix).
