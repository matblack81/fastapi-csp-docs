---
description: CSP-safe replacements for FastAPI's built-in /docs, /redoc, and OAuth2 redirect endpoints, with no inline script or style.
---

# FastAPI CSP Docs

FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect pages embed inline `<script>`/`<style>` tags, so they break under a Content-Security-Policy without `'unsafe-inline'`. `fastapi-csp-docs` replaces all three pages with versions that load every script and stylesheet from a separate endpoint, with no inline content anywhere.

## Installation

=== "pip"

    ```bash
    pip install fastapi-csp-docs
    ```

=== "uv"

    ```bash
    uv add fastapi-csp-docs
    ```

The [README on GitHub](https://github.com/matblack81/fastapi-csp-docs#readme) has the quick start and the CSP each mode needs. The [reference](reference.md) lists every parameter.
