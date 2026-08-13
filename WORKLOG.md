# netguardir.com — WORKLOG

## 2026-05-25 01:25 — ScoreGuard page + Vault placeholder + 334FY23 scrub

### Done

- **`/scoreguard/index.html` (new)** — full mirror of `/assetguard/` layout with cyan accent (cyan-500 → cyan-700). Hero, "Why it exists", 4-step features grid, configurable-per-environment grid, "coming next" tiles, download grid (3 platforms), posture section, footer with family cross-links. `/scoreguard/favicon.png` from the build dir.
- **Homepage tile (`index.html:204+`)** — added ScoreGuard tile in family grid right after AssetGuard, cyan `tag-live` pill. Reads "DoD Cyber Hygiene Scorecard automation. Import CSVs → preview → fill manual sections → export a paste-ready Cyber Maintenance Hardening Scorecard workbook."
- **NetGuard Vault placeholder (`index.html:215+`)** — slotted in the family grid between Drift and Multi-vendor, 2026 Q4 timing, 🗄 icon. Per Chris: STIG requires automated config backup; gold-image restore is part of the spec.
- **Scrubbed every `334FY23` reference site-wide** — Chris flagged it's an old file reference; the official name is just "Cyber Maintenance Hardening Scorecard". 5 mentions on /scoreguard/ page + 1 on homepage tile description.
- Three Cloudflare Pages deploys via `wrangler pages deploy . --project-name=netguardir --branch=main` (per [[netguardir-pages-deploy]] — apex only serves production branch). Live URL each time → apex.
- All three commits in `/root/outlaw-holdings/netguardir.com`:
  - `70b99d4` Add ScoreGuard product page + homepage tile
  - `983d955` Add NetGuard Vault placeholder tile
  - `57a7c39` ScoreGuard: drop 334FY23 file reference, use full template name

### Decisions made + why

- **Vault name (not "Backup", "Archive", "Restore")** — implies safekeeping + gold-image as one concept; matches the trust positioning of the family naming.
- **NetGuard Vault 2026 Q4** — Chris said "easy to build at some point" → low urgency, but the STIG-requirement framing makes it adjacent to NetGuard Audit's value prop. Slotted with Drift so they cluster as "config-state-related" tools.
- **Mirror AssetGuard layout for /scoreguard/** — Chris's [[netguardir-mirror-product]] rule: ship product UI → update site mockup same session. AssetGuard is the closest sibling (also BETA, also ISSO-targeted, also `licensing@inforelay.ai` contact).

### Tried but rejected

- (none)

### Open / Next session

1. **Pricing page** — still pending across the whole family; Chris hasn't decided.
2. **Comparison page** — "vs Tenable Nessus / SC for STIG audit" was in the prior backlog; still open.
3. **CertGuard Request-Access flow → other products** — currently only CertGuard uses gated access; ScoreGuard/AssetGuard ship open binaries. Revisit when license enforcement code is built.

### Watch out for

- **NEVER write `334FY23` in any new ScoreGuard copy** (page, email, README) — it's an old file reference. Use "Cyber Maintenance Hardening Scorecard".
- All other [[netguardir-pages-deploy]] gotchas still apply: production branch is `main` NOT `master`; downloads served from `/var/www/netguardir-downloads/` via nginx vhost, NOT Pages; commits need `-c user.email=... -c user.name=...` per-call (no global git config).

---

## 2026-05-24 18:30 — CertGuard public binary pulled · Request Access flow live

### Done

- Replaced the CertGuard download grid on `certguard/index.html` (3 download tiles + Windows-install walkthrough + Linux/macOS tiles) with a single **Request Access** panel: 4-step instructional flow (email → receive binary + key → activate → 30-day trial included), mailto with prefilled body (org/contact/platform/tier), pricing call-out linking to `/#licensing`.
- Updated the hero CTA at `certguard/index.html:92` from "⬇ Download CertGuard" to "Request access" pointing at the same `#download` anchor.
- Commit `d2d0002` deployed to Cloudflare Pages (`--branch=main`). Live URL: `https://6fbacf74.netguardir.pages.dev` → apex.
- Verified live apex: 0 references to `certguard-0.1-*.zip` or `download-tile` class on the page; "Request access" + "How to get the binary" + `licensing@netguardir.com` all render.

### Watch out for

- **Binaries are NOT deleted** — moved to `/opt/certguard-releases/v0.1/` on `oh-prod-01` so the license-gated download server can serve them later via signed URLs.
- **Direct deep links return 404** via belt-and-suspenders nginx `location /certguard/ { return 404; }` block on the `downloads.netguardir.com` vhost — even if files re-appear in the public dir, nginx refuses to serve.
- See [[certguard-licensing-service]] for the full activation infra (this is the marketing site; the activation work is on a different repo / different infra).

### File index

- `certguard/index.html` UPDATED (hero CTA + Request Access section, lines 92 + 464-517)

---

## 2026-05-24 12:02 — Site rebuild deploy, Chain Map mockup swap, internal-data scrub, CertGuard pricing live

### Done

**Four wrangler deploys this session, all `--branch=main`:**

1. **Carry-over Netwrix-style rebuild** (commit `5cfcb25`) — committed at start of session, was uncommitted from previous session. Massive diff: utility bar, trust strip, terminal+GUI demo pair, platform showcase, why-us 4-up, capabilities, how-it-works, stats, use cases, CTA strip, download grid, resources, FAQ, multi-col footer. DoD → DoW rename across copy. Plus `/certguard/one-pager/` + `/certguard/vs-cyberark/` collateral pages.

2. **CertGuard product page: Chain Map mockup** (commit `7f4abc2`):
   - Replaced Bulk Enrollment GUI mockup at `certguard/index.html:150-226` with new Chain Health Map mockup featuring:
     - Clickable stat-tile row (All / Healthy / ≤90d / ≤60d / ≤30d / Expired — Expired pre-highlighted as active filter showing 73 expired)
     - 2x3 grid of compound CA containers color-coded by worst-child verdict (ICA-NMC green, ICA-IESS orange w/ one selected ≤30d dot, ICA-OLD-NMC red, External faded purple)
     - Right-side detail drawer for selected `dc-iess-02` cert
   - Added supporting CSS in `assets/styles.css` (~85 lines): `.cm-stats`, `.cm-tile`, `.cm-canvas`, `.cm-ca` (+ variants `.root`, `.issuing`, `.external`, `.healthy`, `.warn30`, `.expired`), `.cm-dot` (+ `.ok`, `.urgent`, `.exp`, `.selected`), `.cm-side`, `.cm-kv`.

3. **Sanitize internal data + add CertGuard pricing** (commit `f443e7e`):
   - Chain Map mockup labels: `OCA-SBX` → `Offline-Root-CA`, `ICA-NMC` → `Issuing-CA-Web`, `ICA-IESS` → `Issuing-CA-User`, `ICA-OLD-NMC` → `Issuing-CA-Web-Legacy`, `dc-iess-02.iess.local` → `dc-02.corp.local`.
   - NetGuard mockup on homepage: `V1-9407R-1` → `core-sw-01`, `10.50.0.12` → `10.0.0.10`.
   - FAQ "multi-domain auth" rewording: NMC/IESS → CORP/CORP-LAB.
   - **Licensing FAQ at `index.html:504-518`** now lists CertGuard tiers:
     - `Solo` 1 CA — **$1,995/yr**
     - `Team` 5 CAs — **$5,995/yr**
     - `Site` unlimited — **$14,995/yr**
     - Plus offline license-file model description (Ed25519-signed, no phone-home, no hardware-fingerprint binding, version-range entitlement).
     - CTA: `licensing@netguardir.com` mailto.

4. **Drop "vessel" wording in vs-cyberark** (commit `ad82064`):
   - `certguard/vs-cyberark/index.html:131-135`: "Carry it onto a vessel or SCIF visit" → "Carry it into a SCIF or onto a deployed site". Caught after Chris flagged that V1/Vessel terminology stands out to colleagues.

**Verified live:**
- `curl -s https://netguardir.com/ | grep -cE 'V1-9407R|10\.50\.0\.|NMC|IESS|OCA-SBX'` → 0
- `curl -s https://netguardir.com/certguard/ | grep -cE 'V1-9407R|10\.50\.0\.|NMC|IESS|OCA-SBX|nmc\.local|iess\.local'` → 0
- `curl -s https://netguardir.com/certguard/vs-cyberark/ | grep -ciE 'vessel|V1[-_]'` → 0

### Tried but rejected

(none this session — every change Chris asked for landed cleanly)

### Open / Next session

- **Pricing + competitor pages** (strategy option #4 from sibling CertGuard roadmap): build `/pricing/` (gated form behind Cloudflare Turnstile), 4 more `/vs-X/` pages (Venafi, Keyfactor, AppViewX, native AD CS `/certsrv`), `/compare/` matrix page summarizing all 5.
- **License-gated downloads**: swap the open URLs in `index.html` and `certguard/index.html` download tiles for activation-required signed URLs (Cloudflare Workers can sign; or a tiny Flask service on this VPS).

### Watch out for

- **Production branch is `main` NOT `master`** — always pass `--branch=main` to wrangler, or the deploy lands on a `*.netguardir.pages.dev` preview URL and the apex keeps serving stale content. See [[netguardir-pages-deploy]].
- **Local repo has NO git remote** — deploys go via wrangler, not git push. Don't try to `git push origin main`.
- **Commits require `-c user.name=... -c user.email=...` flags** — the repo lacks a local user config, and per [[destructive-ops-manual]] memory we don't touch global git config. One-shot override per commit is the workaround.
- **Browser cache after deploy** — apex serves `cache-control: max-age=0, must-revalidate`, but WebView2 / Cloudflare edge can still hold prior HTML for ~30s. Hard-refresh (Ctrl+Shift+R) before assuming a deploy didn't take.
- **Downloads at `/var/www/netguardir-downloads/`** are served by nginx directly on this host (NOT Cloudflare Pages). Zip refreshes happen via atomic `cp foo.zip foo.zip.new && mv foo.zip.new foo.zip` to avoid mid-download truncation.

---

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
