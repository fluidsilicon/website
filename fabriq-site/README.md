# Fabriq — FPGA marketing site starter

A static marketing site with the structural bones of a proteanTecs-style B2B
semiconductor site (mega-nav → solutions by topic and by industry → technology →
partners → resources → company), rebuilt from scratch with an original design in
burnt orange, white and black, and FPGA placeholder content throughout.

No build step. No npm. No framework. 17 HTML pages, one CSS file, one JS file.
Open a file, edit it, refresh.

---

## 1. Run it locally (macOS)

```bash
cd path/to/this/folder
python3 -m http.server 8000
```

Open <http://localhost:8000>.

`python3` ships with the Xcode Command Line Tools, so if you have `git`, you have
this. Any static server works — `npx serve`, VS Code Live Server, whatever you
already use. Opening `index.html` straight from Finder works too, since every
path is relative.

---

## 2. What's here

```
index.html              Homepage — the full structure
solutions.html          Overview: by topic + by industry
solution-*.html         Six topic pages (timing, power, debug, production, fleet, security)
industries.html         Six industry sections, anchor-linked from the nav
technology.html         The four-layer technology story
partners.html           Logo wall + partner programs
resources.html          Knowledge center: papers, case studies, webinars
blog.html               Blog + newsroom
about.html              Company
careers.html            Open roles
contact.html            Book-a-demo form (not wired up yet — see §4)
404.html                Not-found page

assets/css/site.css     Everything visual. Tokens at the top.
assets/js/site.js       Nav, tabs, scroll reveals, the hero floorplan.
assets/img/             Generated placeholders — replace all of these.
tools/make-placeholders.py   Regenerates the placeholder art. Delete when done.
```

### The one trade-off you should know about

The header and footer are **copy-pasted into all 17 pages**. That's the price of
zero build tooling — you can open any file and see the whole page, and it deploys
anywhere with no pipeline. When editing the nav in 17 places starts to hurt, move
to Astro or Eleventy: the CSS and markup transfer over untouched, you're only
extracting a layout.

Until then: edit the nav in `index.html`, then find-and-replace the `<header>`
block across the rest.

---

## 3. Make it yours

### Name

Everything is called `Fabriq`. One command:

```bash
grep -rl 'Fabriq' . --include='*.html' --include='*.md' | xargs sed -i '' 's/Fabriq/YourName/g'
```

(The empty `''` after `-i` is required on macOS — that's BSD sed, not GNU.)

The wordmark lives in the `<header>` and `<footer>` of each page:
`<span class="brand__word">Fabr<em>i</em>q</span>` — the `<em>` is what makes one
letter orange. The mark beside it is inline SVG. Swap both for your real logo.

### Colour

All of it is at the top of `assets/css/site.css`:

```css
--black:  #0B0B0C;   /* deepest surface */
--white:  #FFFFFF;
--burnt:  #B8410E;   /* primary burnt orange — for use on light backgrounds */
--ember:  #F0752A;   /* brighter orange — for use on dark, for contrast */
```

Two oranges rather than one, deliberately: a burnt orange dark enough to read on
white is too dark to read on black. Change `--burnt` and `--ember` together and
keep the lightness gap between them.

Below those sit the semantic tokens (`--bg`, `--fg`, `--accent`, `--rule`,
`--card-bg`…). Any section with `class="on-dark"` flips them, and every component
reads only the semantic ones — so nothing needs a dark variant.

### Type

Archivo (display) + IBM Plex Sans (body) + IBM Plex Mono (labels, data, buttons),
from Google Fonts in each `<head>`. The mono face is doing real work: it's the
"utilization report" voice, used for anything that's a measurement or a label and
never for prose. If you swap faces, keep a mono in that role or the design loses
its accent.

### Images

Everything in `assets/img/` is a generated placeholder — the orange corner
brackets are the tell. `tools/make-placeholders.py` regenerates them at different
sizes while you wait for real art. Delete the script and its output once you have
the real thing.

The hero is **not** a placeholder. It's a live SVG device floorplan drawn by
`initFloorplan()` in `site.js` — the fabric grid, the placed design in orange, the
telemetry sweep, and the readout underneath. It's the signature element. If you'd
rather have a background video there like proteanTecs does, drop a `<video>` in
place of the `.floorplan` block and delete that function.

### Copy

All placeholder, all original, all written to sound like engineers wrote it. It's
specific on purpose — specific placeholder copy is much easier to react to than
lorem ipsum. Rewrite freely.

---

## 4. Before you go live

- [ ] `contact.html` — the form doesn't submit anywhere. Point its `action` at
      Formspree, HubSpot, or your own endpoint, and delete the `data-demo-form`
      handler at the bottom of `site.js`.
- [ ] Footer legal links (`Privacy`, `Terms`, `Cookie settings`) are `href="#"`.
- [ ] Social links in the footer are `href="#"`.
- [ ] `robots.txt` and `sitemap.xml` say `www.example.com` — replace.
- [ ] `assets/img/og-image.svg` is a placeholder, and most social scrapers want a
      PNG or JPG for `og:image`. Export a real 1200×630 and update the meta tags.
- [ ] The stats (`18%`, `12 °C`, `9%`…) are invented. Don't ship invented numbers.

---

## 5. Deploy to GitHub Pages

From this folder, into your empty repo:

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/YOUR-REPO.git
git push -u origin main
```

Then in the repo: **Settings → Pages → Build and deployment**

- Source: **Deploy from a branch**
- Branch: **main**, folder: **/ (root)** → **Save**

First build takes a minute or two, then you're live at
`https://YOUR-ORG.github.io/YOUR-REPO/`.

The `.nojekyll` file in the root matters — without it GitHub runs everything
through Jekyll, which silently ignores any directory starting with an underscore.
You don't have one today, but you will eventually, and the failure is confusing.

> Not married to GitHub Pages? Netlify and Cloudflare Pages both take this repo
> with no build command and a publish directory of `/`, and both make the DNS step
> easier. Nothing in the site depends on the host.

---

## 6. Point your Squarespace domain at it

Two halves: tell GitHub the domain, tell Squarespace where to send it.

### a. GitHub side

**Settings → Pages → Custom domain** → enter `www.yourdomain.com` → **Save**.

This auto-commits a `CNAME` file to your repo — expected, leave it alone. (That's
why there's no `CNAME` file in here already: a wrong one would break the site.)
Then `git pull` so your local copy has it.

### b. Squarespace side

**Domains dashboard → click your domain → DNS → DNS Settings → Custom Records**.

First, **remove the Squarespace default records** — the A records pointing at
`198.185.159.x` / `198.49.23.x` and the `www` CNAME to `ext-sq.squarespace.com`.
Those are what currently send the domain to Squarespace's servers, and they'll
fight with yours.

**Leave your MX records alone.** Those are email. Deleting them takes down your
inbox, and it's a bad afternoon.

Then add:

| Type  | Host  | Value                 |
| ----- | ----- | --------------------- |
| CNAME | `www` | `YOUR-ORG.github.io`  |
| A     | `@`   | `185.199.108.153`     |
| A     | `@`   | `185.199.109.153`     |
| A     | `@`   | `185.199.110.153`     |
| A     | `@`   | `185.199.111.153`     |
| AAAA  | `@`   | `2606:50c0:8000::153` |
| AAAA  | `@`   | `2606:50c0:8001::153` |
| AAAA  | `@`   | `2606:50c0:8002::153` |
| AAAA  | `@`   | `2606:50c0:8003::153` |

The CNAME target is your GitHub org or username — `YOUR-ORG.github.io`, **not**
`YOUR-ORG.github.io/YOUR-REPO`, and no trailing slash.

The A and AAAA records on the apex make `yourdomain.com` work too; GitHub
redirects it to the `www` you set as the custom domain. If Squarespace only lets
you save a single A record, one is enough to start.

### c. Then wait, then check

DNS usually settles in 10–30 minutes but is allowed to take 24 hours. From your
Mac:

```bash
dig www.yourdomain.com +noall +answer
dig yourdomain.com +noall +answer -t A
```

Back in **Settings → Pages**, GitHub runs its own DNS check. Once it passes, the
**Enforce HTTPS** checkbox becomes available — tick it. The certificate can take
up to an hour to issue after the check passes, so a greyed-out box usually means
waiting rather than something being wrong.

### If it doesn't come up

- **Certificate errors, or "Enforce HTTPS" stays greyed out** → almost always a
  leftover record. Extra A, AAAA, ALIAS or CNAME entries on `@` or `www` block
  certificate provisioning. There should be exactly one path to your site.
- **Still seeing Squarespace** → old records cached, or the domain is still
  attached to a Squarespace site. Detach it there first.
- **"Domain already taken"** → it's set as the custom domain on another repo.
- **404 on every page but the homepage** → you published a subfolder as the root.
  Publish from `/ (root)`.

---

## 7. Design notes

For whoever restyles this next:

- **The signature is the hero floorplan.** Everything around it is deliberately
  quiet so it can be loud. Add a second attention-grabbing element and they'll
  fight — and you'll lose the one that says what the company does.
- **Structural labels carry information, not decoration.** The tag on each
  solution card (`Design`, `Test`, `Field`) tells a buyer where in their flow it
  lands. The `01`–`04` on the technology pillars is a real sequence. Where a label
  would only have restated the link text, there isn't one. Keep that rule or they
  turn into noise.
- **Sections alternate dark and light on purpose** — dark is "inside the fabric",
  light is "the report you read". It isn't just rhythm.
- **The mono face is the real accent**, more than the orange is. Orange is used
  sparingly enough that removing the mono would do more damage.
