import importlib.util
import re

from pathlib import Path

import pytest

from fastapi.testclient import TestClient

from examples._csp import REDOC_STYLE_HASHES
from fastapi_csp_docs.docs import (
    _FAVICON_URL,
    _GOOGLE_FONTS_CSS_URL,
    _REDOC_JS_URL,
    _SWAGGER_CSS_URL,
    _SWAGGER_JS_URL,
)

ROOT = Path(__file__).parent.parent
DOCS_SRC = ROOT / "docs_src"
SNIPPETS = sorted(DOCS_SRC.rglob("*.py"))

# The HTML pages each docs_src file serves.
PAGES = {
    "advanced/fonts": ["/docs", "/docs/oauth2-redirect", "/redoc"],
    "advanced/manual_wiring": ["/docs", "/docs/oauth2-redirect", "/redoc"],
    "advanced/manual_wiring_root_path": ["/docs"],
    "advanced/paths": ["/api-docs", "/docs/oauth2-redirect"],
    "advanced/sub_app": ["/api/docs", "/api/docs/oauth2-redirect", "/api/redoc"],
    "advanced/swagger_ui_options": ["/docs", "/auth/callback", "/redoc"],
    "guides/redoc_disable_search": ["/docs", "/docs/oauth2-redirect", "/redoc"],
    "guides/redoc_scoped_csp": ["/docs", "/docs/oauth2-redirect", "/redoc"],
    "guides/self_hosted": ["/docs", "/docs/oauth2-redirect", "/redoc"],
    "quickstart/app": ["/docs", "/docs/oauth2-redirect", "/redoc"],
}


def snippet_id(path: Path) -> str:
    return path.relative_to(DOCS_SRC).with_suffix("").as_posix()


def pages_text() -> str:
    return "\n".join(page.read_text(encoding="utf-8") for page in (ROOT / "docs").rglob("*.md"))


def test_pages_lists_every_docs_src_file() -> None:
    assert sorted(PAGES) == [snippet_id(path) for path in SNIPPETS]


@pytest.mark.parametrize("snippet", SNIPPETS, ids=snippet_id)
def test_docs_snippet_serves_its_pages_with_no_inline_script_or_style(snippet: Path) -> None:
    """The docs pages include these files, so a page can't show code that no longer runs."""
    spec = importlib.util.spec_from_file_location(f"docs_src_{snippet.stem}", snippet)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    client = TestClient(module.app)

    for path in PAGES[snippet_id(snippet)]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert "<script src=" in response.text, path
        assert "<script>" not in response.text, path
        assert "<style>" not in response.text, path


def test_every_docs_src_file_is_included_by_a_page() -> None:
    """A file no page includes is an example nobody reads, and nobody notices when it rots."""
    pages = pages_text()

    files = [path.relative_to(ROOT).as_posix() for path in SNIPPETS]

    assert [path for path in files if path not in pages] == []


def test_every_page_include_points_at_an_existing_docs_src_file() -> None:
    included = re.findall(r'--8<-- "(docs_src/[^":]+)', pages_text())

    assert included
    assert [path for path in included if not (ROOT / path).is_file()] == []


def test_reference_lists_the_default_asset_urls() -> None:
    """The generated reference prints the private constants' names, so the page spells out
    their values: a version bump that misses the page fails here."""
    reference = (ROOT / "docs" / "reference.md").read_text(encoding="utf-8")

    for url in (_SWAGGER_JS_URL, _SWAGGER_CSS_URL, _REDOC_JS_URL, _FAVICON_URL, _GOOGLE_FONTS_CSS_URL):
        assert f"`{url}`" in reference


def test_snippets_list_the_same_redoc_hashes_as_the_examples() -> None:
    """The hashes change with the ReDoc build, and every snippet that lists them has to follow."""
    snippets = [path for path in SNIPPETS if "sha256-" in path.read_text(encoding="utf-8")]

    assert snippets
    for path in snippets:
        hashes = re.findall(r"'sha256-[^']+'", path.read_text(encoding="utf-8"))
        assert tuple(hashes) == REDOC_STYLE_HASHES, path
