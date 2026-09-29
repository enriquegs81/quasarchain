"""Qiskit comparison for the reproducible Bell-state laboratory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import qiskit
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

from .quantum_lab import BellExperiment


@dataclass(frozen=True)
class QiskitBellExperiment:
    """Observed output and runtime metadata from Qiskit's local simulator."""

    counts: dict[str, int]
    shots: int
    seed: int
    qiskit_version: str
    backend: str = "BasicSimulator"
    noise_model: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "counts": self.counts,
            "qiskit_version": self.qiskit_version,
            "seed": self.seed,
            "shots": self.shots,
            "noise_model": self.noise_model,
        }


def run_qiskit_bell_experiment(shots: int = 1024, seed: int = 7) -> QiskitBellExperiment:
    """Run the same Bell circuit with Qiskit's local BasicSimulator."""
    if shots <= 0:
        raise ValueError("shots must be positive")

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    result = BasicSimulator().run(circuit, shots=shots, seed_simulator=seed).result()
    raw_counts = result.get_counts()
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in ("00", "01", "10", "11")}
    return QiskitBellExperiment(counts, shots, seed, qiskit.__version__)


def run_qiskit_noisy_bell_experiment(
    shots: int = 1024,
    seed: int = 7,
    readout_error: float = 0.05,
) -> QiskitBellExperiment:
    """Run Bell with symmetric independent readout error on every qubit."""
    if not 0 <= readout_error < 0.5:
        raise ValueError("readout_error must be between 0 and 0.5")

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    noise_model = NoiseModel()
    noise_model.add_all_qubit_readout_error(
        ReadoutError(
            [
                [1 - readout_error, readout_error],
                [readout_error, 1 - readout_error],
            ]
        )
    )
    result = AerSimulator(noise_model=noise_model).run(
        circuit,
        shots=shots,
        seed_simulator=seed,
    ).result()
    raw_counts = result.get_counts()
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in ("00", "01", "10", "11")}
    description = f"symmetric-readout-error:p={readout_error:g}"
    return QiskitBellExperiment(
        counts,
        shots,
        seed,
        qiskit.__version__,
        backend="AerSimulator",
        noise_model=description,
    )


def disagreement_rate(counts: dict[str, int], shots: int) -> float:
    """Return the fraction of two-bit measurements with different bits."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    return (counts.get("01", 0) + counts.get("10", 0)) / shots


def compare_bell_results(
    standard: BellExperiment,
    qiskit_result: QiskitBellExperiment,
) -> dict[str, bool]:
    """Compare invariant behavior without requiring identical RNG sequences."""
    standard_support = {outcome for outcome, count in standard.counts.items() if count}
    qiskit_support = {outcome for outcome, count in qiskit_result.counts.items() if count}
    return {
        "same_shots": standard.shots == qiskit_result.shots,
        "same_nonzero_support": standard_support == qiskit_support,
        "same_counts": standard.counts == qiskit_result.counts,
    }