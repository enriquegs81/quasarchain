import base64
import copy
import json
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from quasar_verifier import canonical_payload, verify_manifest


FIXED_NOW = datetime(2026, 9, 29, 12, 0, tzinfo=timezone.utc)


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _signed_manifest() -> tuple[dict, Ed25519PrivateKey]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    manifest = {
        "schema": "quasarchain.agent-manifest/v1",
        "agent_id": "did:quasar:agent:support-triage-001",
        "operator_id": "did:quasar:org:pilot-001",
        "name": "Support Triage Agent",
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
        "revocation_endpoint": "https://pilot.invalid/revocations/support-triage-001",
        "signing": {
            "algorithm": "EdDSA",
            "key_id": "did:quasar:org:pilot-001#key-1",
            "public_key": _encode(public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)),
            "signature": "",
        },
    }
    manifest["signing"]["signature"] = _encode(private_key.sign(canonical_payload(manifest)))
    return manifest, private_key


def test_valid_manifest_is_verified() -> None:
    manifest, _ = _signed_manifest()

    result = verify_manifest(manifest, now=FIXED_NOW)

    assert result.valid is True
    assert result.code == "verified"


def test_altered_manifest_is_rejected() -> None:
    manifest, _ = _signed_manifest()
    manifest["version"] = "2.0.0"

    result = verify_manifest(manifest, now=FIXED_NOW)

    assert result.valid is False
    assert result.code == "invalid_signature"


def test_revoked_manifest_is_rejected_before_signature_check() -> None:
    manifest, _ = _signed_manifest()

    result = verify_manifest(
        manifest,
        revoked_agent_ids={manifest["agent_id"]},
        now=FIXED_NOW,
    )

    assert result.valid is False
    assert result.code == "agent_revoked"


def test_expired_manifest_is_rejected() -> None:
    manifest, _ = _signed_manifest()

    result = verify_manifest(
        manifest,
        now=datetime(2026, 11, 1, tzinfo=timezone.utc),
    )

    assert result.valid is False
    assert result.code == "manifest_expired"


def test_result_can_be_serialized_for_an_api() -> None:
    manifest, _ = _signed_manifest()

    result = verify_manifest(manifest, now=FIXED_NOW)

    assert json.loads(json.dumps(result.as_dict()))["code"] == "verified"
