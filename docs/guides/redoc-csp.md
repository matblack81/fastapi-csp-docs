---
description: The three CSP entries ReDoc's own runtime needs, and how to keep them on the ReDoc page.
---

# ReDoc and CSP

ReDoc's runtime does three things that need CSP entries, whatever URL its bundle comes from. `fastapi-csp-docs` can't remove them, and `setup()` has no CSP parameters: the entries go in your policy.

## Inline styles

ReDoc is built with `styled-components`, which injects `<style>` tags into the page at runtime. Hashes in `style-src` allow them without `'unsafe-inline'`. For `redoc@2.5.4` the hashes are:

```text
'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='
'sha256-QMIg+bpjm3JdElJ388KYke01izlUW0UoNOeKjpMxdgc='
```

The hashes depend on the ReDoc build. With another `redoc.standalone.js`, open the page with DevTools and copy the `'sha256-...'` values the browser reports as blocked.

## Web Worker

ReDoc indexes its search in a Web Worker created from a `blob:` URL: the source of the worker is a string inside `redoc.standalone.js`, so no file URL exists to allow instead. `worker-src` governs the worker and falls back to `script-src`, which never matches a `blob:` URL, so without an explicit entry the page logs a violation (`Creating a worker from 'blob:...' violates ... worker-src`) and search breaks.

Allow it with `worker-src 'self' blob:`, or remove search. `setup()` can't turn search off, so pass `redoc_url=None` and write the ReDoc routes with `get_redoc_html(disable_search=True)`:

```python
--8<-- "docs_src/guides/redoc_disable_search.py:snippet"
```

The page then has no search box and creates no worker, so the policy needs no `worker-src`. The full app is [`examples/redoc_disable_search_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/redoc_disable_search_app.py).

## Logo image

ReDoc's "API docs by Redocly" logo is a hardcoded `cdn.redoc.ly` URL with no option to change it. CSP hashes don't apply to images, so the only way to allow the logo is the origin in `img-src`: `https://cdn.redoc.ly`, or `https://cdn.redoc.ly/redoc/logo-mini.svg` for the exact file.

## Scoping the entries to the ReDoc page

The browser enforces the CSP sent with the HTML response, not the one sent with the scripts and stylesheets the page loads. An app that sets its CSP in a middleware can send the ReDoc entries with `/redoc` alone and keep every other route on the stricter policy:

```python
--8<-- "docs_src/guides/redoc_scoped_csp.py:snippet"
```
