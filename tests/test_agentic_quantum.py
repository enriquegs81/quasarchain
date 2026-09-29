import base64
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from quasar_verifier import PolicyGateway, canonical_payload
from quasar_verifier.agentic_quantum import QuantumProposal, execute_agent_proposal
from quasar_verifier.quantum_lab import verify_passport


FIXED_NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _review_manifest() -> dict:
    private_key = Ed25519PrivateKey.generate()
    manifest = {
        "schema": "quasarchain.agent-manifest/v1",
        "agent_id": "did:quasar:agent:quantum-planner",
        "operator_id": "did:quasar:org:lab",
        "version": "1.0.0",
        "capabilities": ["propose_bell_experiment"],
        "tools": [
            {
                "name": "quantum_simulator",
                "operations": [
                    {
                        "name": "bell.execute",
                        "permission": "quantum.local.execute",
                        "decision": "review",
                    }
                ],
            }
        ],
        "issued_at": "2026-09-30T00:00:00Z",
        "expires_at": "2026-10-30T00:00:00Z",
        "revocation_endpoint": "https://lab.invalid/revocations/quantum-planner",
        "signing": {
            "algorithm": "EdDSA",
            "key_id": "did:quasar:org:lab#key-1",
            "public_key": _encode(
                private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            ),
            "signature": "",
        },
    }
    manifest["signing"]["signature"] = _encode(private_key.sign(canonical_payload(manifest)))
    return manifest


def test_agent_proposal_requires_human_approval() -> None:
    result = execute_agent_proposal(
        QuantumProposal("proposal-001"),
        PolicyGateway(_review_manifest(), clock=lambda: FIXED_NOW),
        Ed25519PrivateKey.generate(),
        FIXED_NOW,
    )

    assert result.decision == "review"
    assert result.reason == "human_approval_required"
    assert result.gateway_result is not None
    assert result.gateway_result.executed is False
    assert result.passport is None


def test_approved_agent_proposal_links_gateway_evidence_to_passport() -> None:
    result = execute_agent_proposal(
        QuantumProposal("proposal-002"),
        PolicyGateway(_review_manifest(), clock=lambda: FIXED_NOW),
        Ed25519PrivateKey.generate(),
        FIXED_NOW,
        approval_id="approval-quantum-001",
    )

    assert result.decision == "allow"
    assert result.gateway_result is not None
    assert result.gateway_result.executed is True
    assert result.passport is not None
    assert verify_passport(result.passport).code == "verified"
    assert result.passport["agent_context"]["proposal"]["proposal_id"] == "proposal-002"
    assert (
        result.passport["agent_context"]["gateway"]["evidence_hash"]
        == result.gateway_result.event.evidence_hash
    )


def test_agent_rejects_a_proposal_that_exceeds_the_shot_limit() -> None:
    result = execute_agent_proposal(
        QuantumProposal("proposal-003", shots=2048),
        PolicyGateway(_review_manifest(), clock=lambda: FIXED_NOW),
        Ed25519PrivateKey.generate(),
        FIXED_NOW,
    )

    assert result.decision == "deny"
    assert result.reason == "shot_limit_exceeded"
    assert result.gateway_result is None
    assert result.passport is None