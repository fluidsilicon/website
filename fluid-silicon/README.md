# Fluid Silicon — site

Static site for Fluid Silicon (University of Pennsylvania): silicon health
monitoring for FPGAs. No build step, no npm. 7 HTML pages, one CSS file, one JS
file. Edit a file, refresh.

## 0. Restore the assets folder first

This repo needs the `assets/` folder from the original Fabriq starter
(`assets/css/site.css`, `assets/js/site.js`, `assets/img/favicon.svg`,
`assets/img/og-image.svg`). Copy it in unchanged — every page references it and
the colors (burnt orange / black / white) already match Fluid Silicon's.

## 1. Run locally (macOS, Apple Silicon fine)

```bash
cd path/to/this/folder
python3 -m http.server 8000
```
Open <http://localhost:8000>.

## 2. What's here

```
index.html         Home — hero floorplan, capabilities, how it works, industries
solutions.html     Five capabilities: monitoring, timing queries, compensation,
                   characterization, self-healing (anchor-linked from the nav)
technology.html    The four-layer platform story
industries.html    Data centers, defense & aerospace, telecom, automotive
about.html         The group
contact.html       Contact form (not wired up — see §3)
404.html           Not-found page
```

The header and footer are copy-pasted into every page (the price of zero build
tooling). Edit the nav in `index.html`, then find-and-replace the `<header>`
block across the rest.

## 3. Before you go live

- [ ] `contact.html` — point the form `action` at Formspree or your endpoint,
      and delete the `data-demo-form` handler at the bottom of `site.js`.
- [ ] Replace `contact@example.com` in `contact.html` with the real address.
- [ ] `robots.txt` and `sitemap.xml` say `www.example.com` — replace.
- [ ] Footer `Privacy` link is `href="#"`.
- [ ] Export a real 1200×630 PNG for `og:image` and update the meta tags.

## 4. Deploy to GitHub Pages

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/YOUR-REPO.git
git push -u origin main
```

Repo → **Settings → Pages → Build and deployment**: Source **Deploy from a
branch**, branch **main**, folder **/ (root)** → Save. Live in a minute or two at
`https://YOUR-ORG.github.io/YOUR-REPO/`. Keep the `.nojekyll` file — it stops
GitHub from running the site through Jekyll.

## 5. Point your Squarespace domain at it

**GitHub side:** Settings → Pages → Custom domain → enter `www.yourdomain.com`
→ Save. This auto-commits a `CNAME` file — leave it, then `git pull`.

**Squarespace side:** Domains dashboard → your domain → DNS → DNS Settings →
Custom Records. First delete the Squarespace defaults — the A records at
`198.185.159.x` / `198.49.23.x` and the `www` CNAME to
`ext-sq.squarespace.com`. **Do not touch MX records** (that's your email).

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

The CNAME target is `YOUR-ORG.github.io` — no repo name, no trailing slash.

**Then:** wait 10–30 min (up to 24 h), check with
`dig www.yourdomain.com +noall +answer`. Once GitHub's DNS check passes in
Settings → Pages, tick **Enforce HTTPS** (the certificate can take up to an
hour after the check passes).

If HTTPS stays greyed out, it's almost always a leftover A/AAAA/CNAME record on
`@` or `www`. If you still see Squarespace, detach the domain from any
Squarespace site first.
