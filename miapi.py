#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCHEMA = "desarrollamo.miapi.v1"
UA = "MiAPI/1.0 (+https://github.com/amoedo7/MiAPI)"


def parse_headers(values: list[str]) -> dict[str, str]:
    out = {}
    for item in values:
        if ":" not in item:
            raise ValueError(f"Header inválido: {item}")
        k, v = item.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def inspect(url: str, method: str, headers: dict[str, str], json_body: str | None, include_body: bool) -> dict:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("La URL debe comenzar con http:// o https://")
    body = None
    request_headers = {"User-Agent": UA, **headers}
    if json_body is not None:
        parsed_json = json.loads(json_body)
        body = json.dumps(parsed_json, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, method=method.upper(), headers=request_headers)
    started = time.perf_counter()
    raw = b""
    status = None
    final_url = url
    response_headers = {}
    error = None
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read(2_000_000)
            status = getattr(r, "status", 200)
            final_url = r.geturl()
            response_headers = dict(r.headers.items())
    except urllib.error.HTTPError as e:
        raw = e.read(2_000_000) if e.fp else b""
        status = e.code
        final_url = e.geturl()
        response_headers = dict(e.headers.items())
        error = "HTTPError"
    except Exception as exc:
        error = exc.__class__.__name__
    elapsed = round((time.perf_counter() - started) * 1000, 1)
    content_type = next((v for k, v in response_headers.items() if k.lower() == "content-type"), None)
    text = raw.decode("utf-8", errors="replace")
    is_json = False
    json_type = None
    try:
        obj = json.loads(text) if text else None
        if text:
            is_json = True
            json_type = type(obj).__name__
    except Exception:
        pass
    response = {
        "status": status,
        "ok": bool(status and 200 <= status < 400),
        "final_url": final_url,
        "elapsed_ms": elapsed,
        "bytes_read": len(raw),
        "content_type": content_type,
        "is_json": is_json,
        "json_type": json_type,
        "headers": response_headers,
        "error": error,
    }
    if include_body:
        response["body_preview"] = text[:4000]
    return {
        "schema": SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "request": {
            "method": method.upper(),
            "url": url,
            "header_names": sorted(request_headers.keys()),
            "header_values_recorded": False,
            "body_sent": json_body is not None,
        },
        "response": response,
    }


def self_test() -> dict:
    return {
        "schema": SCHEMA,
        "self_test": True,
        "request": {"method": "GET", "url": "https://example.invalid", "header_values_recorded": False},
        "response": {"status": None, "is_json": False},
    }


def main() -> int:
    p = argparse.ArgumentParser(description="MiAPI: inspector HTTP/JSON portátil")
    p.add_argument("url", nargs="?")
    p.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"])
    p.add_argument("--header", action="append", default=[])
    p.add_argument("--json", dest="json_body")
    p.add_argument("--include-body", action="store_true")
    p.add_argument("--output")
    p.add_argument("--compact", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        report = self_test()
    else:
        if not args.url:
            p.error("falta URL")
        report = inspect(args.url, args.method, parse_headers(args.header), args.json_body, args.include_body)
    text = json.dumps(report, ensure_ascii=False, indent=None if args.compact else 2)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
