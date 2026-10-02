"""Qiskit comparison for the reproducible Bell-state laboratory."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from statistics import mean, stdev
from typing import Any

import numpy as np
import qiskit
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    ReadoutError,
    depolarizing_error,
    thermal_relaxation_error,
)

from .quantum_lab import BellExperiment


OUTCOMES = ("00", "01", "10", "11")


@dataclass(frozen=True)
class QiskitBellExperiment:
    """Observed output and runtime metadata from Qiskit's local simulator."""

    counts: dict[str, int]
    shots: int
    seed: int
    qiskit_version: str
    backend: str = "BasicSimulator"
    noise_model: str | None = None
    measurement_basis: str = "Z"

    def as_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "counts": self.counts,
            "qiskit_version": self.qiskit_version,
            "seed": self.seed,
            "shots": self.shots,
            "noise_model": self.noise_model,
            "measurement_basis": self.measurement_basis,
        }


@dataclass(frozen=True)
class NoiseSweepPoint:
    """One repeated observation in a two-parameter noise sweep."""

    readout_error: float
    gate_error: float
    seed: int
    shots: int
    counts: dict[str, int]
    mismatch_rate: float
    zz_correlation: float


@dataclass(frozen=True)
class ThermalSweepPoint:
    """One repeated Bell observation under a thermal-relaxation parameter set."""

    t1: float
    t2: float
    single_gate_time: float
    two_gate_time: float
    seed: int
    shots: int
    counts: dict[str, int]
    zz_correlation: float


@dataclass(frozen=True)
class ObservableSweepPoint:
    """One observable measured under one noise model and seed."""

    model: str
    measurement_basis: str
    seed: int
    shots: int
    counts: dict[str, int]
    correlation: float


def _bell_circuit(measurement_basis: str = "Z") -> QuantumCircuit:
    if measurement_basis not in {"X", "Z"}:
        raise ValueError("measurement_basis must be 'X' or 'Z'")
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    if measurement_basis == "X":
        circuit.h(0)
        circuit.h(1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def run_qiskit_bell_experiment(
    shots: int = 1024,
    seed: int = 7,
    measurement_basis: str = "Z",
) -> QiskitBellExperiment:
    """Run the same Bell circuit with Qiskit's local BasicSimulator."""
    if shots <= 0:
        raise ValueError("shots must be positive")

    circuit = _bell_circuit(measurement_basis)
    result = BasicSimulator().run(circuit, shots=shots, seed_simulator=seed).result()
    raw_counts = result.get_counts()
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES}
    return QiskitBellExperiment(
        counts,
        shots,
        seed,
        qiskit.__version__,
        measurement_basis=measurement_basis,
    )


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
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES}
    description = f"symmetric-readout-error:p={readout_error:g}"
    return QiskitBellExperiment(
        counts,
        shots,
        seed,
        qiskit.__version__,
        backend="AerSimulator",
        noise_model=description,
    )


def run_readout_calibration(
    shots: int = 1024,
    seed: int = 7,
    readout_error: float = 0.05,
) -> dict[str, dict[str, int]]:
    """Measure computational-basis states to estimate readout confusion."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if not 0 <= readout_error < 0.5:
        raise ValueError("readout_error must be between 0 and 0.5")

    noise_model = NoiseModel()
    noise_model.add_all_qubit_readout_error(
        ReadoutError(
            [
                [1 - readout_error, readout_error],
                [readout_error, 1 - readout_error],
            ]
        )
    )
    calibration: dict[str, dict[str, int]] = {}
    for prepared_state in ("00", "01", "10", "11"):
        circuit = QuantumCircuit(2, 2)
        for qubit, bit in enumerate(reversed(prepared_state)):
            if bit == "1":
                circuit.x(qubit)
        circuit.measure([0, 1], [0, 1])
        raw_counts = AerSimulator(noise_model=noise_model).run(
            circuit,
            shots=shots,
            seed_simulator=seed,
        ).result().get_counts()
        calibration[prepared_state] = {
            outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES
        }
    return calibration


def run_qiskit_gate_noise_bell_experiment(
    shots: int = 1024,
    seed: int = 7,
    gate_error: float = 0.01,
    measurement_basis: str = "Z",
) -> QiskitBellExperiment:
    """Run Bell with depolarizing errors after H and CNOT gates."""
    if not 0 <= gate_error <= 1:
        raise ValueError("gate_error must be between 0 and 1")

    circuit = _bell_circuit(measurement_basis)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(depolarizing_error(gate_error, 1), ["h"])
    noise_model.add_all_qubit_quantum_error(depolarizing_error(gate_error, 2), ["cx"])
    result = AerSimulator(noise_model=noise_model).run(
        circuit,
        shots=shots,
        seed_simulator=seed,
    ).result()
    raw_counts = result.get_counts()
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES}
    description = f"depolarizing-gate-error:p={gate_error:g}"
    return QiskitBellExperiment(
        counts,
        shots,
        seed,
        qiskit.__version__,
        backend="AerSimulator",
        noise_model=description,
        measurement_basis=measurement_basis,
    )


def run_qiskit_thermal_relaxation_bell_experiment(
    shots: int = 1024,
    seed: int = 7,
    t1: float = 50e-6,
    t2: float = 70e-6,
    single_gate_time: float = 50e-9,
    two_gate_time: float = 300e-9,
    measurement_basis: str = "Z",
) -> QiskitBellExperiment:
    """Run Bell with thermal relaxation after one- and two-qubit gates."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if t1 <= 0 or t2 <= 0 or t2 > 2 * t1:
        raise ValueError("require 0 < t2 <= 2 * t1")
    if single_gate_time <= 0 or two_gate_time <= 0:
        raise ValueError("gate times must be positive")

    circuit = _bell_circuit(measurement_basis)
    noise_model = NoiseModel()
    one_qubit_error = thermal_relaxation_error(t1, t2, single_gate_time)
    two_qubit_error = thermal_relaxation_error(t1, t2, two_gate_time).tensor(
        thermal_relaxation_error(t1, t2, two_gate_time)
    )
    noise_model.add_all_qubit_quantum_error(one_qubit_error, ["h"])
    noise_model.add_all_qubit_quantum_error(two_qubit_error, ["cx"])
    result = AerSimulator(noise_model=noise_model).run(
        circuit,
        shots=shots,
        seed_simulator=seed,
    ).result()
    raw_counts = result.get_counts()
    counts = {outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES}
    description = (
        f"thermal-relaxation:t1={t1:g},t2={t2:g},"
        f"h={single_gate_time:g},cx={two_gate_time:g}"
    )
    return QiskitBellExperiment(
        counts,
        shots,
        seed,
        qiskit.__version__,
        backend="AerSimulator",
        noise_model=description,
        measurement_basis=measurement_basis,
    )


def run_thermal_sweep(
    *,
    parameter_sets: tuple[tuple[float, float, float, float], ...] = (
        (50e-6, 70e-6, 50e-9, 300e-9),
        (5e-6, 7e-6, 50e-9, 300e-9),
        (1e-6, 1.5e-6, 50e-9, 300e-9),
    ),
    seeds: tuple[int, ...] = (7, 11, 13),
    shots: int = 1024,
) -> list[ThermalSweepPoint]:
    """Repeat Bell simulations over T1, T2, and gate-duration regimes."""
    if not seeds:
        raise ValueError("seeds must not be empty")
    points: list[ThermalSweepPoint] = []
    for t1, t2, single_gate_time, two_gate_time in parameter_sets:
        for seed in seeds:
            result = run_qiskit_thermal_relaxation_bell_experiment(
                shots=shots,
                seed=seed,
                t1=t1,
                t2=t2,
                single_gate_time=single_gate_time,
                two_gate_time=two_gate_time,
            )
            points.append(
                ThermalSweepPoint(
                    t1,
                    t2,
                    single_gate_time,
                    two_gate_time,
                    seed,
                    shots,
                    result.counts,
                    zz_correlation(result.counts, shots),
                )
            )
    return points


def summarize_thermal_sweep(
    points: list[ThermalSweepPoint],
) -> dict[tuple[float, float, float, float], dict[str, float]]:
    """Summarize mean, minimum, and maximum ZZ correlation per regime."""
    if not points:
        raise ValueError("points must not be empty")
    grouped: dict[tuple[float, float, float, float], list[float]] = {}
    for point in points:
        parameters = (point.t1, point.t2, point.single_gate_time, point.two_gate_time)
        grouped.setdefault(parameters, []).append(point.zz_correlation)
    return {
        parameters: {
            "observations": float(len(values)),
            "mean_zz": mean(values),
            "min_zz": min(values),
            "max_zz": max(values),
        }
        for parameters, values in grouped.items()
    }


def mitigate_readout_counts(
    observed_counts: Mapping[str, int],
    calibration: Mapping[str, Mapping[str, int]],
    shots: int,
    calibration_shots: int | None = None,
) -> dict[str, float]:
    """Invert a calibrated readout matrix without clipping statistical estimates."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    calibration_shots = calibration_shots or shots
    if calibration_shots <= 0:
        raise ValueError("calibration_shots must be positive")
    try:
        matrix = np.asarray(
            [
                [calibration[prepared][observed] / calibration_shots for observed in OUTCOMES]
                for prepared in OUTCOMES
            ],
            dtype=float,
        )
        measured = np.asarray(
            [observed_counts[outcome] / shots for outcome in OUTCOMES],
            dtype=float,
        )
    except KeyError as error:
        raise ValueError(f"missing calibration outcome: {error.args[0]}") from error
    if not np.allclose(matrix.sum(axis=1), 1.0):
        raise ValueError("each calibration row must sum to calibration_shots")
    try:
        corrected_probabilities = np.linalg.solve(matrix.T, measured)
    except np.linalg.LinAlgError as error:
        raise ValueError("the readout calibration matrix is singular") from error
    return {
        outcome: float(probability * shots)
        for outcome, probability in zip(OUTCOMES, corrected_probabilities)
    }


def disagreement_rate(counts: Mapping[str, float], shots: int) -> float:
    """Return the fraction of two-bit measurements with different bits."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    return (counts.get("01", 0) + counts.get("10", 0)) / shots


def zz_correlation(counts: Mapping[str, float], shots: int) -> float:
    """Estimate the Z tensor Z correlation from computational-basis counts."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    return (
        counts.get("00", 0)
        + counts.get("11", 0)
        - counts.get("01", 0)
        - counts.get("10", 0)
    ) / shots


def run_noise_sweep(
    *,
    readout_errors: tuple[float, ...] = (0.0, 0.05),
    gate_errors: tuple[float, ...] = (0.0, 0.01),
    seeds: tuple[int, ...] = (7, 11, 13),
    shots: int = 1024,
) -> list[NoiseSweepPoint]:
    """Run a reproducible two-factor sweep over readout and gate noise."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if not seeds:
        raise ValueError("seeds must not be empty")
    if any(not 0 <= value < 0.5 for value in readout_errors):
        raise ValueError("readout_errors must be between 0 and 0.5")
    if any(not 0 <= value <= 1 for value in gate_errors):
        raise ValueError("gate_errors must be between 0 and 1")

    points: list[NoiseSweepPoint] = []
    for readout_error in readout_errors:
        for gate_error in gate_errors:
            for seed in seeds:
                circuit = QuantumCircuit(2, 2)
                circuit.h(0)
                circuit.cx(0, 1)
                circuit.measure([0, 1], [0, 1])
                noise_model = NoiseModel()
                if gate_error:
                    noise_model.add_all_qubit_quantum_error(
                        depolarizing_error(gate_error, 1), ["h"]
                    )
                    noise_model.add_all_qubit_quantum_error(
                        depolarizing_error(gate_error, 2), ["cx"]
                    )
                if readout_error:
                    noise_model.add_all_qubit_readout_error(
                        ReadoutError(
                            [
                                [1 - readout_error, readout_error],
                                [readout_error, 1 - readout_error],
                            ]
                        )
                    )
                simulator = AerSimulator(noise_model=noise_model)
                raw_counts = simulator.run(
                    circuit,
                    shots=shots,
                    seed_simulator=seed,
                ).result().get_counts()
                counts = {
                    outcome: int(raw_counts.get(outcome, 0)) for outcome in OUTCOMES
                }
                points.append(
                    NoiseSweepPoint(
                        readout_error,
                        gate_error,
                        seed,
                        shots,
                        counts,
                        disagreement_rate(counts, shots),
                        zz_correlation(counts, shots),
                    )
                )
    return points


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Return a Wilson confidence interval for a binomial proportion."""
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("successes must be between zero and trials")
    proportion = successes / trials
    denominator = 1 + z**2 / trials
    center = (proportion + z**2 / (2 * trials)) / denominator
    margin = (
        z
        * ((proportion * (1 - proportion) / trials + z**2 / (4 * trials**2)) ** 0.5)
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def summarize_noise_sweep(points: list[NoiseSweepPoint]) -> dict[tuple[float, float], dict[str, Any]]:
    """Aggregate mismatch and ZZ estimates with 95% Wilson intervals."""
    if not points:
        raise ValueError("points must not be empty")
    grouped: dict[tuple[float, float], list[NoiseSweepPoint]] = {}
    for point in points:
        grouped.setdefault((point.readout_error, point.gate_error), []).append(point)

    summary: dict[tuple[float, float], dict[str, Any]] = {}
    for parameters, observations in grouped.items():
        shots = sum(point.shots for point in observations)
        mismatches = sum(point.counts["01"] + point.counts["10"] for point in observations)
        mismatch_rate = mismatches / shots
        mismatch_interval = wilson_interval(mismatches, shots)
        summary[parameters] = {
            "observations": len(observations),
            "shots": shots,
            "mismatch_rate": mismatch_rate,
            "mismatch_ci95": mismatch_interval,
            "zz_correlation": 1 - 2 * mismatch_rate,
            "zz_ci95": (1 - 2 * mismatch_interval[1], 1 - 2 * mismatch_interval[0]),
        }
    return summary


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


def run_observable_model_sweep(
    *,
    shots: int = 4096,
    seeds: tuple[int, ...] = (7, 11, 13),
    depolarizing_gate_error: float = 0.01,
    thermal_parameters: tuple[float, float, float, float] = (
        5e-6,
        7e-6,
        50e-9,
        300e-9,
    ),
) -> list[ObservableSweepPoint]:
    """Compare ideal, depolarizing, and thermal models in Z and X bases."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if not seeds:
        raise ValueError("seeds must not be empty")
    t1, t2, single_gate_time, two_gate_time = thermal_parameters

    points: list[ObservableSweepPoint] = []
    for basis in ("Z", "X"):
        for seed in seeds:
            ideal = run_qiskit_bell_experiment(
                shots=shots,
                seed=seed,
                measurement_basis=basis,
            )
            points.append(
                ObservableSweepPoint(
                    "ideal", basis, seed, shots, ideal.counts, zz_correlation(ideal.counts, shots)
                )
            )
            depolarizing = run_qiskit_gate_noise_bell_experiment(
                shots=shots,
                seed=seed,
                gate_error=depolarizing_gate_error,
                measurement_basis=basis,
            )
            points.append(
                ObservableSweepPoint(
                    "depolarizing", basis, seed, shots, depolarizing.counts,
                    zz_correlation(depolarizing.counts, shots),
                )
            )
            thermal = run_qiskit_thermal_relaxation_bell_experiment(
                shots=shots,
                seed=seed,
                t1=t1,
                t2=t2,
                single_gate_time=single_gate_time,
                two_gate_time=two_gate_time,
                measurement_basis=basis,
            )
            points.append(
                ObservableSweepPoint(
                    "thermal", basis, seed, shots, thermal.counts,
                    zz_correlation(thermal.counts, shots),
                )
            )
    return points


def summarize_observable_model_sweep(
    points: list[ObservableSweepPoint],
) -> dict[tuple[str, str], dict[str, float]]:
    """Summarize mean and sample standard deviation by model and basis."""
    if not points:
        raise ValueError("points must not be empty")
    grouped: dict[tuple[str, str], list[float]] = {}
    for point in points:
        grouped.setdefault((point.model, point.measurement_basis), []).append(point.correlation)
    return {
        key: {
            "observations": float(len(values)),
            "mean_correlation": mean(values),
            "sample_std": stdev(values) if len(values) > 1 else 0.0,
        }
        for key, values in grouped.items()
    }


def run_parameter_matched_comparison(
    *,
    shots: int = 4096,
    seeds: tuple[int, ...] = tuple(range(7, 37)),
    depolarizing_gate_error: float = 0.12,
    thermal_parameters: tuple[float, float, float, float] = (
        5e-6,
        7e-6,
        50e-9,
        300e-9,
    ),
) -> dict[str, dict[str, float]]:
    """Estimate paired thermal-minus-depolarizing differences by basis."""
    if shots <= 0 or not seeds:
        raise ValueError("shots must be positive and seeds must not be empty")
    t1, t2, single_gate_time, two_gate_time = thermal_parameters
    differences: dict[str, list[float]] = {"Z": [], "X": []}
    for basis in ("Z", "X"):
        for seed in seeds:
            depolarizing = run_qiskit_gate_noise_bell_experiment(
                shots=shots,
                seed=seed,
                gate_error=depolarizing_gate_error,
                measurement_basis=basis,
            )
            thermal = run_qiskit_thermal_relaxation_bell_experiment(
                shots=shots,
                seed=seed,
                t1=t1,
                t2=t2,
                single_gate_time=single_gate_time,
                two_gate_time=two_gate_time,
                measurement_basis=basis,
            )
            differences[basis].append(
                zz_correlation(thermal.counts, shots)
                - zz_correlation(depolarizing.counts, shots)
            )

    summary: dict[str, dict[str, float]] = {}
    for basis, values in differences.items():
        average = mean(values)
        standard_error = stdev(values) / (len(values) ** 0.5) if len(values) > 1 else 0.0
        summary[basis] = {
            "observations": float(len(values)),
            "mean_difference": average,
            "ci95_lower": average - 1.96 * standard_error,
            "ci95_upper": average + 1.96 * standard_error,
        }
    return summary