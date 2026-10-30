---
description: What setup() checks and registers, how each request builds its URLs, and what the browser loads.
---

# How it works

`setup()` runs once and registers routes on your app. The pages those routes return contain only references to external files.

## 1. What `setup()` checks

For each page it is asked to set up, `setup()` raises `RuntimeError` if the app's matching attribute (`app.docs_url` or `app.redoc_url`) is still set. Otherwise FastAPI's built-in page would serve the same path with its inline content.

If `app.openapi_url` is `None`, there is no schema to render, and `setup()` skips the page with no warning, as FastAPI does.

## 2. What `setup()` registers

Each page gets a companion route for the content FastAPI embeds inline:

| Page | Companion route | Content moved out of the page |
|---|---|---|
| `docs_url` | `{docs_url}/swagger-initializer.js` | The `SwaggerUIBundle(...)` startup script |
| `swagger_ui_oauth2_redirect_url` | `{swagger_ui_oauth2_redirect_url}.js` | The OAuth2 redirect logic |
| `redoc_url` | `{redoc_url}/redoc.css` | The CSS reset |

The redirect routes exist only while Swagger UI is set up and `app.swagger_ui_oauth2_redirect_url` is set. All the routes are registered with `include_in_schema=False`.

## 3. What happens on each request

Each page handler reads `root_path` from the request's ASGI scope and builds its URLs from it: the companion route, the schema URL, and any [asset URL that starts with a single `/`](guides/self-hosted.md#urls-under-a-prefix). The same app can therefore answer under different prefixes with no configuration.

The Swagger UI script reads `app.swagger_ui_parameters`, `app.swagger_ui_init_oauth` and `app.swagger_ui_oauth2_redirect_url` on each request. The route paths are fixed when `setup()` runs. The OAuth2 redirect script and `redoc.css` have no dynamic content, so each response is built once and reused.

## 4. What the browser loads

For Swagger UI, in order:

1. `/docs` returns HTML with a `<link>` to `swagger-ui.css` and two `<script src=...>` tags.
2. The browser loads `swagger-ui-bundle.js`, which defines `SwaggerUIBundle`.
3. It loads `swagger-initializer.js`, which starts Swagger UI on the schema URL.

For ReDoc, `/redoc` returns HTML with a `<redoc spec-url=...>` element, a `<link>` to `redoc.css`, one to the fonts stylesheet, and a `<script src=...>` tag for `redoc.standalone.js`. ReDoc's bundle then does the work that [needs its own CSP entries](guides/redoc-csp.md).

Every step is a separate request to a URL, so `script-src` and `style-src` can match each one without `'unsafe-inline'`.

## 5. How values are escaped

The JSON in `swagger-initializer.js` is serialized with `<`, `>` and `&` written as `<`, `>` and `&`. The values interpolated into the HTML pages go through `html.escape()`.
