from quasar_verifier.qiskit_lab import (
    compare_bell_results,
    disagreement_rate,
    mitigate_readout_counts,
    run_qiskit_bell_experiment,
    run_qiskit_gate_noise_bell_experiment,
    run_qiskit_noisy_bell_experiment,
    run_qiskit_thermal_relaxation_bell_experiment,
    run_observable_model_sweep,
    run_parameter_matched_comparison,
    run_readout_calibration,
    run_noise_sweep,
    run_thermal_sweep,
    summarize_noise_sweep,
    summarize_thermal_sweep,
    summarize_observable_model_sweep,
    wilson_interval,
    zz_correlation,
)
from quasar_verifier.quantum_lab import run_bell_experiment


def test_qiskit_bell_experiment_preserves_ideal_support() -> None:
    result = run_qiskit_bell_experiment(shots=1024, seed=7)

    assert result.shots == 1024
    assert result.counts["00"] + result.counts["11"] == 1024
    assert result.counts["01"] == 0
    assert result.counts["10"] == 0
    assert result.qiskit_version == "2.5.2"


def test_ideal_bell_state_has_x_and_z_correlations() -> None:
    x_result = run_qiskit_bell_experiment(shots=1024, seed=7, measurement_basis="X")

    assert x_result.measurement_basis == "X"
    assert x_result.counts["01"] == 0
    assert x_result.counts["10"] == 0
    assert zz_correlation(x_result.counts, x_result.shots) == 1


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


def test_gate_noise_reduces_bell_correlation() -> None:
    result = run_qiskit_gate_noise_bell_experiment(shots=1024, seed=7, gate_error=0.01)

    assert result.noise_model == "depolarizing-gate-error:p=0.01"
    assert sum(result.counts.values()) == 1024
    assert zz_correlation(result.counts, result.shots) < 1
    assert zz_correlation(result.counts, result.shots) > 0.8


def test_thermal_relaxation_uses_explicit_t1_t2_and_gate_times() -> None:
    result = run_qiskit_thermal_relaxation_bell_experiment(
        shots=1024,
        seed=7,
        t1=50e-6,
        t2=70e-6,
        single_gate_time=50e-9,
        two_gate_time=300e-9,
    )

    assert result.noise_model == "thermal-relaxation:t1=5e-05,t2=7e-05,h=5e-08,cx=3e-07"
    assert sum(result.counts.values()) == 1024
    assert 0.98 < zz_correlation(result.counts, result.shots) < 1


def test_thermal_relaxation_can_be_measured_in_x_basis() -> None:
    result = run_qiskit_thermal_relaxation_bell_experiment(
        shots=1024,
        seed=7,
        t1=50e-6,
        t2=70e-6,
        single_gate_time=50e-9,
        two_gate_time=300e-9,
        measurement_basis="X",
    )

    assert result.measurement_basis == "X"
    assert 0.8 < zz_correlation(result.counts, result.shots) <= 1


def test_readout_calibration_has_one_reference_row_per_basis_state() -> None:
    calibration = run_readout_calibration(shots=1024, seed=7, readout_error=0.05)

    assert set(calibration) == {"00", "01", "10", "11"}
    for prepared_state, observed_counts in calibration.items():
        assert sum(observed_counts.values()) == 1024
        assert observed_counts[prepared_state] > 800


def test_readout_mitigation_improves_bell_correlation_without_clipping() -> None:
    calibration = run_readout_calibration(shots=1024, seed=7, readout_error=0.05)
    observed = run_qiskit_noisy_bell_experiment(shots=1024, seed=7, readout_error=0.05)

    corrected = mitigate_readout_counts(observed.counts, calibration, shots=1024)

    assert abs(sum(corrected.values()) - 1024) < 1e-9
    assert zz_correlation(corrected, 1024) > zz_correlation(observed.counts, 1024)
    assert 0.9 < zz_correlation(corrected, 1024) <= 1.05


def test_readout_mitigation_accepts_different_calibration_shots() -> None:
    calibration = run_readout_calibration(shots=256, seed=7, readout_error=0.05)
    observed = run_qiskit_noisy_bell_experiment(shots=1024, seed=7, readout_error=0.05)

    corrected = mitigate_readout_counts(
        observed.counts,
        calibration,
        shots=1024,
        calibration_shots=256,
    )

    assert abs(sum(corrected.values()) - 1024) < 1e-9


def test_noise_sweep_separates_readout_and_gate_effects() -> None:
    points = run_noise_sweep(shots=256, seeds=(7, 11))
    summary = summarize_noise_sweep(points)

    assert len(points) == 8
    assert summary[(0.0, 0.0)]["mismatch_rate"] == 0
    assert (
        summary[(0.05, 0.0)]["mismatch_rate"]
        > summary[(0.0, 0.01)]["mismatch_rate"]
    )


def test_wilson_interval_contains_a_half_proportion() -> None:
    lower, upper = wilson_interval(50, 100)

    assert lower < 0.5 < upper


def test_thermal_sweep_detects_lower_coherence_times() -> None:
    points = run_thermal_sweep(
        parameter_sets=(
            (50e-6, 70e-6, 50e-9, 300e-9),
            (5e-6, 7e-6, 50e-9, 300e-9),
        ),
        seeds=(7, 11),
        shots=256,
    )
    summary = summarize_thermal_sweep(points)

    assert len(points) == 4
    high_coherence = summary[(50e-6, 70e-6, 50e-9, 300e-9)]
    low_coherence = summary[(5e-6, 7e-6, 50e-9, 300e-9)]
    assert high_coherence["mean_zz"] > low_coherence["mean_zz"]


def test_observable_sweep_compares_models_in_both_bases() -> None:
    points = run_observable_model_sweep(shots=256, seeds=(7, 11))
    summary = summarize_observable_model_sweep(points)

    assert len(points) == 12
    assert set(summary) == {
        ("ideal", "Z"),
        ("ideal", "X"),
        ("depolarizing", "Z"),
        ("depolarizing", "X"),
        ("thermal", "Z"),
        ("thermal", "X"),
    }
    assert summary[("ideal", "Z")]["mean_correlation"] == 1
    assert summary[("ideal", "X")]["mean_correlation"] == 1
    assert summary[("thermal", "Z")]["mean_correlation"] < 0.95
    assert summary[("thermal", "X")]["mean_correlation"] < 0.95


def test_parameter_matched_models_separate_in_x_basis() -> None:
    points = run_observable_model_sweep(
        shots=512,
        seeds=(7, 11),
        depolarizing_gate_error=0.12,
        thermal_parameters=(5e-6, 7e-6, 50e-9, 300e-9),
    )
    summary = summarize_observable_model_sweep(points)

    depolarizing_z = summary[("depolarizing", "Z")]["mean_correlation"]
    thermal_z = summary[("thermal", "Z")]["mean_correlation"]
    depolarizing_x = summary[("depolarizing", "X")]["mean_correlation"]
    thermal_x = summary[("thermal", "X")]["mean_correlation"]
    assert abs(depolarizing_z - thermal_z) < 0.08
    assert thermal_x - depolarizing_x > 0.15


def test_paired_comparison_reports_larger_x_basis_difference() -> None:
    summary = run_parameter_matched_comparison(shots=256, seeds=(7, 11, 13, 17, 19))

    assert summary["X"]["mean_difference"] > summary["Z"]["mean_difference"]
    assert summary["X"]["ci95_lower"] > 0