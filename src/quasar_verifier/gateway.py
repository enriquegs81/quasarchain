"""Policy gateway and execution evidence for the local Trust Layer MVP."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping

from .manifest import verify_manifest


Executor = Callable[[], str]


@dataclass(frozen=True)
class EvidenceEvent:
    """Minimal, exportable evidence for one attempted tool operation."""

    event_id: str
    agent_id: str
    domain_alias: str | None
    agent_version: str
    tool: str
    operation: str
    permission: str | None
    decision: str
    executed: bool
    approval_id: str | None
    reason: str
    timestamp: str
    result_summary: str | None
    evidence_hash: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "agent_id": self.agent_id,
            "domain_alias": self.domain_alias,
            "agent_version": self.agent_version,
            "tool": self.tool,
            "operation": self.operation,
            "permission": self.permission,
            "decision": self.decision,
            "executed": self.executed,
            "approval_id": self.approval_id,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "result_summary": self.result_summary,
            "evidence_hash": self.evidence_hash,
        }


@dataclass(frozen=True)
class GatewayResult:
    """Decision, execution state, and evidence returned to the caller."""

    decision: str
    executed: bool
    result: str | None
    event: EvidenceEvent


class PolicyGateway:
    """Apply manifest and operation policy before calling a tool executor."""

    def __init__(
        self,
        manifest: Mapping[str, Any],
        revoked_agent_ids: Iterable[str] = (),
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._manifest = manifest
        self._revoked_agent_ids = set(revoked_agent_ids)
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def execute(
        self,
        tool: str,
        operation: str,
        executor: Executor,
        *,
        approval_id: str | None = None,
    ) -> GatewayResult:
        """Decide whether to invoke executor and create evidence for the attempt."""

        verification = verify_manifest(
            self._manifest,
            revoked_agent_ids=self._revoked_agent_ids,
            now=self._clock(),
        )
        permission: str | None = None
        decision = "deny"
        reason = verification.code
        result: str | None = None
        executed = False

        if verification.valid:
            declared_operation = self._find_operation(tool, operation)
            if declared_operation is None:
                reason = "operation_not_declared"
            else:
                permission = declared_operation["permission"]
                requested_decision = declared_operation["decision"]
                if requested_decision == "allow":
                    decision = "allow"
                    reason = "policy_allowed"
                    result = executor()
                    executed = True
                elif requested_decision == "review" and approval_id:
                    decision = "allow"
                    reason = "human_approved"
                    result = executor()
                    executed = True
                elif requested_decision == "review":
                    decision = "review"
                    reason = "human_approval_required"
                else:
                    decision = "deny"
                    reason = "policy_denied"

        timestamp = self._clock().astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        event = _build_event(
            agent_id=self._manifest.get("agent_id", "unknown"),
            domain_alias=_domain_alias(self._manifest),
            agent_version=self._manifest.get("version", "unknown"),
            tool=tool,
            operation=operation,
            permission=permission,
            decision=decision,
            executed=executed,
            approval_id=approval_id,
            reason=reason,
            timestamp=timestamp,
            result_summary=result,
        )
        return GatewayResult(decision, executed, result, event)

    def _find_operation(self, tool_name: str, operation_name: str) -> Mapping[str, str] | None:
        for tool in self._manifest.get("tools", []):
            if tool.get("name") != tool_name:
                continue
            for operation in tool.get("operations", []):
                if operation.get("name") == operation_name:
                    return operation
        return None


def _build_event(
    *,
    agent_id: str,
    domain_alias: str | None,
    agent_version: str,
    tool: str,
    operation: str,
    permission: str | None,
    decision: str,
    executed: bool,
    approval_id: str | None,
    reason: str,
    timestamp: str,
    result_summary: str | None,
) -> EvidenceEvent:
    event_id = str(uuid.uuid4())
    evidence = {
        "event_id": event_id,
        "agent_id": agent_id,
        "domain_alias": domain_alias,
        "agent_version": agent_version,
        "tool": tool,
        "operation": operation,
        "permission": permission,
        "decision": decision,
        "executed": executed,
        "approval_id": approval_id,
        "reason": reason,
        "timestamp": timestamp,
        "result_summary": result_summary,
    }
    evidence_hash = hashlib.sha256(
        json.dumps(evidence, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    return EvidenceEvent(**evidence, evidence_hash=evidence_hash)


def _domain_alias(manifest: Mapping[str, Any]) -> str | None:
    naming = manifest.get("naming")
    if not isinstance(naming, Mapping):
        return None
    alias = naming.get("domain")
    return alias if isinstance(alias, str) and alias else None
