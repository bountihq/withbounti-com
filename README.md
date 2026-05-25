# withbounti.com — cold-outreach landing page

Static landing page served at https://withbounti.com via GitHub Pages.

## Why this exists

Cold-outreach sender domains need a real website at their root URL. ISPs
filter domains with MX records but no website as throwaway spammer
infrastructure. This single-page site:

- Resolves to real content (not 404 or registrar parking)
- Identifies the parent brand (Bounti, Inc.)
- Acknowledges the cold email honestly
- Provides a clear opt-out path

## Local preview

```bash
open index.html
# or, served over http:
python3 -m http.server 8000
```

## Test (Playwright)

```bash
python3 test_landing.py
```

Asserts content + saves desktop + mobile screenshots to `screenshots/`.

## Deploy

Auto-deployed via GitHub Pages on push to `main`. HTTPS via Let's Encrypt,
auto-provisioned by GitHub after DNS propagates.

## DNS records at Namecheap

For `withbounti.com`, apex A records pointing at GitHub Pages IPs:

```
@  A  185.199.108.153
@  A  185.199.109.153
@  A  185.199.110.153
@  A  185.199.111.153
```

## Updating

```bash
# edit index.html, then:
git add index.html
git commit -m "Tweak landing copy"
git push
# GitHub Pages redeploys in ~30 seconds.
```
