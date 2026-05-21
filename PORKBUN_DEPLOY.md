# Deploying netguardir.com to Porkbun

Two viable paths depending on which Porkbun product is enabled for the domain.

## Path A — Porkbun Static Hosting (recommended; free with the domain)

Porkbun bundles free static hosting with any domain registered with them. No DNS work — they auto-wire it.

### Steps

1. **Build the upload bundle:**
   ```bash
   cd netguardir.com
   ./deploy.sh
   # → build/netguardir-site.zip   (~30 MB)
   ```

2. **Upload via the Porkbun dashboard:**
   - Log into <https://porkbun.com/account/login>
   - **Domain Management** → **netguardir.com** → **Static Hosting** (left sidebar)
   - If hosting is not yet enabled: **Enable Hosting**. Free, instant.
   - Click **File Manager**
   - **Upload** → drop `build/netguardir-site.zip` → **Extract here**
   - Delete `build/netguardir-site.zip` from the file manager after extracting
   - Click **Save / Apply** at the top

3. **Wait 2–5 minutes** for the CDN to warm. Then visit:
   - <https://netguardir.com>
   - <https://www.netguardir.com>
   - <https://netguardir.com/docs/user-guide.html>
   - <https://netguardir.com/downloads/inforelay-netguard-0.1-src.tar.gz>

Porkbun auto-provisions:
- SSL certificate (Let's Encrypt)
- Both apex and www subdomains
- The required A and CNAME records

That's it. No DNS edits needed.

---

## Path B — External hosting + Porkbun DNS only

Use this if you'd rather host on Cloudflare Pages / Netlify / OCI / Hostinger and only use Porkbun for DNS.

### Steps

1. **Upload site files** to your external host (SCP/SFTP/git push depending on platform).

2. **Find the target IP or CNAME** the host gave you. Examples:
   - Cloudflare Pages: `<project>.pages.dev` (CNAME)
   - OCI block: `<floating-ip>` (A record)
   - Hostinger: `<vps-ip>` (A record)

3. **Set DNS via the Porkbun API:**
   ```bash
   export PORKBUN_API_KEY=pk1_xxxxxxxx
   export PORKBUN_API_SECRET=sk1_xxxxxxxx

   # apex A record
   ./porkbun_dns.py upsert netguardir.com A @ 1.2.3.4 --ttl 600

   # www CNAME
   ./porkbun_dns.py upsert netguardir.com CNAME www netguardir.com --ttl 600
   ```

4. **Provision SSL** on your host (Let's Encrypt via certbot or platform-managed).

### Verifying via API

```bash
./porkbun_dns.py ping                 # auth sanity check
./porkbun_dns.py list netguardir.com  # show every record
```

---

## What's on the live site

| URL | Purpose |
|---|---|
| `/` | Landing page (features, workflow, download, FAQ) |
| `/docs/user-guide.html` | Single-page v0.1 user manual |
| `/downloads/inforelay-netguard-0.1-src.tar.gz` | Source tarball (~30 MB) — live now |
| `/downloads/netguard-0.1-windows-x64.exe` | **PENDING** — build on Win11 box via `build_windows.bat`, upload to `downloads/` |
| `/downloads/netguard-0.1-macos.dmg` | **PENDING** — needs Mac build host |
| `/downloads/netguard-0.1-linux-x86_64.AppImage` | **PENDING** — needs AppImage packager |
| `/assets/styles.css`, `/assets/logo.svg` | Brand assets |

Until the platform binaries are built, those download tiles 404 — the page already shows the **SOON** badge on each so it's not misleading.

## Iterating on the site

If you want changes after deploy:

1. Edit the source files locally (`index.html`, `assets/styles.css`, etc.)
2. Re-run `./deploy.sh`
3. Upload the new `build/netguardir-site.zip` to Porkbun static hosting (same path as Path A step 2)
4. Porkbun's "Extract here" lets you choose **overwrite existing**
