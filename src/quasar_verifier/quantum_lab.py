"""Small standard-library Bell-state simulator for the first learning lab."""

from __future__ import annotations

import hashlib
import json
import platform
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from .manifest import VerificationResult, canonical_payload


@dataclass(frozen=True)
class BellExperiment:
    """Reproducible record of one ideal two-qubit circuit experiment."""

    circuit: tuple[dict[str, Any], ...]
    shots: int
    seed: int
    counts: dict[str, int]
    circuit_hash: str
    simulator: str = "stdlib-state-vector"

    def as_dict(self) -> dict[str, Any]:
        return {
            "circuit": list(self.circuit),
            "circuit_hash": self.circuit_hash,
            "counts": self.counts,
            "seed": self.seed,
            "shots": self.shots,
            "simulator": self.simulator,
        }


def run_bell_experiment(shots: int = 1024, seed: int = 7) -> BellExperiment:
    """Prepare |00>, apply H(0) and CNOT(0, 1), then measure both qubits."""
    if shots <= 0:
        raise ValueError("shots must be positive")

    circuit = (
        {"gate": "H", "qubit": 0},
        {"control": 0, "gate": "CNOT", "target": 1},
        {"gate": "MEASURE", "qubits": [0, 1]},
    )
    amplitudes = _apply_hadamard(_zero_state())
    amplitudes = _apply_cnot(amplitudes)
    probabilities = [abs(amplitude) ** 2 for amplitude in amplitudes]
    counts = _sample(probabilities, shots, seed)
    return BellExperiment(
        circuit=circuit,
        shots=shots,
        seed=seed,
        counts=counts,
        circuit_hash=hash_circuit(circuit),
    )


def hash_circuit(circuit: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> str:
    """Hash a canonical JSON representation of the circuit instructions."""
    payload = json.dumps(circuit, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_signed_passport(
    experiment: BellExperiment,
    private_key: Ed25519PrivateKey,
    issued_at: datetime,
    agent_context: Mapping[str, Any] | None = None,
    experiment_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a signed, portable receipt for one Bell experiment."""
    if issued_at.tzinfo is None:
        raise ValueError("issued_at must include a timezone")

    passport: dict[str, Any] = {
        "schema": "quasarchain.quantum-experiment-passport/v1",
        "experiment_id": f"bell-{experiment.circuit_hash[:16]}",
        "issued_at": issued_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "software": {
            "package": "quasarchain-verifier",
            "package_version": "0.1.0",
            "python_implementation": sys.implementation.name,
            "python_version": platform.python_version(),
            "simulator": experiment.simulator,
            "source": "src/quasar_verifier/quantum_lab.py",
        },
        "experiment": experiment.as_dict(),
        "signing": {
            "algorithm": "EdDSA",
            "key_id": "did:quasar:local:quantum-lab#key-1",
            "public_key": _encode(private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)),
            "signature": "",
        },
    }
    if agent_context is not None:
        passport["agent_context"] = dict(agent_context)
    if experiment_context is not None:
        passport["experiment_context"] = dict(experiment_context)
    passport["signing"]["signature"] = _encode(private_key.sign(canonical_payload(passport)))
    return passport


def verify_passport(passport: dict[str, Any]) -> VerificationResult:
    """Verify the structure and signature of a quantum experiment passport."""
    signing = passport.get("signing")
    if passport.get("schema") != "quasarchain.quantum-experiment-passport/v1":
        return VerificationResult(False, "unsupported_schema", "Unsupported passport schema")
    if not isinstance(signing, dict):
        return VerificationResult(False, "invalid_structure", "Signing must be an object")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(_decode(signing["public_key"]))
        public_key.verify(_decode(signing["signature"]), canonical_payload(passport))
    except (KeyError, TypeError, ValueError) as error:
        return VerificationResult(False, "invalid_key_or_encoding", str(error))
    except InvalidSignature:
        return VerificationResult(False, "invalid_signature", "The passport signature is invalid")

    experiment = passport.get("experiment")
    if not isinstance(experiment, dict):
        return VerificationResult(False, "invalid_structure", "Experiment must be an object")
    circuit = experiment.get("circuit")
    if not isinstance(circuit, list) or experiment.get("circuit_hash") != hash_circuit(circuit):
        return VerificationResult(False, "circuit_hash_mismatch", "The circuit hash does not match the circuit")
    counts = experiment.get("counts")
    shots = experiment.get("shots")
    if not isinstance(counts, dict) or not isinstance(shots, int):
        return VerificationResult(False, "invalid_structure", "Counts and shots must be present")
    if sum(counts.values()) != shots:
        return VerificationResult(False, "count_mismatch", "Counts must sum to shots")
    return VerificationResult(True, "verified", "The quantum experiment passport is valid")


def _zero_state() -> list[complex]:
    return [1 + 0j, 0j, 0j, 0j]


def _apply_hadamard(state: list[complex]) -> list[complex]:
    factor = 1 / sqrt(2)
    return [
        (state[0] + state[1]) * factor,
        (state[0] - state[1]) * factor,
        (state[2] + state[3]) * factor,
        (state[2] - state[3]) * factor,
    ]


def _apply_cnot(state: list[complex]) -> list[complex]:
    # Qubit 0 is the least-significant bit: CNOT maps |01> and |11>.
    return [state[0], state[3], state[2], state[1]]


def _sample(probabilities: list[float], shots: int, seed: int) -> dict[str, int]:
    rng = random.Random(seed)
    outcomes = ("00", "01", "10", "11")
    counts = {outcome: 0 for outcome in outcomes}
    for _ in range(shots):
        draw = rng.random()
        cumulative = 0.0
        for outcome, probability in zip(outcomes, probabilities):
            cumulative += probability
            if draw < cumulative:
                counts[outcome] += 1
                break
    return counts


def _encode(value: bytes) -> str:
    import base64

    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _decode(value: str) -> bytes:
    import base64

    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))