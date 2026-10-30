---
description: Which Swagger UI and ReDoc releases the default asset URLs load, and what to check when an upgrade changes them.
---

# Pinned asset versions

The default asset URLs pin exact releases on jsdelivr: `swagger-ui-dist@5.34.0` and `redoc@2.5.4`. FastAPI's own defaults use the floating `@5` and `@2` tags. The full URLs are in the [reference](../reference.md#default-asset-urls).

With a pinned version, the files the browser loads change only when you upgrade `fastapi-csp-docs`, so the CSP entries that depend on them keep matching until then.

## Upgrading

The release notes list every version bump. When one changes these versions, update:

- the file URLs, if your CSP [pins exact files](../guides/csp.md#pinning-exact-files);
- the [ReDoc style hashes](../guides/redoc-csp.md#inline-styles), which depend on the ReDoc build;
- your copies of the bundles, if you [self-host them](../guides/self-hosted.md).

## Other versions

To load another release, pass its URL as `swagger_js_url`, `swagger_css_url` or `redoc_js_url`.

The ReDoc hashes in this documentation apply to `redoc@2.5.4` only: capture them again for any other build, as [Inline styles](../guides/redoc-csp.md#inline-styles) describes.
