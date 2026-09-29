"""Validation and Ed25519 verification for agent manifests."""

from __future__ import annotations

import base64
import binascii
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


REQUIRED_FIELDS = {
    "schema",
    "agent_id",
    "operator_id",
    "version",
    "capabilities",
    "tools",
    "issued_at",
    "expires_at",
    "revocation_endpoint",
    "signing",
}
EXPECTED_SCHEMA = "quasarchain.agent-manifest/v1"


@dataclass(frozen=True)
class VerificationResult:
    """Structured result suitable for a CLI, API, or audit event."""

    valid: bool
    code: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "code": self.code,
            "message": self.message,
        }


def canonical_payload(manifest: Mapping[str, Any]) -> bytes:
    """Return the deterministic bytes covered by the manifest signature."""

    unsigned_manifest = dict(manifest)
    signing = dict(unsigned_manifest.get("signing", {}))
    signing.pop("signature", None)
    unsigned_manifest["signing"] = signing
    return json.dumps(
        unsigned_manifest,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def verify_manifest(
    manifest: Mapping[str, Any],
    revoked_agent_ids: Iterable[str] = (),
    now: datetime | None = None,
) -> VerificationResult:
    """Verify structure, lifecycle, revocation, and the Ed25519 signature."""

    structure_error = _validate_structure(manifest)
    if structure_error is not None:
        return structure_error

    agent_id = manifest["agent_id"]
    if agent_id in set(revoked_agent_ids):
        return VerificationResult(False, "agent_revoked", "The agent manifest is revoked")

    try:
        issued_at = _parse_timestamp(manifest["issued_at"])
        expires_at = _parse_timestamp(manifest["expires_at"])
    except ValueError as error:
        return VerificationResult(False, "invalid_timestamp", str(error))

    current_time = now or datetime.now(timezone.utc)
    if issued_at > current_time:
        return VerificationResult(False, "not_yet_valid", "The manifest is not valid yet")
    if expires_at <= current_time:
        return VerificationResult(False, "manifest_expired", "The manifest has expired")
    if expires_at <= issued_at:
        return VerificationResult(False, "invalid_lifetime", "The expiry must be after issuance")

    try:
        public_key = Ed25519PublicKey.from_public_bytes(
            _decode_base64url(manifest["signing"]["public_key"])
        )
        signature = _decode_base64url(manifest["signing"]["signature"])
        public_key.verify(signature, canonical_payload(manifest))
    except (ValueError, TypeError, binascii.Error) as error:
        return VerificationResult(False, "invalid_key_or_encoding", str(error))
    except InvalidSignature:
        return VerificationResult(False, "invalid_signature", "The manifest signature is invalid")

    return VerificationResult(True, "verified", "The manifest is valid")


def _validate_structure(manifest: Mapping[str, Any]) -> VerificationResult | None:
    missing_fields = sorted(REQUIRED_FIELDS - manifest.keys())
    if missing_fields:
        return VerificationResult(
            False,
            "invalid_structure",
            f"Missing required fields: {', '.join(missing_fields)}",
        )

    if manifest["schema"] != EXPECTED_SCHEMA:
        return VerificationResult(False, "unsupported_schema", "Unsupported manifest schema")
    if not isinstance(manifest["capabilities"], list):
        return VerificationResult(False, "invalid_structure", "Capabilities must be a list")
    if not isinstance(manifest["tools"], list) or not manifest["tools"]:
        return VerificationResult(False, "invalid_structure", "Tools must be a non-empty list")

    signing = manifest["signing"]
    if not isinstance(signing, Mapping):
        return VerificationResult(False, "invalid_structure", "Signing must be an object")
    for field in ("algorithm", "key_id", "public_key", "signature"):
        if not isinstance(signing.get(field), str) or not signing[field]:
            return VerificationResult(
                False,
                "invalid_structure",
                f"Signing field '{field}' must be a non-empty string",
            )
    if signing["algorithm"] != "EdDSA":
        return VerificationResult(False, "unsupported_algorithm", "Only EdDSA is supported")
    return None


def _parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Timestamps must be ISO 8601 strings")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Timestamp is not valid ISO 8601") from error
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def _decode_base64url(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)
