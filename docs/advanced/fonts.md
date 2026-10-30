---
description: Control the Montserrat and Roboto stylesheet the ReDoc page loads with with_google_fonts and google_fonts_css_url.
---

# Fonts

The ReDoc page loads Montserrat and Roboto from Google Fonts. Swagger UI is not affected. To load no stylesheet, pass `with_google_fonts=False`:

```python
--8<-- "docs_src/advanced/fonts.py:snippet"
```

| Setup | ReDoc loads | CSP entries |
|---|---|---|
| Default | The stylesheet on `fonts.googleapis.com` | `https://fonts.googleapis.com` in `style-src`, `https://fonts.gstatic.com` in `font-src` |
| `google_fonts_css_url="/static/fonts.css"` | Your stylesheet | `'self'` in both, for files on your app |
| `with_google_fonts=False` | No font stylesheet | None |

`google_fonts_css_url` accepts any stylesheet URL, despite its name. [Fully self-hosted docs](../guides/self-hosted.md) uses it, and [`examples/static/fonts.css`](https://github.com/matblack81/fastapi-csp-docs/blob/main/examples/static/fonts.css) is a copy of the Google stylesheet that points at local font files.
