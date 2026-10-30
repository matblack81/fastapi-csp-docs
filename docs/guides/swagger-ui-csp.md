---
description: The CSP entries Swagger UI needs, and the style-src-attr violations caused by Markdown in OpenAPI descriptions.
---

# Swagger UI and CSP

Swagger UI needs no CSP entries beyond its asset URLs, listed in [Writing the CSP](csp.md). It sets its inline styles through the CSSOM (`element.style`), which `style-src` doesn't govern.

## Markdown in descriptions

Swagger UI renders the Markdown in your OpenAPI `description` fields as HTML. A table with aligned columns (`| :---: |`) becomes `<th style="text-align:center">`, and raw HTML can carry its own `style` attributes. Under a `style-src` without `'unsafe-inline'`, the browser drops these attributes and logs a `style-src-attr` violation every time the page re-renders. The text still shows, without that alignment or styling.

| To | Do |
|---|---|
| Avoid the violations | Remove the alignment markers and `style` attributes from your descriptions |
| Keep the styling | Add the hashes the browser reports to `style-src`, together with `'unsafe-hashes'`, which hashes of style attributes require |
