#!/usr/bin/env python3
"""Porkbun DNS helper — list / create / delete A and CNAME records.

Usage:
    export PORKBUN_API_KEY=pk1_...
    export PORKBUN_API_SECRET=sk1_...

    # List current records for netguardir.com
    ./porkbun_dns.py list netguardir.com

    # Point apex A → 1.2.3.4 (e.g., your external host)
    ./porkbun_dns.py upsert netguardir.com A @ 1.2.3.4 --ttl 600

    # Point www → apex via CNAME
    ./porkbun_dns.py upsert netguardir.com CNAME www netguardir.com --ttl 600

    # Delete one
    ./porkbun_dns.py delete netguardir.com <RECORD_ID>

Skip the script entirely if you're using Porkbun static hosting — that auto-
provisions DNS for you. This helper is for the "external host + Porkbun DNS"
deployment path.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request


API_BASE = "https://api.porkbun.com/api/json/v3"


def _auth() -> dict:
    key = os.environ.get("PORKBUN_API_KEY")
    secret = os.environ.get("PORKBUN_API_SECRET")
    if not key or not secret:
        sys.exit("error: set PORKBUN_API_KEY and PORKBUN_API_SECRET environment variables")
    return {"apikey": key, "secretapikey": secret}


def _post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"error: HTTP {exc.code} — {body}")


def cmd_ping(args) -> int:
    out = _post("/ping", _auth())
    print(json.dumps(out, indent=2))
    return 0 if out.get("status") == "SUCCESS" else 1


def cmd_list(args) -> int:
    payload = dict(_auth())
    out = _post(f"/dns/retrieve/{args.domain}", payload)
    if out.get("status") != "SUCCESS":
        print(json.dumps(out, indent=2)); return 1
    rows = out.get("records", [])
    if not rows:
        print("(no records)"); return 0
    print(f"{'ID':<12} {'TYPE':<6} {'NAME':<32} {'CONTENT':<40} TTL")
    for r in rows:
        print(f"{r['id']:<12} {r['type']:<6} {r['name']:<32} {r['content'][:38]:<40} {r.get('ttl','')}")
    return 0


def cmd_upsert(args) -> int:
    """Create or replace a record with given (type, name) pair."""
    payload = dict(_auth())
    payload.update({
        "name": "" if args.name == "@" else args.name,
        "type": args.type,
        "content": args.content,
        "ttl": str(args.ttl),
    })

    # Delete any existing record with same (type, name)
    auth = _auth()
    listing = _post(f"/dns/retrieveByNameType/{args.domain}/{args.type}/{payload['name']}", auth)
    if listing.get("status") == "SUCCESS":
        for existing in listing.get("records", []):
            print(f"  removing existing {existing['type']} record id={existing['id']}")
            _post(f"/dns/delete/{args.domain}/{existing['id']}", auth)

    out = _post(f"/dns/create/{args.domain}", payload)
    if out.get("status") != "SUCCESS":
        print(json.dumps(out, indent=2)); return 1
    print(f"  ✓ created {args.type} {args.name} → {args.content} (id={out.get('id')})")
    return 0


def cmd_delete(args) -> int:
    out = _post(f"/dns/delete/{args.domain}/{args.id}", _auth())
    if out.get("status") != "SUCCESS":
        print(json.dumps(out, indent=2)); return 1
    print(f"  ✓ deleted record {args.id}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="porkbun_dns.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("ping", help="verify API credentials")
    sp.set_defaults(fn=cmd_ping)

    sp = sub.add_parser("list", help="list DNS records for DOMAIN")
    sp.add_argument("domain")
    sp.set_defaults(fn=cmd_list)

    sp = sub.add_parser("upsert", help="create-or-replace a DNS record")
    sp.add_argument("domain")
    sp.add_argument("type", choices=["A", "AAAA", "CNAME", "TXT", "MX"])
    sp.add_argument("name", help="@ for apex, www for www, etc.")
    sp.add_argument("content")
    sp.add_argument("--ttl", type=int, default=600)
    sp.set_defaults(fn=cmd_upsert)

    sp = sub.add_parser("delete", help="delete a DNS record by ID")
    sp.add_argument("domain")
    sp.add_argument("id")
    sp.set_defaults(fn=cmd_delete)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
