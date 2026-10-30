---
description: Parameters, defaults and behavior of setup() and the content generators for manual wiring.
---

# Reference

::: fastapi_csp_docs.setup.setup

## Default asset URLs

`setup()` and the content generators share these defaults:

- `swagger_js_url`: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui-bundle.js`
- `swagger_css_url`: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui.css`
- `redoc_js_url`: `https://cdn.jsdelivr.net/npm/redoc@2.5.4/bundles/redoc.standalone.js`
- `swagger_favicon_url`, `redoc_favicon_url`: `https://fastapi.tiangolo.com/img/favicon.png`
- `google_fonts_css_url`: `https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700`

## Content generators

`setup()` builds each page and its companion script or stylesheet with these functions. Call them yourself to wire the routes by hand.

::: fastapi_csp_docs.get_swagger_ui_html

::: fastapi_csp_docs.get_swagger_ui_init_js

::: fastapi_csp_docs.get_swagger_ui_oauth2_redirect_html

::: fastapi_csp_docs.get_swagger_ui_oauth2_redirect_js

::: fastapi_csp_docs.get_redoc_html

::: fastapi_csp_docs.get_redoc_css
