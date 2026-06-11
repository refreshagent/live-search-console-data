#!/usr/bin/env python3
"""Authenticated RefreshAgent REST helper."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


def parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected KEY=VALUE")
    key, raw = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("parameter key cannot be empty")
    return key, raw


def build_url(base_url: str, path: str, params: list[tuple[str, str]]) -> str:
    base = base_url.rstrip("/") + "/"
    url = urljoin(base, path.lstrip("/"))
    if params:
        url = f"{url}?{urlencode(params)}"
    return url


def load_body(raw_json: str | None) -> bytes | None:
    if raw_json is None:
        return None
    try:
        parsed: Any = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON body: {exc}") from exc
    return json.dumps(parsed, separators=(",", ":")).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Call RefreshAgent API endpoints.")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    parser.add_argument("path", help="API path, e.g. /api/v1/sc/sites")
    parser.add_argument("--param", action="append", default=[], type=parse_key_value, help="Query parameter as KEY=VALUE")
    parser.add_argument("--json", dest="json_body", help="JSON request body for POST/PUT/PATCH")
    parser.add_argument("--base-url", default=os.environ.get("REFRESHAGENT_BASE_URL", "https://refreshagent.com"))
    parser.add_argument("--api-key", default=os.environ.get("REFRESHAGENT_API_KEY"))
    args = parser.parse_args()

    if not args.api_key:
        print("Missing API key. Set REFRESHAGENT_API_KEY or pass --api-key.", file=sys.stderr)
        return 2

    body = load_body(args.json_body)
    url = build_url(args.base_url, args.path, args.param)
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 RefreshAgentSkill/1.0",
        "X-API-Key": args.api_key,
    }
    if body is not None:
        headers["Content-Type"] = "application/json"

    request = Request(url, data=body, headers=headers, method=args.method)

    try:
        with urlopen(request, timeout=60) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        error_payload = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code} {exc.reason}: {error_payload}", file=sys.stderr)
        return 1
    except URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        return 1

    try:
        print(json.dumps(json.loads(payload), indent=2, sort_keys=True))
    except json.JSONDecodeError:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
