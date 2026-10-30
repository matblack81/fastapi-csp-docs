# Release Notes

## Latest Changes

### Breaking Changes

* 📌 Load Swagger UI 5.34.0 and ReDoc 2.5.4 instead of the floating @5 and @2 tags. PR [#72](https://github.com/matblack81/fastapi-csp-docs/pull/72) by [@matblack81](https://github.com/matblack81).

### Features

* ✨ Let setup() load Swagger UI and ReDoc from custom asset URLs. PR [#75](https://github.com/matblack81/fastapi-csp-docs/pull/75) by [@matblack81](https://github.com/matblack81).

### Docs

* 📝 Add the documentation site skeleton with a strict build in CI. PR [#78](https://github.com/matblack81/fastapi-csp-docs/pull/78) by [@matblack81](https://github.com/matblack81).
* 📝 Document the CSP violations caused by Markdown in Swagger UI descriptions. PR [#77](https://github.com/matblack81/fastapi-csp-docs/pull/77) by [@matblack81](https://github.com/matblack81).
* 📝 Document setup()'s asset URL parameters and the manual wiring alternative. PR [#76](https://github.com/matblack81/fastapi-csp-docs/pull/76) by [@matblack81](https://github.com/matblack81).
* 📝 Add a README note on keeping the stricter CSP outside the ReDoc page. PR [#73](https://github.com/matblack81/fastapi-csp-docs/pull/73) by [@matblack81](https://github.com/matblack81).
* 🔥 Remove root_path_app example that relies on deprecated FastAPI(root_path=...). PR [#62](https://github.com/matblack81/fastapi-csp-docs/pull/62) by [@matblack81](https://github.com/matblack81).
* 🔧 Replace old GitHub username in release notes links. PR [#61](https://github.com/matblack81/fastapi-csp-docs/pull/61) by [@matblack81](https://github.com/matblack81).

### Internal

* ⬆ Bump fastapi from 0.141.1 to 0.162.0. PR [#74](https://github.com/matblack81/fastapi-csp-docs/pull/74) by [@matblack81](https://github.com/matblack81).
* ✅ Snapshot the pages every docs generator emits. PR [#71](https://github.com/matblack81/fastapi-csp-docs/pull/71) by [@matblack81](https://github.com/matblack81).
* 🔥 Remove the leftover sync-pin markers from the workflows. PR [#70](https://github.com/matblack81/fastapi-csp-docs/pull/70) by [@matblack81](https://github.com/matblack81).
* 👷 Install only the tests dependency group in the test workflows. PR [#69](https://github.com/matblack81/fastapi-csp-docs/pull/69) by [@matblack81](https://github.com/matblack81).
* 🔧 Split the dev dependencies into a separate tests group. PR [#68](https://github.com/matblack81/fastapi-csp-docs/pull/68) by [@matblack81](https://github.com/matblack81).
* 👷 Run the FastAPI master workflow daily. PR [#67](https://github.com/matblack81/fastapi-csp-docs/pull/67) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump certifi to 2026.10.23 and allow its name in typos. PR [#66](https://github.com/matblack81/fastapi-csp-docs/pull/66) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump certifi from 2026.6.17 to 2026.10.19. PR [#65](https://github.com/matblack81/fastapi-csp-docs/pull/65) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add a weekly CI run against FastAPI master. PR [#64](https://github.com/matblack81/fastapi-csp-docs/pull/64) by [@matblack81](https://github.com/matblack81).
* 👷 Test the latest FastAPI release in CI instead of the locked version. PR [#63](https://github.com/matblack81/fastapi-csp-docs/pull/63) by [@matblack81](https://github.com/matblack81).

## 1.0.4 (2026-10-16)

### Internal

* 🔧 Update GitHub owner name. PR [#59](https://github.com/matblack81/fastapi-csp-docs/pull/59) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump the python-packages group with 4 updates. PR [#58](https://github.com/matblack81/fastapi-csp-docs/pull/58) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the python-packages group with 3 updates. PR [#57](https://github.com/matblack81/fastapi-csp-docs/pull/57) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 2 updates. PR [#56](https://github.com/matblack81/fastapi-csp-docs/pull/56) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 1.0.3 (2026-09-22)

### Docs

* 📝 Fix release notes link still pointing to the old uppercase filename. PR [#44](https://github.com/matblack81/fastapi-csp-docs/pull/44) by [@matblack81](https://github.com/matblack81).

### Internal

* ⬆ Bump anyio from 4.14.1 to 4.14.2. PR [#51](https://github.com/matblack81/fastapi-csp-docs/pull/51) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the python-packages group with 8 updates. PR [#54](https://github.com/matblack81/fastapi-csp-docs/pull/54) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 3 updates. PR [#53](https://github.com/matblack81/fastapi-csp-docs/pull/53) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🐛 Tolerate anyio's BlockingPortal deprecation warning in tests. PR [#52](https://github.com/matblack81/fastapi-csp-docs/pull/52) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump pre-commit hooks. PR [#50](https://github.com/matblack81/fastapi-csp-docs/pull/50) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump the python-packages group with 4 updates. PR [#49](https://github.com/matblack81/fastapi-csp-docs/pull/49) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump re-actors/alls-green from 1.2.2 to 1.3.0 in the github-actions group. PR [#48](https://github.com/matblack81/fastapi-csp-docs/pull/48) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump fastapi from 0.140.0 to 0.141.1. PR [#47](https://github.com/matblack81/fastapi-csp-docs/pull/47) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the python-packages group with 9 updates. PR [#46](https://github.com/matblack81/fastapi-csp-docs/pull/46) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 2 updates. PR [#45](https://github.com/matblack81/fastapi-csp-docs/pull/45) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Replace actions/labeler with Latest Changes App auto-labeling. PR [#43](https://github.com/matblack81/fastapi-csp-docs/pull/43) by [@matblack81](https://github.com/matblack81).

## 1.0.2 (2026-08-12)

### Internal

* 👷 Tag CI action pins for sync tracking. PR [#41](https://github.com/matblack81/fastapi-csp-docs/pull/41) by [@matblack81](https://github.com/matblack81).
* 👷 Sync CI, pre-commit, and release scripts workflows with the latest template. PR [#40](https://github.com/matblack81/fastapi-csp-docs/pull/40) by [@matblack81](https://github.com/matblack81).
* 🐛 Fix release date defaulting to the date the script was imported. PR [#39](https://github.com/matblack81/fastapi-csp-docs/pull/39) by [@matblack81](https://github.com/matblack81).
* 🐛 Fix partial release state when release notes write fails. PR [#38](https://github.com/matblack81/fastapi-csp-docs/pull/38) by [@matblack81](https://github.com/matblack81).

## 1.0.1 (2026-08-05)

### Internal

* ✅ Add test for all runnable examples. PR [#36](https://github.com/matblack81/fastapi-csp-docs/pull/36) by [@matblack81](https://github.com/matblack81).
* ✅ Close remaining test coverage gaps in the package. PR [#35](https://github.com/matblack81/fastapi-csp-docs/pull/35) by [@matblack81](https://github.com/matblack81).
* ♻️ Import Response types from fastapi in the remaining examples and README. PR [#34](https://github.com/matblack81/fastapi-csp-docs/pull/34) by [@matblack81](https://github.com/matblack81).
* 🐛 Reject invalid bump types and cover prepare_release's untested error paths. PR [#33](https://github.com/matblack81/fastapi-csp-docs/pull/33) by [@matblack81](https://github.com/matblack81).
* 🐛 Fix partial release state when release notes update fails. PR [#32](https://github.com/matblack81/fastapi-csp-docs/pull/32) by [@matblack81](https://github.com/matblack81).
* 🔒️ Escape interpolated values in generated Swagger UI/ReDoc pages. PR [#31](https://github.com/matblack81/fastapi-csp-docs/pull/31) by [@matblack81](https://github.com/matblack81).
* ✅ Prove PR test changes actually catch a regression before merging. PR [#30](https://github.com/matblack81/fastapi-csp-docs/pull/30) by [@matblack81](https://github.com/matblack81).
* ⬆️ Bump tiangolo/latest-changes to 0.7.1. PR [#29](https://github.com/matblack81/fastapi-csp-docs/pull/29) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump fastapi from 0.139.2 to 0.140.0. PR [#28](https://github.com/matblack81/fastapi-csp-docs/pull/28) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the python-packages group with 5 updates. PR [#27](https://github.com/matblack81/fastapi-csp-docs/pull/27) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump zizmorcore/zizmor-action from 0.6.0 to 0.6.1 in the github-actions group. PR [#26](https://github.com/matblack81/fastapi-csp-docs/pull/26) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 1.0.0 (2026-07-28)
🎉 First stable release of fastapi-csp-docs.

## 0.1.4 (2026-07-28)

### Internal

* ⬆ Bump fastapi from 0.139.0 to 0.139.2. PR [#23](https://github.com/matblack81/fastapi-csp-docs/pull/23) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 4 updates. PR [#21](https://github.com/matblack81/fastapi-csp-docs/pull/21) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the python-packages group with 4 updates. PR [#22](https://github.com/matblack81/fastapi-csp-docs/pull/22) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pre-commit hooks. PR [#20](https://github.com/matblack81/fastapi-csp-docs/pull/20) by [@matblack81](https://github.com/matblack81).
* 👷 Replace Dependabot pre-commit ecosystem with custom bump workflow. PR [#19](https://github.com/matblack81/fastapi-csp-docs/pull/19) by [@matblack81](https://github.com/matblack81).
* ⬆ Bump the python-packages group with 5 updates. PR [#18](https://github.com/matblack81/fastapi-csp-docs/pull/18) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump zizmorcore/zizmor-action from 0.5.7 to 0.6.0 in the github-actions group. PR [#17](https://github.com/matblack81/fastapi-csp-docs/pull/17) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump https://github.com/crate-ci/typos from v1.48.0 to 5.0.7 in the pre-commit group. PR [#15](https://github.com/matblack81/fastapi-csp-docs/pull/15) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 3 updates. PR [#16](https://github.com/matblack81/fastapi-csp-docs/pull/16) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.1.3 (2026-07-10)

### Refactors

* ♻️ Align imports with FastAPI's public dependency contract. PR [#13](https://github.com/matblack81/fastapi-csp-docs/pull/13) by [@matblack81](https://github.com/matblack81).

### Internal

* 🔧 Add test coverage for setup()'s openapi and root_path edge cases. PR [#12](https://github.com/matblack81/fastapi-csp-docs/pull/12) by [@matblack81](https://github.com/matblack81).

## 0.1.2 (2026-07-09)

### Internal

* 🔧 Integrate Codecov for coverage tracking and update README. PR [#10](https://github.com/matblack81/fastapi-csp-docs/pull/10) by [@matblack81](https://github.com/matblack81).

## 0.1.1 (2026-07-08)

### Docs

* 📝 Update README badge styles and unwrap paragraphs. PR [#8](https://github.com/matblack81/fastapi-csp-docs/pull/8) by [@matblack81](https://github.com/matblack81).

## 0.1.0 (2026-07-08)

🚀 First official public release of **fastapi-csp-docs**.

FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect pages embed inline `<script>`/`<style>` tags, breaking any Content-Security-Policy without `'unsafe-inline'`. Even FastAPI's own ["Custom Docs UI Static Assets"](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) recipe only swaps CDN URLs for local ones, without removing that inline content. `fastapi-csp-docs` replaces all three pages with versions that load every script and stylesheet from a separate endpoint.

### Features

* ✨ `setup(app, *, docs_url="/docs", redoc_url="/redoc")`: one call replaces FastAPI's built-in `/docs`, `/redoc`, and OAuth2 redirect wiring, with no inline script or style left anywhere.
* ✨ Fails fast on misconfiguration: `setup()` raises `RuntimeError` if the app's built-in docs aren't disabled first, instead of silently letting them shadow the CSP-safe routes.
* ✨ CDN or fully self-hosted: works with the default jsdelivr CDN (`script-src 'self' <cdn-host>`) or entirely offline with your own static assets (`script-src 'self'`, zero external origins).
* ✨ Reverse-proxy / sub-app aware: doc URLs include the ASGI `root_path` computed per request, so mounting under a prefix (`app.mount("/api", sub_app)`) works out of the box.
* ✨ Content generators (`get_swagger_ui_html`, `get_swagger_ui_init_js`, `get_redoc_html`, `get_redoc_css`, `get_swagger_ui_oauth2_redirect_html`, `get_swagger_ui_oauth2_redirect_js`) exported for manual wiring, enabling a fully self-hosted setup with no CDN at all.
* ✨ `get_redoc_html(disable_search=True)`: disables ReDoc's client-side search box, avoiding the Web Worker it runs in, which otherwise needs `worker-src 'self' blob:` in the CSP, since the worker is instantiated from a `blob:` URL with no separate file to point at instead.
