---
description: Six runnable apps, one per way of wiring fastapi-csp-docs.
---

# Examples

Every example is a complete, runnable app, imported and checked by the test suite. Run one with `uvicorn examples.<name>:app --reload` from a checkout of the repository; the docstring of each file lists the URLs to open.

## `assisted_app.py`

`setup()` with the CDN-hosted bundles and a CSP that lists the exact files.

??? example "Show the code"

    ```python
    --8<-- "examples/assisted_app.py"
    ```

`_csp.py` holds the CSP this app shares with `mounted_subapp_app.py` and `oauth2_redirect_app.py`:

??? example "Show the shared CSP"

    ```python
    --8<-- "examples/_csp.py"
    ```

## `self_hosted_app.py`

`setup()` with the vendor files in `examples/static/`.

??? example "Show the code"

    ```python
    --8<-- "examples/self_hosted_app.py"
    ```

## `self_hosted_manual_app.py`

The same files with every route written by hand, custom page titles and `disable_search=True`.

??? example "Show the code"

    ```python
    --8<-- "examples/self_hosted_manual_app.py"
    ```

## `mounted_subapp_app.py`

`setup()` on a sub-app mounted under `/api`.

??? example "Show the code"

    ```python
    --8<-- "examples/mounted_subapp_app.py"
    ```

## `oauth2_redirect_app.py`

OAuth2 "Authorize" flow through the redirect page.

??? example "Show the code"

    ```python
    --8<-- "examples/oauth2_redirect_app.py"
    ```

## `redoc_disable_search_app.py`

`setup()` for Swagger UI and a manual ReDoc route with `disable_search=True`.

??? example "Show the code"

    ```python
    --8<-- "examples/redoc_disable_search_app.py"
    ```
