import asyncio

import httpx
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

import fastapi_csp_docs


def _no_inline_script_or_style(html: str) -> bool:
    return "<script>" not in html and "<style>" not in html


def test_setup_raises_if_docs_url_not_disabled():
    app = FastAPI()  # docs_url defaults to "/docs"

    with pytest.raises(RuntimeError, match="docs_url=None"):
        fastapi_csp_docs.setup(app)


def test_setup_raises_if_redoc_url_not_disabled():
    app = FastAPI(docs_url=None)  # redoc_url defaults to "/redoc"

    with pytest.raises(RuntimeError, match="redoc_url=None"):
        fastapi_csp_docs.setup(app)


def test_setup_registers_swagger_and_redoc_routes():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    for path in [
        "/docs",
        "/docs/swagger-initializer.js",
        "/redoc",
        "/redoc/redoc.css",
        "/docs/oauth2-redirect",
        "/docs/oauth2-redirect.js",
    ]:
        response = client.get(path)
        assert response.status_code == 200, path


def test_setup_docs_html_and_redoc_html_have_no_inline_script_or_style():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    docs_html = client.get("/docs").text
    redoc_html = client.get("/redoc").text
    oauth_html = client.get("/docs/oauth2-redirect").text

    assert _no_inline_script_or_style(docs_html)
    assert _no_inline_script_or_style(redoc_html)
    assert _no_inline_script_or_style(oauth_html)


def test_setup_asset_content_types():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    assert client.get("/docs/swagger-initializer.js").headers["content-type"].startswith("text/javascript")
    assert client.get("/docs/oauth2-redirect.js").headers["content-type"].startswith("text/javascript")
    assert client.get("/redoc/redoc.css").headers["content-type"].startswith("text/css")


def test_setup_swagger_initializer_embeds_openapi_url():
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url="/schema.json")
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    js = client.get("/docs/swagger-initializer.js").text
    assert "/schema.json" in js


def test_setup_redoc_search_enabled_by_default():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    html = client.get("/redoc").text
    assert "disable-search" not in html


def test_setup_respects_custom_docs_and_redoc_url():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, docs_url="/documentation", redoc_url="/documentation/redoc")
    client = TestClient(app)

    assert client.get("/documentation").status_code == 200
    assert client.get("/documentation/swagger-initializer.js").status_code == 200
    assert client.get("/documentation/redoc").status_code == 200
    assert client.get("/documentation/redoc/redoc.css").status_code == 200
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404


def test_setup_uses_cdn_assets_by_default():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    docs = client.get("/docs").text
    assert '<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui-bundle.js"' in docs
    assert 'href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.34.0/swagger-ui.css"' in docs
    redoc = client.get("/redoc").text
    assert '<script src="https://cdn.jsdelivr.net/npm/redoc@2.5.4/bundles/redoc.standalone.js">' in redoc
    assert 'href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700"' in redoc


def test_setup_uses_custom_asset_urls():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(
        app,
        swagger_js_url="https://assets.example.com/swagger-ui-bundle.js",
        swagger_css_url="https://assets.example.com/swagger-ui.css",
        swagger_favicon_url="https://assets.example.com/swagger.png",
        redoc_js_url="https://assets.example.com/redoc.standalone.js",
        redoc_favicon_url="https://assets.example.com/redoc.png",
        google_fonts_css_url="https://assets.example.com/fonts.css",
    )
    client = TestClient(app)

    docs = client.get("/docs").text
    assert '<script src="https://assets.example.com/swagger-ui-bundle.js" charset="UTF-8"></script>' in docs
    assert '<link type="text/css" rel="stylesheet" href="https://assets.example.com/swagger-ui.css">' in docs
    assert '<link rel="shortcut icon" href="https://assets.example.com/swagger.png">' in docs
    assert "cdn.jsdelivr.net" not in docs

    redoc = client.get("/redoc").text
    assert '<script src="https://assets.example.com/redoc.standalone.js"> </script>' in redoc
    assert '<link rel="shortcut icon" href="https://assets.example.com/redoc.png">' in redoc
    assert '<link href="https://assets.example.com/fonts.css" rel="stylesheet">' in redoc
    assert "cdn.jsdelivr.net" not in redoc
    assert "fonts.googleapis.com" not in redoc


def test_setup_without_google_fonts_omits_the_fonts_stylesheet():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, with_google_fonts=False)
    client = TestClient(app)

    redoc = client.get("/redoc").text
    assert '<script src="https://cdn.jsdelivr.net/npm/redoc@2.5.4/bundles/redoc.standalone.js">' in redoc
    assert "fonts.googleapis.com" not in redoc


@pytest.mark.parametrize(
    ("asset_url", "expected"),
    [
        ("/static/redoc.standalone.js", "/api/static/redoc.standalone.js"),
        ("https://assets.example.com/redoc.standalone.js", "https://assets.example.com/redoc.standalone.js"),
        ("//assets.example.com/redoc.standalone.js", "//assets.example.com/redoc.standalone.js"),
        ("static/redoc.standalone.js", "static/redoc.standalone.js"),
    ],
)
def test_setup_prefixes_root_path_only_to_asset_paths_on_the_app(asset_url: str, expected: str):
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, redoc_js_url=asset_url)
    client = TestClient(app, root_path="/api")

    assert f'<script src="{expected}"> </script>' in client.get("/redoc").text


def test_setup_asset_paths_follow_the_mount_prefix():
    sub_app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(
        sub_app,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.png",
        google_fonts_css_url="/static/fonts.css",
    )
    parent_app = FastAPI()
    parent_app.mount("/api", sub_app)
    client = TestClient(parent_app)

    docs = client.get("/api/docs").text
    assert '<script src="/api/static/swagger-ui-bundle.js" charset="UTF-8"></script>' in docs
    assert 'href="/api/static/swagger-ui.css"' in docs
    assert 'href="/api/static/favicon.png"' in docs

    redoc = client.get("/api/redoc").text
    assert '<script src="/api/static/redoc.standalone.js"> </script>' in redoc
    assert 'href="/api/static/favicon.png"' in redoc
    assert 'href="/api/static/fonts.css"' in redoc


def test_setup_asset_paths_are_unchanged_without_root_path():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, swagger_js_url="/static/swagger-ui-bundle.js")
    client = TestClient(app)

    assert '<script src="/static/swagger-ui-bundle.js" charset="UTF-8"></script>' in client.get("/docs").text


def test_setup_docs_url_none_skips_swagger_ui_only():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, docs_url=None)
    client = TestClient(app)

    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 200


def test_setup_redoc_url_none_skips_redoc_only():
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, redoc_url=None)
    client = TestClient(app)

    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 404


def test_setup_skips_oauth2_redirect_when_disabled_on_app():
    app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_oauth2_redirect_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    assert client.get("/docs").status_code == 200
    assert client.get("/docs/oauth2-redirect").status_code == 404
    assert client.get("/docs/oauth2-redirect.js").status_code == 404


def test_setup_no_routes_when_openapi_disabled():
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)
    client = TestClient(app)

    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404


def test_setup_openapi_disabled_skips_docs_url_only():
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, redoc_url=None)
    client = TestClient(app)

    assert client.get("/docs").status_code == 404


def test_setup_openapi_disabled_skips_redoc_url_only():
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app, docs_url=None)
    client = TestClient(app)

    assert client.get("/redoc").status_code == 404


def test_setup_root_path_is_reflected_in_mounted_sub_app():
    sub_app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(sub_app)

    parent_app = FastAPI()
    parent_app.mount("/api", sub_app)

    client = TestClient(parent_app)
    js = client.get("/api/docs/swagger-initializer.js").text
    assert "/api/openapi.json" in js
    assert "/api/docs/oauth2-redirect" in js

    redoc_html = client.get("/api/redoc").text
    assert "/api/openapi.json" in redoc_html
    assert "/api/redoc/redoc.css" in redoc_html


def test_setup_root_path_set_by_server_is_reflected():
    # TestClient(root_path=...) stands in for the server's --root-path behind a proxy
    # that strips the prefix: requests arrive without it, generated URLs carry it.
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)

    client = TestClient(app, root_path="/api")
    assert "/api/docs/swagger-initializer.js" in client.get("/docs").text

    js = client.get("/docs/swagger-initializer.js").text
    assert "/api/openapi.json" in js
    assert "/api/docs/oauth2-redirect" in js

    assert "/api/docs/oauth2-redirect.js" in client.get("/docs/oauth2-redirect").text

    redoc_html = client.get("/redoc").text
    assert "/api/openapi.json" in redoc_html
    assert "/api/redoc/redoc.css" in redoc_html


async def test_setup_redoc_css_response_is_safe_to_reuse_across_concurrent_requests():
    # _setup_redoc() builds redoc_css_response once and returns that same Response
    # instance for every request; verify concurrent requests all still get the
    # correct, uncorrupted body instead of racing on shared state.
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        responses = await asyncio.gather(*(client.get("/redoc/redoc.css") for _ in range(20)))

    assert all(r.status_code == 200 for r in responses)
    assert all(r.text == "body{margin:0;padding:0;}" for r in responses)


async def test_setup_oauth2_redirect_js_response_is_safe_to_reuse_across_concurrent_requests():
    # Same shared-singleton pattern as redoc_css_response, for
    # oauth2_redirect_js_response in _setup_swagger_ui_oauth2_redirect().
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(app)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        responses = await asyncio.gather(*(client.get("/docs/oauth2-redirect.js") for _ in range(20)))

    assert all(r.status_code == 200 for r in responses)
    assert all(r.text == responses[0].text for r in responses)
    assert "swaggerUIRedirectOauth2" in responses[0].text
