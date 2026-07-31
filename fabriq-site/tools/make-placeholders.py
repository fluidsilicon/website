#!/usr/bin/env python3
"""Generates the logo, favicon and every placeholder SVG in assets/img.

Run from the repo root:  python3 tools/make-placeholders.py
Delete this file and its output once you have real artwork.
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

BLACK = "#0B0B0C"
BURNT = "#B8410E"
EMBER = "#F0752A"
ASH = "#8A8A93"


def esc(t: str) -> str:
    """SVG is XML: a bare & is a parse error. Escape AFTER any case-folding,
    or .upper() turns &amp; into &AMP; and you get an undefined-entity error."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name: str, body: str) -> None:
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("  ", name)


# ---------------------------------------------------------------- logo mark --
# Nine tiles, one lit. The whole product in 24 pixels.
def mark(lit=EMBER, dim="currentColor", dim_op="0.55"):
    tiles = []
    for r in range(3):
        for c in range(3):
            x, y = 1 + c * 7.5, 1 + r * 7.5
            is_lit = (r, c) == (1, 1)
            tiles.append(
                f'<rect x="{x}" y="{y}" width="6" height="6" rx="1" '
                f'fill="{lit if is_lit else dim}"'
                + ("" if is_lit else f' opacity="{dim_op}"')
                + "/>"
            )
    return "".join(tiles)


write(
    "logo-mark.svg",
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    f'role="img" aria-label="Fabriq mark">{mark()}</svg>',
)

write(
    "favicon.svg",
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    f'<rect width="32" height="32" rx="6" fill="{BLACK}"/>'
    f'<g transform="translate(4 4)">{mark(lit=EMBER, dim="#FFFFFF", dim_op="0.5")}</g>'
    f"</svg>",
)


# --------------------------------------------------------------- placeholder --
def fabric(w: int, h: int, step: int, opacity: str) -> str:
    lines = []
    x = step
    while x < w:
        lines.append(f'<path d="M{x} 0V{h}"/>')
        x += step
    y = step
    while y < h:
        lines.append(f'<path d="M0 {y}H{w}"/>')
        y += step
    return (f'<g stroke="#FFFFFF" stroke-opacity="{opacity}" stroke-width="1">'
            + "".join(lines) + "</g>")


def heatmap(w: int, h: int, seed: int) -> str:
    """A scatter of lit tiles weighted toward two hot regions — reads as a
    placed design rather than noise."""
    step = 22
    cols, rows = w // step, h // step
    hubs = [
        (0.3 + 0.1 * math.sin(seed), 0.45 + 0.1 * math.cos(seed), 0.30),
        (0.72 - 0.08 * math.cos(seed * 1.7), 0.6, 0.20),
    ]
    out = []
    for r in range(rows):
        for c in range(cols):
            fx, fy = c / cols, r / rows
            best = 0.0
            for hx, hy, hr in hubs:
                d = math.hypot((fx - hx) / hr, (fy - hy) / (hr * 1.3))
                best = max(best, 1 - d)
            n = (math.sin((c * 12.9898 + r * 78.233 + seed) * 43758.5453) + 1) / 2
            v = best * 1.2 - n * 0.65
            if v <= 0.06:
                continue
            out.append(
                f'<rect x="{c * step + 3}" y="{r * step + 3}" width="{step - 6}" '
                f'height="{step - 6}" rx="1" fill="{BURNT}" opacity="{min(v, 1):.2f}"/>'
            )
    return "".join(out)


def placeholder(name: str, w: int, h: int, label: str, seed: int = 3) -> None:
    cx, cy = w / 2, h / 2
    write(
        name,
        f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     role="img" aria-label="{esc(label)} — placeholder image">
  <rect width="{w}" height="{h}" fill="#0E0E11"/>
  {heatmap(w, h, seed)}
  {fabric(w, h, 44, "0.05")}
  <g fill="none" stroke="{EMBER}" stroke-width="2" stroke-opacity="0.85">
    <path d="M24 46V24h22"/><path d="M{w - 46} 24h22v22"/>
    <path d="M{w - 24} {h - 46}v22h-22"/><path d="M46 {h - 24}H24v-22"/>
  </g>
  <text x="{cx}" y="{cy - 6}" text-anchor="middle" fill="#FFFFFF" fill-opacity="0.92"
        font-family="IBM Plex Mono, ui-monospace, monospace" font-size="15"
        letter-spacing="3.5">{esc(label.upper())}</text>
  <text x="{cx}" y="{cy + 20}" text-anchor="middle" fill="{ASH}"
        font-family="IBM Plex Mono, ui-monospace, monospace" font-size="12"
        letter-spacing="2.5">PLACEHOLDER · {w}×{h}</text>
</svg>""",
    )


print("Writing images…")
placeholder("placeholder-wide.svg", 1600, 900, "Product tour", 1)
placeholder("placeholder-card.svg", 1200, 750, "Replace me", 2)
placeholder("resource-1.svg", 1200, 750, "White paper", 4)
placeholder("resource-2.svg", 1200, 750, "Case study", 5)
placeholder("resource-3.svg", 1200, 750, "Webinar", 6)
placeholder("post-1.svg", 1200, 750, "Blog post", 7)
placeholder("post-2.svg", 1200, 750, "Blog post", 8)
placeholder("post-3.svg", 1200, 750, "Press release", 9)
placeholder("og-image.svg", 1200, 630, "Fabriq", 11)

for i, sector in enumerate(
    ["Data center", "AI / HPC", "Aerospace & defense",
     "Automotive", "Networking & 5G", "Test & measurement"], start=1
):
    placeholder(f"industry-{i}.svg", 1200, 750, sector, 20 + i * 3)

# ------------------------------------------------------------ partner marks --
# The viewBox is kept tight around the artwork so the wordmark stays legible
# when the logo strip scales it to 24px tall.
for i, word in enumerate(
    ["Northfield", "Axiom", "Kestrel", "Veralink",
     "Halcyon", "Drayton", "Silverpeak", "Okapi",
     "Branwell", "Tessera", "Meridian", "Coldbrook"], start=1
):
    h = 20
    w = int(24 + len(word) * 9.4)
    write(
        f"partner-{i}.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     role="img" aria-label="{word} — placeholder partner logo">
  <g transform="translate(0 2)" fill="{BLACK}">
    <rect width="7" height="7" rx="1"/>
    <rect x="8.5" width="7" height="7" rx="1" opacity="0.4"/>
    <rect y="8.5" width="7" height="7" rx="1" opacity="0.4"/>
    <rect x="8.5" y="8.5" width="7" height="7" rx="1" opacity="0.15"/>
  </g>
  <text x="24" y="15" fill="{BLACK}" font-family="Archivo, Helvetica, Arial, sans-serif"
        font-size="15" font-weight="700" letter-spacing="-0.3">{word}</text>
</svg>""",
    )

print("Done. Files in", OUT)
