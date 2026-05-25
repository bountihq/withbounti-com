"""
Visual + content test for this landing page.

Renders index.html in headless Chromium, asserts the structural pieces are
present (logo, headline, CTA with correct href + UTMs, footer attribution,
opt-out language), and saves screenshots at desktop + mobile viewports for
visual review.

Usage:
    python3 test_landing.py
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


HERE = Path(__file__).parent
LANDING = HERE / "index.html"
OUT = HERE / "screenshots"


def main() -> int:
    if not LANDING.exists():
        print(f"ERROR: {LANDING} not found")
        return 1

    OUT.mkdir(exist_ok=True)
    landing_url = f"file://{LANDING.resolve()}"
    failures: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        # ── Desktop viewport ────────────────────────────────────────────────
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(landing_url)
        page.wait_for_load_state("networkidle")

        title = page.title()
        if "Bounti" not in title:
            failures.append(f"Title missing 'Bounti': {title!r}")

        logo_text = page.locator(".logo").inner_text()
        if "Bounti" not in logo_text:
            failures.append(f"Logo missing 'Bounti': {logo_text!r}")

        body_text = page.locator("body").inner_text().lower()
        if "real-estate" not in body_text and "real estate" not in body_text:
            failures.append("Page doesn't mention 'real-estate' anywhere visible")

        cta = page.locator("a.cta")
        if cta.count() != 1:
            failures.append(f"Expected exactly 1 CTA, found {cta.count()}")
        else:
            href = cta.get_attribute("href") or ""
            if "claw.bounti.ai" not in href:
                failures.append(f"CTA href missing 'claw.bounti.ai': {href!r}")
            if "utm_source" not in href:
                failures.append(f"CTA href missing UTM tags: {href!r}")

        footer_text = page.locator("footer").inner_text()
        if "Bounti, Inc." not in footer_text:
            failures.append(f"Footer missing parent-brand attribution: {footer_text!r}")

        if "unsubscribe" not in body_text and "stop emailing" not in body_text:
            failures.append("No visible unsubscribe / opt-out language on page")

        desktop_png = OUT / "desktop-1440x900.png"
        page.screenshot(path=str(desktop_png), full_page=True)
        print(f"  desktop: {desktop_png.relative_to(HERE)}")
        ctx.close()

        # ── Mobile viewport (iPhone 14 Pro) ────────────────────────────────
        ctx = browser.new_context(viewport={"width": 393, "height": 852})
        page = ctx.new_page()
        page.goto(landing_url)
        page.wait_for_load_state("networkidle")
        mobile_png = OUT / "mobile-393x852.png"
        page.screenshot(path=str(mobile_png), full_page=True)
        print(f"  mobile:  {mobile_png.relative_to(HERE)}")
        ctx.close()

        browser.close()

    if failures:
        print("\n✗ FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\n✓ All structural assertions passed.")
    print(f"✓ Review screenshots in {OUT.relative_to(HERE)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
