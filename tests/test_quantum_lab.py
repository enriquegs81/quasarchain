from datetime import datetime, timezone
import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from quasar_verifier import canonical_payload
from quasar_verifier.quantum_lab import (
    create_signed_passport,
    hash_circuit,
    run_bell_experiment,
    verify_passport,
)


def test_bell_experiment_is_reproducible_and_correlated() -> None:
    first = run_bell_experiment(shots=1024, seed=7)
    second = run_bell_experiment(shots=1024, seed=7)

    assert first.as_dict() == second.as_dict()
    assert first.counts["00"] + first.counts["11"] == 1024
    assert first.counts["00"] > 0
    assert first.counts["11"] > 0
    assert first.counts["01"] == 0
    assert first.counts["10"] == 0
    assert len(first.circuit_hash) == 64


def test_changing_the_circuit_changes_its_hash() -> None:
    bell = run_bell_experiment()
    altered_circuit = list(bell.circuit)
    altered_circuit[0] = {"gate": "X", "qubit": 0}

    assert hash_circuit(altered_circuit) != bell.circuit_hash


def test_signed_passport_verifies_and_detects_tampering() -> None:
    experiment = run_bell_experiment()
    passport = create_signed_passport(
        experiment,
        Ed25519PrivateKey.generate(),
        datetime(2026, 9, 30, tzinfo=timezone.utc),
    )

    assert verify_passport(passport).code == "verified"
    assert passport["software"]["package"] == "quasarchain-verifier"
    assert passport["software"]["python_version"]
    assert passport["software"]["source"] == "src/quasar_verifier/quantum_lab.py"

    passport["experiment"]["counts"]["00"] += 1

    assert verify_passport(passport).code == "invalid_signature"


def test_passport_verification_checks_experiment_consistency() -> None:
    experiment = run_bell_experiment()
    private_key = Ed25519PrivateKey.generate()
    passport = create_signed_passport(
        experiment,
        private_key,
        datetime(2026, 9, 30, tzinfo=timezone.utc),
    )

    passport["experiment"]["circuit_hash"] = "0" * 64
    passport["signing"]["signature"] = base64.urlsafe_b64encode(
        private_key.sign(canonical_payload(passport))
    ).decode("ascii").rstrip("=")

    assert verify_passport(passport).code == "circuit_hash_mismatch"