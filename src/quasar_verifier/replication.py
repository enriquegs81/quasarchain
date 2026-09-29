"""Cross-framework replication report for the Bell-state experiment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .qiskit_lab import QiskitBellExperiment, compare_bell_results, run_qiskit_bell_experiment
from .quantum_lab import BellExperiment, create_signed_passport, run_bell_experiment


@dataclass(frozen=True)
class ReplicationReport:
    """Comparison of two independent implementations of one logical circuit."""

    standard: BellExperiment
    qiskit: QiskitBellExperiment
    comparison: dict[str, bool]

    def as_dict(self) -> dict[str, Any]:
        return {
            "comparison": self.comparison,
            "qiskit": self.qiskit.as_dict(),
            "standard": self.standard.as_dict(),
        }


def run_cross_framework_replication(shots: int = 1024, seed: int = 7) -> ReplicationReport:
    """Run the Bell circuit in both simulators and compare invariant behavior."""
    standard = run_bell_experiment(shots=shots, seed=seed)
    qiskit = run_qiskit_bell_experiment(shots=shots, seed=seed)
    return ReplicationReport(standard, qiskit, compare_bell_results(standard, qiskit))


def create_replicated_passport(
    private_key: Ed25519PrivateKey,
    issued_at: datetime,
    *,
    shots: int = 1024,
    seed: int = 7,
) -> dict[str, Any]:
    """Sign the standard result together with its cross-framework report."""
    report = run_cross_framework_replication(shots=shots, seed=seed)
    return create_signed_passport(
        report.standard,
        private_key,
        issued_at,
        experiment_context={"cross_framework_replication": report.as_dict()},
    )