# netguardir.com

Product site for InfoRelay NetGuard. Static HTML/CSS — no build step.

## Structure

```
netguardir.com/
├── index.html              landing page
├── docs/
│   └── user-guide.html     user guide (single-page)
├── assets/
│   ├── styles.css          full brand stylesheet
│   └── logo.svg            NetGuard mark
├── downloads/
│   └── inforelay-netguard-0.1-src.tar.gz   source tarball
└── README.md
```

## Local preview

```bash
cd netguardir.com
python3 -m http.server 8888
# open http://127.0.0.1:8888/
```

## Deploy options

### Option A — Cloudflare Pages (recommended)

1. Push this directory to a GitHub repo (or hand-upload).
2. Cloudflare Pages → New project → connect repo → no build command → output dir `/`.
3. Add `netguardir.com` as a custom domain in Cloudflare.
4. DNS — Cloudflare auto-provisions the A/CNAME records once you delegate the zone.

### Option B — OCI block volume (oh-prod-01)

1. SCP this directory to `oh-prod-01:/var/www/netguardir.com/`.
2. nginx server block:
   ```
   server {
     listen 443 ssl http2;
     server_name netguardir.com www.netguardir.com;
     root /var/www/netguardir.com;
     ssl_certificate /etc/letsencrypt/live/netguardir.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/netguardir.com/privkey.pem;
     location / { try_files $uri $uri/ =404; }
   }
   ```
3. `certbot --nginx -d netguardir.com -d www.netguardir.com`.

### Option C — Hostinger static site

Drop the directory into the Hostinger file manager under the netguardir.com domain root. Cheapest, no infra; fine for v0.

## Downloads

The download tiles on the landing page currently point to:
- `downloads/netguard-0.1-windows-x64.exe`   ← needs PyInstaller build
- `downloads/netguard-0.1-macos.dmg`         ← needs Mac build host
- `downloads/netguard-0.1-linux-x86_64.AppImage` ← needs AppImage packager
- `downloads/inforelay-netguard-0.1-src.tar.gz`  ← ✓ shipped (~30 MB)

Until the binaries are built, the Windows/macOS/Linux tiles 404 — they show the "SOON" badge to set expectations. Replace each file in `downloads/` and the tile auto-resolves.

## Brand tokens

| Token | Value |
|---|---|
| Primary | `#3d6cff` |
| Deep | `#1737a8` |
| Gradient | `linear-gradient(135deg, #3d6cff, #1737a8)` |
| Display font | Space Grotesk (Google) |
| Body font | Inter Tight (Google) |
| Mono | JetBrains Mono (Google) |

Reuse the same brand variables in any future InfoRelay tool sub-site to keep the NetGuard family visually consistent.
