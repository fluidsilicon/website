#!/usr/bin/env python3
"""Generate the site's binary assets from the same sources as the pages.

    python3 tools_assets.py

Writes into src/ (build.py then copies them to dist/site):
  favicon.ico, assets/img/{apple-touch-icon,icon-192,icon-512,icon-maskable-512,og-image}.png,
  site.webmanifest, robots.txt, CNAME, .nojekyll

Needs Playwright with Chromium and Pillow. Nothing here is needed at runtime.
"""
import io, json, os, re, sys, html
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import build as B          # facts, devices, logo, routes

SRC = os.path.join(ROOT, "src")
TMP = os.path.join(ROOT, "_tmp")
IMG = os.path.join(SRC, "assets", "img")
esc = html.escape
os.makedirs(TMP, exist_ok=True)

MARK = open(os.path.join(IMG, "mark.svg"), encoding="utf-8").read()
MARK_INNER = re.search(r'<g class="fs-mark">(.*)</g></svg>', MARK, re.S).group(1)
TRACES = re.search(r'(<g fill="none" stroke="#FFFFFF".*)', MARK_INNER, re.S).group(1)
LOGO_LIGHT = re.sub(r"<title>.*?</title>", "", open(os.path.join(IMG, "logo-on-light.svg"), encoding="utf-8").read())


def svg_page(svg, size, bg="transparent"):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:{bg}}}'
            f'svg{{display:block;width:{size}px;height:{size}px}}</style></head><body>{svg}</body></html>')


def maskable_svg():
    # full-bleed orange, the F traces kept inside the 80% safe zone
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#F06024"/>'
            f'<g transform="translate(32 32) scale(.72) translate(-31 -31)">{TRACES}</g></svg>')


def write_text(path, s):
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


# ------------------------------------------------------------------ open graph image
def og_html():
    """1200 x 630 social image: charcoal background, headline, and the chip floorplan from the site's hero."""
    FONTS = "file://" + os.path.join(B.SRC, "assets", "fonts")
    logo = B.logo_svg("og-logo", "dark")
    chip = B.fabric_svg("og-chip")
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Red Hat Display"; src: url("{FONTS}/red-hat-display-latin-wght-normal.woff2"); font-weight: 300 900; }}
@font-face {{ font-family: "Red Hat Text"; src: url("{FONTS}/red-hat-text-latin-wght-normal.woff2"); font-weight: 300 700; }}
html, body {{ margin: 0; }}
.og {{ position: relative; width: 1200px; height: 630px; box-sizing: border-box; padding: 64px 0 56px 72px; display: grid; grid-template-columns: 600px 1fr; gap: 24px; align-items: center;
       background: #121212; background-image: radial-gradient(700px 420px at 82% 40%, rgba(240, 96, 36, .22), transparent 65%); font-family: "Red Hat Text", sans-serif; overflow: hidden; }}
.left {{ display: grid; gap: 22px; align-content: center; }}
.left svg {{ width: 260px; height: auto; }}
h1 {{ margin: 0; font: 650 64px/1.04 "Red Hat Display", sans-serif; letter-spacing: -0.025em; color: #f4f2ed; }}
.sub {{ margin: 0; font-size: 24px; line-height: 1.4; color: #c3bfb6; max-width: 26ch; }}
.right {{ display: grid; place-items: center; }}
.right svg {{ width: 470px; height: auto; filter: drop-shadow(0 24px 48px rgba(0, 0, 0, .6)); }}
.right .sweep {{ display: none; }}
.bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: linear-gradient(90deg, #f06024 0 34%, #a67c00 34% 67%, #6c602a 67%); }}
</style></head><body><div class="og">
<div class="left">{logo}
<h1>At advanced nodes, every device is different.</h1>
<p class="sub">A customizable platform for FPGA adaptation &amp; resilience: every device measured at speed, in-system, and kept inside its measured margin.</p></div>
<div class="right">{chip}</div><div class="bar"></div></div></body></html>'''


def main(only=None):
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page()
        if only == "og":
            p = os.path.join(TMP, "og.html"); write_text(p, og_html())
            pg.set_viewport_size({"width": 1200, "height": 630})
            pg.goto("file://" + p); pg.wait_for_timeout(500)
            Image.open(io.BytesIO(pg.screenshot())).convert("RGB").save(os.path.join(IMG, "og-image.png"), optimize=True)
            br.close(); print("og-image.png written"); return
        # icons
        shots = {}
        for size in (16, 32, 48, 180, 192, 512):
            pg.set_viewport_size({"width": size, "height": size})
            opaque = size == 180          # iOS paints transparent corners black; fill them with the package edge color
            pg.set_content(svg_page(MARK, size, "#C64E00" if opaque else "transparent"))
            shots[size] = pg.screenshot(omit_background=not opaque)
        pg.set_viewport_size({"width": 512, "height": 512})
        pg.set_content(svg_page(maskable_svg(), 512))
        Image.open(io.BytesIO(pg.screenshot())).save(os.path.join(IMG, "icon-maskable-512.png"), optimize=True)
        for size, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
            Image.open(io.BytesIO(shots[size])).save(os.path.join(IMG, name), optimize=True)
        ico = [Image.open(io.BytesIO(shots[s])).convert("RGBA") for s in (16, 32, 48)]
        ico[2].save(os.path.join(SRC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
        # open graph image
        p = os.path.join(TMP, "og.html"); write_text(p, og_html())
        pg.set_viewport_size({"width": 1200, "height": 630})
        pg.goto("file://" + p); pg.wait_for_timeout(500)
        Image.open(io.BytesIO(pg.screenshot())).convert("RGB").save(os.path.join(IMG, "og-image.png"), optimize=True)
        br.close()
    # text files
    manifest = {"name": "Fluid Silicon", "short_name": "Fluid Silicon", "description": "Timing health for FPGA fleets.",
                "start_url": "/", "scope": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#ffffff",
                "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
                          {"src": "/assets/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    write_text(os.path.join(SRC, "site.webmanifest"), json.dumps(manifest, indent=2) + "\n")
    write_text(os.path.join(SRC, "robots.txt"), f"User-agent: *\nAllow: /\n\nSitemap: {B.SITE_URL}/sitemap.xml\n")
    write_text(os.path.join(SRC, "CNAME"), "fluidsilicon.com\n")
    write_text(os.path.join(SRC, ".nojekyll"), "")
    print("assets written")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
