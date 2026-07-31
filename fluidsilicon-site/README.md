# fluidsilicon.com

Static site. No build step, no framework. HTML + CSS + vanilla JS.

```
index.html          Home
segments.html       Industries
demo.html           Schedule a demo
careers.html        Open roles
jobs/               Job posts
assets/content.js   ALL EDITABLE CONTENT (start here)
assets/styles.css   Design
assets/main.js      Rendering (rarely touched)
assets/img/         Logo and award images
assets/video/       Home page video
CNAME               Custom domain for GitHub Pages
```

## Editing the site

Nearly everything lives in **`assets/content.js`**:

- **Solutions cards** (home): add/remove/reword objects in `solutions`.
- **Industries** (home band + industries page): edit `industries`.
- **Job listings** (careers page): edit `jobs`. Job detail pages are the files in `jobs/`.
- **Recognition logos**: add objects to `recognition`.

Edit, save, `git push`. Done.

## Home page video

When the video is ready, put the file at `assets/video/home.mp4` and change one line in `assets/content.js`:

```js
video: "assets/video/home.mp4",
```

Until then the animated chip fabric shows in its place.

## Logo and award images

- **Logo:** drop your file at `assets/img/fluidsilicon_logo.png`. Every header shows it automatically; if the file is missing, the text wordmark shows instead.
- **Award:** replace `assets/img/presidents_sustainability_prize.png` with the real image (keep the filename).

## Run locally (Mac, VS Code)

```bash
python3 -m http.server 8000
# visit http://localhost:8000
```

(Use the server, not double-clicking the file, so content.js loads.)

## Deploy to GitHub Pages

One-time setup (Terminal, inside this folder):

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fluidsilicon.git
git push -u origin main
```

Then on github.com:

1. Repo > Settings > Pages
2. Source: Deploy from a branch > `main` > `/ (root)` > Save
3. Custom domain: `fluidsilicon.com` > Save (the CNAME file keeps this on every deploy)
4. Check "Enforce HTTPS" once the domain verifies

Every future update:

```bash
git add . && git commit -m "Update" && git push
```

## Connect the Squarespace domain

The domain stays registered with Squarespace; only DNS points to GitHub.

1. account.squarespace.com > Domains > fluidsilicon.com > DNS settings
2. Delete the existing Squarespace A records and the default `www` CNAME
3. Add four A records, Host `@`:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

4. Add one CNAME record, Host `www`, value `YOUR_USERNAME.github.io`
5. Verify after propagation:

```bash
dig fluidsilicon.com +noall +answer
```

Then confirm the green check in GitHub > Settings > Pages and enable HTTPS.

## Demo form

Currently opens a prefilled email to demo@fluidsilicon.com (no backend needed). To collect submissions instead, create a free endpoint at formspree.io and replace the mailto handler at the bottom of `assets/main.js` with a `fetch` POST.

Email addresses used: hello@, demo@, careers@fluidsilicon.com. Set these up as forwards in Squarespace (Domains > Email forwarding).
