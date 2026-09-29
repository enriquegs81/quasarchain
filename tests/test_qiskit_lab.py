from quasar_verifier.qiskit_lab import (
    compare_bell_results,
    disagreement_rate,
    run_qiskit_bell_experiment,
    run_qiskit_noisy_bell_experiment,
)
from quasar_verifier.quantum_lab import run_bell_experiment


def test_qiskit_bell_experiment_preserves_ideal_support() -> None:
    result = run_qiskit_bell_experiment(shots=1024, seed=7)

    assert result.shots == 1024
    assert result.counts["00"] + result.counts["11"] == 1024
    assert result.counts["01"] == 0
    assert result.counts["10"] == 0
    assert result.qiskit_version == "2.5.2"


def test_comparison_distinguishes_invariants_from_rng_specific_counts() -> None:
    comparison = compare_bell_results(
        run_bell_experiment(shots=1024, seed=7),
        run_qiskit_bell_experiment(shots=1024, seed=7),
    )

    assert comparison["same_shots"] is True
    assert comparison["same_nonzero_support"] is True


def test_readout_noise_introduces_mismatched_measurements() -> None:
    result = run_qiskit_noisy_bell_experiment(shots=1024, seed=7, readout_error=0.05)

    assert result.backend == "AerSimulator"
    assert result.noise_model == "symmetric-readout-error:p=0.05"
    assert sum(result.counts.values()) == 1024
    assert result.counts["01"] + result.counts["10"] > 0
    assert 0 < disagreement_rate(result.counts, result.shots) < 0.5