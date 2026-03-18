---
name: opencrawl
description: Crawl any JavaScript-rendered webpage through distributed real Chrome browsers. No local browser needed — perfect for headless VPS.
homepage: https://github.com/hlyylly/OpenCrawl
env:
  required:
    - OPENCRAWL_API_KEY
  optional:
    - OPENCRAWL_API_URL
---

# OpenCrawl Skill

Use this skill to crawl any JavaScript-rendered webpage using **real Chrome browsers** from a distributed worker pool. Unlike headless browser solutions (Puppeteer/Playwright), OpenCrawl requires zero local browser installation — ideal for VPS and cloud environments.

**Authentication:** Set `OPENCRAWL_API_KEY` (get one by registering at your OpenCrawl server dashboard) in your environment or `.env` file. Optionally set `OPENCRAWL_API_URL` (defaults to `http://localhost:9877`).

**How it works:** Your request → OpenCrawl server → dispatched to a real Chrome browser worker → page rendered with full JavaScript → content extracted → uploaded to Cloudflare R2 → download URL returned to you.

**Errors:** On failure the script writes a JSON error to stderr and exits with code 1.

---

## Tools

### 1. Crawl Page

Use this to get the full rendered text content of any webpage, including JavaScript-rendered content that simple HTTP requests cannot retrieve.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --url "https://example.com"
```

**Examples:**
```bash
# Crawl a full page
python3 {baseDir}/tools/crawl.py --url "https://www.smzdm.com/p/170177008/"

# Crawl with CSS selector to extract specific content
python3 {baseDir}/tools/crawl.py --url "https://example.com" --selector ".article-content"

# Output raw JSON response (includes downloadUrl)
python3 {baseDir}/tools/crawl.py --url "https://example.com" --raw
```

Optional flags:
- `--selector ".css-selector"` — Extract only matching elements
- `--raw` — Output full JSON response instead of just the text content
- `--timeout 60` — Custom timeout in seconds (default: 60)

---

### 2. Check Balance

Use this to check how many credits remain on the API key.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --balance
```

---

### 3. Check Status

Use this to check the OpenCrawl platform status — how many workers are online, tasks completed, etc.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --status
```

---

## Summary

| Action | Argument | Example |
|--------|----------|---------|
| Crawl page | `--url` | `python3 {baseDir}/tools/crawl.py --url "https://example.com"` |
| Crawl with selector | `--url` + `--selector` | `python3 {baseDir}/tools/crawl.py --url "https://example.com" --selector ".main"` |
| Check balance | `--balance` | `python3 {baseDir}/tools/crawl.py --balance` |
| Check status | `--status` | `python3 {baseDir}/tools/crawl.py --status` |

**Output:** Crawl → rendered page text (or JSON with `--raw`). Balance → JSON with credits info. Status → JSON with worker/task stats.

**Requirements:** Python 3.8+, `requests` library. No browser installation needed.
