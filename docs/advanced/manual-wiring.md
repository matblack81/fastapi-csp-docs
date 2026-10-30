---
description: Write the docs routes yourself with the content generators, for page titles, disabled search and anything else setup() doesn't accept.
---

# Manual wiring

`setup()` is optional. The [content generators](../reference.md#content-generators) build the same pages, so you can write the routes yourself and pass what `setup()` doesn't accept, such as your own page titles or `disable_search=True`.

Each page needs its companion route. Swagger UI:

```python
--8<-- "docs_src/advanced/manual_wiring.py:swagger"
```

The OAuth2 redirect, needed only for OAuth2 login in Swagger UI:

```python
--8<-- "docs_src/advanced/manual_wiring.py:oauth2"
```

ReDoc:

```python
--8<-- "docs_src/advanced/manual_wiring.py:redoc"
```

Asset URLs you leave out take the [pinned defaults](pinned-versions.md).

## `root_path`

The generators use URLs as given. `setup()` adds the [`root_path`](reverse-proxy-and-sub-apps.md) on each request; in your own routes, read it from the request scope:

```python
--8<-- "docs_src/advanced/manual_wiring_root_path.py:snippet"
```

[`examples/self_hosted_manual_app.py`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/self_hosted_manual_app.py) wires every route with self-hosted assets.
