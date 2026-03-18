# OpenCrawl Skill for OpenClaw

Crawl any JavaScript-rendered webpage through **distributed real Chrome browsers**. No local browser installation needed — perfect for headless VPS environments.

Powered by [OpenCrawl](https://github.com/hlyylly/OpenCrawl).

## Why?

Your OpenClaw agent runs on a VPS without a real browser. Puppeteer/Playwright need 4GB+ RAM and complex setup. This skill gives your agent access to a **pool of real Chrome browsers** via a simple API call.

## Setup

1. Get an API key from an OpenCrawl server (or [deploy your own](https://github.com/hlyylly/OpenCrawl))
2. Set environment variable:
   ```bash
   export OPENCRAWL_API_KEY=ak_your_key
   export OPENCRAWL_API_URL=https://your-server:9877  # optional
   ```
3. Install the skill:
   ```bash
   clawhub install hlyylly/opencrawl
   ```

## Usage

Once installed, your OpenClaw agent can:

- **"Crawl https://example.com"** — Get rendered page content
- **"Crawl https://example.com and extract .article-content"** — Get specific elements
- **"Check my OpenCrawl balance"** — See remaining credits

## How It Works

```
Your Agent → OpenCrawl API → Real Chrome Worker → Render JS → Extract Content → R2 → Agent
```

- Workers are real Chrome browsers contributed by the community
- Each crawl costs 1 credit, Workers earn 1 credit per task
- Results stored on Cloudflare R2 (zero egress fees)
- Worker cookies isolated via incognito mode

## License

MIT
