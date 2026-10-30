---
description: What each Content-Security-Policy directive does for the Swagger UI and ReDoc pages, and how to pin it to exact files.
---

# Writing the CSP

`fastapi-csp-docs` sends no CSP header: your app sets it. The policy in the [Quick start](../quickstart.md) covers both pages with the default asset URLs:

| Directive | Entries | Needed by |
|---|---|---|
| `default-src` | `'self'` | Everything without its own directive, including the app's schema and the generated script and CSS routes |
| `script-src` | `https://cdn.jsdelivr.net` | The Swagger UI and ReDoc bundles |
| `style-src` | `https://cdn.jsdelivr.net` | `swagger-ui.css` |
| `style-src` | `https://fonts.googleapis.com` | The stylesheet of [ReDoc's fonts](../advanced/fonts.md) |
| `style-src` | Two `'sha256-...'` hashes | [ReDoc's runtime styles](redoc-csp.md#inline-styles) |
| `font-src` | `https://fonts.gstatic.com` | The font files of that stylesheet |
| `img-src` | `data:` | SVG icons the Swagger UI bundle inlines |
| `img-src` | `https://fastapi.tiangolo.com` | The default favicon |
| `img-src` | `https://cdn.redoc.ly` | [ReDoc's logo](redoc-csp.md#logo-image) |
| `connect-src` | `https://cdn.jsdelivr.net` | The source maps of `swagger-ui.css` and `redoc.standalone.js`, which browser developer tools fetch when you inspect a source file |
| `worker-src` | `'self' blob:` | [ReDoc's search worker](redoc-csp.md#web-worker) |

## Pinning exact files

`https://cdn.jsdelivr.net` allows every package hosted on jsdelivr. Listing the exact files limits the policy to the bundles the pages load, as in [`examples/_csp.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/_csp.py). Google serves font files under version-hashed names, so `https://fonts.gstatic.com/s/` is the closest match for `font-src`.

The [default asset URLs](../advanced/pinned-versions.md) contain the exact Swagger UI and ReDoc versions, so these entries keep matching until an upgrade of `fastapi-csp-docs` changes the versions.

## Page-specific entries

The browser enforces the CSP sent with the HTML response, so the ReDoc entries can stay on the ReDoc page. See [Scoping the entries to the ReDoc page](redoc-csp.md#scoping-the-entries-to-the-redoc-page).
