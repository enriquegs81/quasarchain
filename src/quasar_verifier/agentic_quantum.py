"""Policy-gated agent workflow for proposing a local Bell experiment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .gateway import GatewayResult, PolicyGateway
from .quantum_lab import BellExperiment, create_signed_passport, run_bell_experiment


@dataclass(frozen=True)
class QuantumProposal:
    """The structured request produced by an experiment-planning agent."""

    proposal_id: str
    circuit: str = "bell"
    backend: str = "local"
    shots: int = 1024
    seed: int = 7

    def as_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "circuit": self.circuit,
            "backend": self.backend,
            "shots": self.shots,
            "seed": self.seed,
        }


@dataclass(frozen=True)
class AgenticExperimentResult:
    """Outcome of proposal validation, policy evaluation, and execution."""

    proposal: QuantumProposal
    decision: str
    reason: str
    gateway_result: GatewayResult | None
    passport: dict[str, Any] | None


def execute_agent_proposal(
    proposal: QuantumProposal,
    gateway: PolicyGateway,
    private_key: Ed25519PrivateKey,
    issued_at: datetime,
    *,
    approval_id: str | None = None,
    max_shots: int = 1024,
) -> AgenticExperimentResult:
    """Validate and execute an agent proposal through the local policy gateway."""
    validation_error = _validate_proposal(proposal, max_shots=max_shots)
    if validation_error is not None:
        return AgenticExperimentResult(proposal, "deny", validation_error, None, None)

    completed_experiment: list[BellExperiment] = []

    def execute() -> str:
        completed_experiment.append(run_bell_experiment(proposal.shots, proposal.seed))
        return proposal.proposal_id

    gateway_result = gateway.execute(
        "quantum_simulator",
        "bell.execute",
        execute,
        approval_id=approval_id,
    )
    passport = None
    if completed_experiment:
        passport = create_signed_passport(
            completed_experiment[0],
            private_key,
            issued_at,
            agent_context={
                "proposal": proposal.as_dict(),
                "gateway": {
                    "decision": gateway_result.decision,
                    "approval_id": gateway_result.event.approval_id,
                    "evidence_hash": gateway_result.event.evidence_hash,
                },
            },
        )
    return AgenticExperimentResult(
        proposal,
        gateway_result.decision,
        gateway_result.event.reason,
        gateway_result,
        passport,
    )


def _validate_proposal(proposal: QuantumProposal, *, max_shots: int) -> str | None:
    if proposal.circuit != "bell":
        return "unsupported_circuit"
    if proposal.backend != "local":
        return "unsupported_backend"
    if proposal.shots <= 0:
        return "invalid_shot_count"
    if proposal.shots > max_shots:
        return "shot_limit_exceeded"
    if proposal.seed < 0:
        return "invalid_seed"
    return None