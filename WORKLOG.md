# netguardir.com — WORKLOG

## 2026-05-22 01:20 — CertGuard family addition + no-installer positioning

### Done
- **CertGuard landing page** added at `/certguard/index.html` — green accent (vs NetGuard blue). Same Buy / Download CTA layout. Cross-links to main site's family grid.
- **Main index.html**:
  - Hero subhead reframed from "Cisco STIG audit tool" → "Offline-first network security tools for air-gapped DoD environments."
  - Family grid now shows both products as LIVE (was just NetGuard-Audit before).
  - Added feature tile: **"Zero installer · SWAB-friendly"** — single-binary, no MSI, no admin, no auto-update. This is the value-prop Chris discovered is the moat for DoD work.
  - New FAQ entry: "Why no installer?" → SWAB approval pain, EDR scanning, RMF baseline drift.
  - Footer updated to reference both products.
- **Pricing teaser** kept off the page until v1.0 (per [[netguard-launch-plan]] — Std 100 / Pro 250 / Ent 1000 tiered per-site licensing not exposed yet).
- **Downloads vhost**: `downloads.netguardir.com` on oh-prod-01 (129.213.117.42) serves both product .zip artifacts. Cloudflare proxy enabled.
  - CF Pages 25 MiB asset limit forced this — binaries are 30-60 MB each.
- **Cloudflare config**: used `api_token_full` (NOT `api_token`) — DNS-only token couldn't create the page rule. Saved to [[cloudflare-creds]].
- **DNS**: `netguardir.com` apex + `downloads.netguardir.com` registered 2026-05-21 via Porkbun, A records to oh-prod-01. NS pointed to Cloudflare. See [[netguard-product-family]].
- **nginx**: `/etc/nginx/sites-available/downloads.netguardir.com` — TLS via Let's Encrypt, autoindex off, served files from `/var/www/downloads-netguardir/`.

### Tried but rejected
- **Host binaries on Cloudflare R2 with signed URLs** — overkill for free-download MVP. nginx is fine. Revisit when adding paid-license unlock URLs.
- **Add "buy now" Stripe checkout** — premature. No license enforcement code yet; would have to refund. Defer to v1.0 with Nuitka build + watermarking.

### Open / Next session
1. **Pricing page** — design (not publish) the per-site tier table for v1.0 launch. Std/Pro/Ent.
2. **Comparison page** "NetGuard vs Tenable Nessus vs Tenable.sc" — the niche positioning needs an explicit "we are the no-install Tenable for STIG audit on air-gapped switches" angle.
3. **Customer case study placeholder** — once first DoD design partner ships, slot at /case-studies/<name>.

### Watch out for
- **Cloudflare DNS-only token (`api_token`) cannot manage page rules or worker routes.** Use `api_token_full` for anything beyond DNS records. Both stored at `/root/.console-creds/cloudflare.json`.
- **CF Pages 25 MiB asset limit** is per-file, not per-deploy. Binaries always go via nginx vhost, never inline in Pages bundle.
- The site repo lives at `/root/outlaw-holdings/netguardir.com/` (not at `/var/www/`). Pages deploys via `wrangler` push from this dir.
