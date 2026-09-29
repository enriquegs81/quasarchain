from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from quasar_verifier.quantum_lab import verify_passport
from quasar_verifier.replication import create_replicated_passport, run_cross_framework_replication


def test_cross_framework_replication_compares_invariants() -> None:
    report = run_cross_framework_replication(shots=1024, seed=7)

    assert report.comparison["same_shots"] is True
    assert report.comparison["same_nonzero_support"] is True
    assert set(report.standard.counts) == set(report.qiskit.counts)


def test_replicated_report_is_inside_the_signed_passport() -> None:
    passport = create_replicated_passport(
        Ed25519PrivateKey.generate(),
        datetime(2026, 9, 30, tzinfo=timezone.utc),
    )

    assert verify_passport(passport).code == "verified"
    replication = passport["experiment_context"]["cross_framework_replication"]
    assert replication["comparison"]["same_nonzero_support"] is True
    assert replication["qiskit"]["backend"] == "BasicSimulator"