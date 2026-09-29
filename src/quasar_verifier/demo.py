"""Ten-execution support_api demonstration for the Trust Layer MVP."""

from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from .gateway import GatewayResult, PolicyGateway
from .manifest import canonical_payload


DEMO_NOW = datetime(2026, 9, 29, 12, 0, tzinfo=timezone.utc)


def run_demo(output_path: Path | None = None) -> list[dict[str, Any]]:
    manifest = _signed_demo_manifest()
    revoked_agent_ids: set[str] = set()
    gateway = PolicyGateway(manifest, clock=lambda: DEMO_NOW)
    results: list[GatewayResult] = []

    results.append(gateway.execute("support_api", "customer.read", lambda: "customer record found"))
    results.append(gateway.execute("support_api", "ticket.create", lambda: "ticket created"))
    results.append(gateway.execute("support_api", "customer.export", lambda: "export complete"))
    results.append(
        gateway.execute(
            "support_api",
            "customer.export",
            lambda: "export complete",
            approval_id="approval-004",
        )
    )
    results.append(gateway.execute("support_api", "customer.delete", lambda: "should not run"))
    results.append(gateway.execute("support_api", "customer.read", lambda: "customer record found"))
    results.append(gateway.execute("support_api", "ticket.create", lambda: "ticket created"))
    results.append(gateway.execute("support_api", "customer.export", lambda: "export complete"))

    revoked_agent_ids.add(manifest["agent_id"])
    gateway = PolicyGateway(
        manifest,
        revoked_agent_ids=revoked_agent_ids,
        clock=lambda: DEMO_NOW,
    )
    results.append(gateway.execute("support_api", "customer.read", lambda: "should not run"))
    results.append(gateway.execute("support_api", "ticket.create", lambda: "should not run"))

    events = [result.event.as_dict() for result in results]
    if output_path is not None:
        output_path.write_text(json.dumps(events, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the QuasarChain support_api demo")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("demo-evidence.json"),
        help="Output JSON path (default: demo-evidence.json)",
    )
    arguments = parser.parse_args()
    events = run_demo(arguments.output)
    print(json.dumps({"events": len(events), "output": str(arguments.output)}, ensure_ascii=True))
    return 0


def _signed_demo_manifest() -> dict[str, Any]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    manifest: dict[str, Any] = {
        "schema": "quasarchain.agent-manifest/v1",
        "agent_id": "did:quasar:agent:support-triage-demo",
        "operator_id": "did:quasar:org:demo",
        "name": "Support Triage Demo Agent",
        "naming": {
            "domain": "support-triage.quasarchain.crypto",
            "namespace": "quasarchain.crypto",
            "verification_uri": "http://127.0.0.1:8765/verify/support-triage",
        },
        "version": "1.0.0",
        "environment": "sandbox",
        "capabilities": ["read_customer_record", "create_support_ticket"],
        "tools": [
            {
                "name": "support_api",
                "operations": [
                    {
                        "name": "customer.read",
                        "permission": "support.customer.read",
                        "decision": "allow",
                    },
                    {
                        "name": "ticket.create",
                        "permission": "support.ticket.create",
                        "decision": "allow",
                    },
                    {
                        "name": "customer.export",
                        "permission": "support.customer.export",
                        "decision": "review",
                    },
                ],
            }
        ],
        "issued_at": "2026-09-29T00:00:00Z",
        "expires_at": "2026-10-29T00:00:00Z",
        "revocation_endpoint": "https://demo.invalid/revocations/support-triage-demo",
        "signing": {
            "algorithm": "EdDSA",
            "key_id": "did:quasar:org:demo#key-1",
            "public_key": _encode(public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)),
            "signature": "",
        },
    }
    manifest["signing"]["signature"] = _encode(private_key.sign(canonical_payload(manifest)))
    return manifest


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


if __name__ == "__main__":
    raise SystemExit(main())
