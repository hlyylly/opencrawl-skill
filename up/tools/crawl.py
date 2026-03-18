#!/usr/bin/env python3
"""OpenCrawl CLI — Crawl any JS-rendered page through distributed real Chrome browsers."""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


API_URL = os.environ.get("OPENCRAWL_API_URL", "http://localhost:9877")
API_KEY = os.environ.get("OPENCRAWL_API_KEY", "")


def error_exit(msg):
    json.dump({"success": False, "error": msg}, sys.stderr)
    sys.stderr.write("\n")
    sys.exit(1)


def crawl(url, selector=None, timeout=60, raw=False):
    if not API_KEY:
        error_exit("OPENCRAWL_API_KEY environment variable not set")

    try:
        body = {"url": url}
        if selector:
            body["selector"] = selector

        res = requests.post(
            f"{API_URL}/api/crawl",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=timeout + 5,
        )
        data = res.json()
    except requests.Timeout:
        error_exit(f"Request timed out after {timeout}s")
    except requests.ConnectionError:
        error_exit(f"Cannot connect to OpenCrawl server at {API_URL}")
    except Exception as e:
        error_exit(str(e))

    if not res.ok or not data.get("success"):
        error_exit(data.get("error") or data.get("detail") or f"HTTP {res.status_code}")

    if raw:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    # Download the actual content from R2
    download_url = data.get("downloadUrl")
    if not download_url:
        error_exit("No download URL in response")

    try:
        dl_res = requests.get(download_url, timeout=30)
        dl_res.raise_for_status()
        content = dl_res.json()
        text = content.get("data", "")
        sys.stdout.write(text)
        sys.stdout.write("\n")
    except Exception as e:
        error_exit(f"Failed to download result: {e}")


def check_balance():
    if not API_KEY:
        error_exit("OPENCRAWL_API_KEY environment variable not set")

    try:
        res = requests.get(
            f"{API_URL}/api/balance",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        data = res.json()
    except Exception as e:
        error_exit(str(e))

    if not res.ok:
        error_exit(data.get("error") or data.get("detail") or f"HTTP {res.status_code}")

    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def check_status():
    try:
        res = requests.get(f"{API_URL}/api/status", timeout=10)
        data = res.json()
    except Exception as e:
        error_exit(str(e))

    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main():
    parser = argparse.ArgumentParser(description="OpenCrawl — Distributed browser rendering")
    parser.add_argument("--url", help="URL to crawl")
    parser.add_argument("--selector", help="CSS selector to extract specific elements")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON response")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds (default: 60)")
    parser.add_argument("--balance", action="store_true", help="Check API key balance")
    parser.add_argument("--status", action="store_true", help="Check platform status")

    args = parser.parse_args()

    if args.balance:
        check_balance()
    elif args.status:
        check_status()
    elif args.url:
        crawl(args.url, args.selector, args.timeout, args.raw)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
