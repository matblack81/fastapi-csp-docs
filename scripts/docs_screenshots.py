"""Regenerates the screenshots of docs/assets/screenshots/ from the apps the pages describe.

    uv run python scripts/docs_screenshots.py --channel chrome
    uv run python scripts/docs_screenshots.py --channel chrome --only redoc-search

Each screenshot is taken in a real browser, from a file of docs_src/ served locally: the same
code the page shows, with its Content-Security-Policy. The script fails if the browser reports a
CSP violation on the way, so a run also proves that the policies of docs_src/ hold. Swagger UI
and ReDoc load their scripts from a CDN, so the machine needs network access.

--channel chrome (or msedge) uses the browser already installed. Without it, Playwright uses its
own Chromium, installed once with `uv run playwright install chromium`.
"""

import argparse
import importlib.util
import socket
import threading
import time

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import uvicorn

from playwright.sync_api import ConsoleMessage, Page, sync_playwright

ROOT = Path(__file__).parent.parent
OUT = ROOT / "docs/assets/screenshots"
WIDTH = 800
REDOC_WIDTH = 1000  # ReDoc hides its side menu on narrower windows
REDOC_HEIGHT = 480
SCALE = 2  # screenshots are taken at twice the size they are shown at, to stay sharp on dense screens
PADDING = 24


def swagger(page: Page) -> dict[str, float]:
    """From the title of Swagger UI to the last operation."""
    page.wait_for_selector(".swagger-ui .opblock")
    bottom = page.evaluate(
        "Math.max(...[...document.querySelectorAll('.opblock')].map(e => e.getBoundingClientRect().bottom + scrollY))"
    )
    return {"x": 0, "y": 30, "width": WIDTH, "height": bottom + PADDING - 30}


def redoc(page: Page) -> dict[str, float]:
    """The top of ReDoc, side menu included."""
    page.wait_for_selector(".menu-content")
    return {"x": 0, "y": 0, "width": REDOC_WIDTH, "height": REDOC_HEIGHT}


def redoc_search(page: Page) -> dict[str, float]:
    """ReDoc with the results of a search, which only appear if its worker started."""
    clip = redoc(page)
    page.get_by_placeholder("Search...").fill("items")
    page.wait_for_selector("[data-role='search:results'] li")
    return clip


@dataclass(frozen=True)
class Shot:
    name: str
    app: str  # file with an `app`, relative to the repository root
    path: str
    width: int
    prepare: Callable[[Page], dict[str, float]]  # brings the page to the state to show, returns the clip


SHOTS = [
    Shot("quickstart-swagger", "docs_src/quickstart/app.py", "/docs", WIDTH, swagger),
    Shot("quickstart-redoc", "docs_src/quickstart/app.py", "/redoc", REDOC_WIDTH, redoc),
    Shot("redoc-search", "docs_src/quickstart/app.py", "/redoc", REDOC_WIDTH, redoc_search),
    Shot("redoc-no-search", "docs_src/guides/redoc_disable_search.py", "/redoc", REDOC_WIDTH, redoc),
]


def load_app(relative: str) -> Any:
    spec = importlib.util.spec_from_file_location(f"shot_{relative.replace('/', '_')}", ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


@contextmanager
def serve(app: Any) -> Iterator[str]:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--channel", help="installed browser to use: chrome or msedge (default: Playwright's Chromium)")
    parser.add_argument("--only", nargs="+", metavar="NAME", help="take only these screenshots")
    args = parser.parse_args()

    shots = [shot for shot in SHOTS if not args.only or shot.name in args.only]
    unknown = set(args.only or []) - {shot.name for shot in SHOTS}
    if unknown:
        parser.error(f"unknown screenshot(s): {', '.join(sorted(unknown))}")

    violations: list[str] = []

    def record_violation(message: ConsoleMessage) -> None:
        if "Content Security Policy" in message.text:
            violations.append(f"{message.location['url']}: {message.text}")

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel=args.channel)
        context = browser.new_context(
            viewport={"width": WIDTH, "height": 700}, device_scale_factor=SCALE, color_scheme="light"
        )
        page = context.new_page()
        page.on("console", record_violation)
        for app_file in dict.fromkeys(shot.app for shot in shots):
            with serve(load_app(app_file)) as base_url:
                for shot in (s for s in shots if s.app == app_file):
                    page.set_viewport_size({"width": shot.width, "height": 700})
                    page.goto(f"{base_url}{shot.path}", wait_until="networkidle")
                    clip = shot.prepare(page)
                    target = OUT / f"{shot.name}.jpg"
                    page.screenshot(path=target, type="jpeg", quality=88, clip=clip, full_page=True)
                    print(f"{shot.name:20} {target.stat().st_size // 1024:4} KB  <- {shot.app} {shot.path}")
        browser.close()

    if violations:
        raise SystemExit("CSP violations:\n" + "\n".join(violations))


if __name__ == "__main__":
    main()
