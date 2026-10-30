import importlib.util

from pathlib import Path
from typing import Any

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

import fastapi_csp_docs

DOCS_SRC = Path(__file__).parent.parent / "docs_src"


def load(name: str) -> Any:
    """Import docs_src/<name>.py, which builds the app the page describes."""
    spec = importlib.util.spec_from_file_location(f"docs_src_{name.replace('/', '_')}", DOCS_SRC / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quickstart_serves_every_route_setup_registers() -> None:
    client = TestClient(load("quickstart/app").app)

    assert client.get("/docs/swagger-initializer.js").headers["content-type"].startswith("text/javascript")
    assert client.get("/docs/oauth2-redirect.js").headers["content-type"].startswith("text/javascript")
    assert client.get("/redoc/redoc.css").headers["content-type"].startswith("text/css")
    assert 'href="/redoc/redoc.css"' in client.get("/redoc").text
    assert 'src="/docs/swagger-initializer.js"' in client.get("/docs").text
    assert 'src="/docs/oauth2-redirect.js"' in client.get("/docs/oauth2-redirect").text


def test_quickstart_sends_a_policy_without_unsafe_inline() -> None:
    client = TestClient(load("quickstart/app").app)

    policy = client.get("/docs").headers["content-security-policy"]

    assert "script-src 'self' https://cdn.jsdelivr.net;" in policy
    assert "'unsafe-inline'" not in policy


def test_setup_keeps_the_docs_routes_out_of_the_schema() -> None:
    client = TestClient(load("quickstart/app").app)

    assert list(client.get("/openapi.json").json()["paths"]) == ["/items"]


def test_setup_raises_while_the_built_in_docs_are_enabled() -> None:
    app = FastAPI()

    with pytest.raises(RuntimeError) as exc_info:
        fastapi_csp_docs.setup(app)

    assert str(exc_info.value) == (
        "fastapi_csp_docs.setup() cannot mount Swagger UI at '/docs' because the app still serves "
        "its built-in docs at '/docs'. Create the FastAPI app with docs_url=None to disable it "
        "first, e.g. FastAPI(docs_url=None)."
    )


def test_self_hosted_guide_loads_every_asset_from_the_app() -> None:
    client = TestClient(load("guides/self_hosted").app)

    docs = client.get("/docs").text
    redoc = client.get("/redoc").text
    policy = client.get("/docs").headers["content-security-policy"]

    assert "https://" not in docs
    assert 'href="/static/fonts.css"' in redoc
    assert 'src="/static/redoc.standalone.js"' in redoc
    assert "https://" not in redoc
    for asset in ("swagger-ui-bundle.js", "swagger-ui.css", "redoc.standalone.js", "favicon.png", "fonts.css"):
        assert client.get(f"/static/{asset}").status_code == 200
    assert policy.count("https://") == 1
    assert "img-src 'self' data: https://cdn.redoc.ly" in policy


def test_self_hosted_guide_prefixes_the_asset_urls_under_a_root_path() -> None:
    client = TestClient(load("guides/self_hosted").app, root_path="/api")

    assert 'src="/api/static/swagger-ui-bundle.js"' in client.get("/docs").text


def test_absolute_and_protocol_relative_asset_urls_are_used_as_given() -> None:
    app = FastAPI(docs_url=None, redoc_url=None)
    fastapi_csp_docs.setup(
        app,
        swagger_js_url="https://assets.example.com/swagger-ui-bundle.js",
        swagger_css_url="//assets.example.com/swagger-ui.css",
    )

    docs = TestClient(app, root_path="/api").get("/docs").text

    assert 'src="https://assets.example.com/swagger-ui-bundle.js"' in docs
    assert 'href="//assets.example.com/swagger-ui.css"' in docs


def test_scoped_csp_gives_only_the_redoc_page_the_redoc_directives() -> None:
    client = TestClient(load("guides/redoc_scoped_csp").app)

    docs_policy = client.get("/docs").headers["content-security-policy"]
    redoc_policy = client.get("/redoc").headers["content-security-policy"]

    assert "script-src 'self' https://cdn.jsdelivr.net" in docs_policy
    for entry in ("sha256-", "blob:", "cdn.redoc.ly", "fonts.googleapis.com"):
        assert entry not in docs_policy
        assert entry in redoc_policy


def test_disabled_search_needs_no_worker_src() -> None:
    client = TestClient(load("guides/redoc_disable_search").app)

    response = client.get("/redoc")

    assert 'disable-search="true"' in response.text
    assert client.get("/redoc/redoc.css").status_code == 200
    assert "script-src" in response.headers["content-security-policy"]
    assert "worker-src" not in response.headers["content-security-policy"]


def test_paths_moves_swagger_ui_and_skips_redoc() -> None:
    client = TestClient(load("advanced/paths").app)

    assert 'src="/api-docs/swagger-initializer.js"' in client.get("/api-docs").text
    assert client.get("/api-docs/swagger-initializer.js").status_code == 200
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404


def test_paths_leaves_the_oauth2_redirect_at_fastapis_url() -> None:
    client = TestClient(load("advanced/paths").app)

    assert client.get("/docs/oauth2-redirect").status_code == 200
    assert client.get("/api-docs/oauth2-redirect").status_code == 404


def test_passing_none_keeps_fastapis_built_in_page_if_the_app_has_it() -> None:
    app = FastAPI(docs_url=None)
    fastapi_csp_docs.setup(app, redoc_url=None)

    client = TestClient(app)

    assert "<style>" in client.get("/redoc").text
    assert "<script>" not in client.get("/docs").text


def test_no_openapi_schema_skips_both_pages() -> None:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    fastapi_csp_docs.setup(app)

    client = TestClient(app)

    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404


def test_swagger_ui_options_reach_the_init_script() -> None:
    client = TestClient(load("advanced/swagger_ui_options").app)

    script = client.get("/docs/swagger-initializer.js").text

    assert '"docExpansion": "none"' in script
    assert '"tryItOutEnabled": true' in script
    assert '"deepLinking": true' in script
    assert 'ui.initOAuth({"clientId": "docs-client", "usePkceWithAuthorizationCodeGrant": true})' in script
    assert 'oauth2RedirectUrl: window.location.origin + "/auth/callback"' in script


def test_swagger_ui_oauth2_redirect_url_moves_both_redirect_routes() -> None:
    client = TestClient(load("advanced/swagger_ui_options").app)

    assert 'src="/auth/callback.js"' in client.get("/auth/callback").text
    assert client.get("/auth/callback.js").status_code == 200
    assert client.get("/docs/oauth2-redirect").status_code == 404


def test_no_oauth2_redirect_url_skips_the_redirect_routes() -> None:
    app = FastAPI(docs_url=None, redoc_url=None, swagger_ui_oauth2_redirect_url=None)
    fastapi_csp_docs.setup(app)

    client = TestClient(app)

    assert client.get("/docs").status_code == 200
    assert "oauth2RedirectUrl" not in client.get("/docs/swagger-initializer.js").text
    assert client.get("/docs/oauth2-redirect").status_code == 404


def test_fonts_off_drops_the_stylesheet_from_redoc() -> None:
    client = TestClient(load("advanced/fonts").app)

    redoc = client.get("/redoc").text

    assert "<redoc spec-url=" in redoc
    assert "fonts.googleapis.com" not in redoc


def test_sub_app_resolves_its_urls_under_the_mount_prefix() -> None:
    client = TestClient(load("advanced/sub_app").app)

    script = client.get("/api/docs/swagger-initializer.js").text
    redoc = client.get("/api/redoc").text

    assert 'src="/api/docs/swagger-initializer.js"' in client.get("/api/docs").text
    assert 'url: "/api/openapi.json"' in script
    assert 'oauth2RedirectUrl: window.location.origin + "/api/docs/oauth2-redirect"' in script
    assert 'href="/api/redoc/redoc.css"' in redoc
    assert 'spec-url="/api/openapi.json"' in redoc


def test_root_path_from_the_server_prefixes_the_urls() -> None:
    client = TestClient(load("quickstart/app").app, root_path="/api")

    assert 'src="/api/docs/swagger-initializer.js"' in client.get("/docs").text
    assert 'spec-url="/api/openapi.json"' in client.get("/redoc").text


def test_manual_wiring_serves_every_companion_route() -> None:
    client = TestClient(load("advanced/manual_wiring").app)

    assert "<title>Items API reference</title>" in client.get("/docs").text
    assert 'url: "/openapi.json"' in client.get("/docs/swagger-initializer.js").text
    assert 'src="/docs/oauth2-redirect.js"' in client.get("/docs/oauth2-redirect").text
    assert client.get("/docs/oauth2-redirect.js").status_code == 200
    assert "<title>Items API guide</title>" in client.get("/redoc").text
    assert 'disable-search="true"' in client.get("/redoc").text
    assert client.get("/redoc/redoc.css").status_code == 200


def test_manual_wiring_ignores_the_root_path_unless_the_route_reads_it() -> None:
    plain = TestClient(load("advanced/manual_wiring").app, root_path="/api")
    aware = TestClient(load("advanced/manual_wiring_root_path").app, root_path="/api")

    assert 'src="/docs/swagger-initializer.js"' in plain.get("/docs").text
    assert 'src="/api/docs/swagger-initializer.js"' in aware.get("/docs").text
