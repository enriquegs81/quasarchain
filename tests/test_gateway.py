from datetime import datetime, timezone

from quasar_verifier import PolicyGateway

from test_manifest import FIXED_NOW, _signed_manifest


def test_allowed_operation_is_executed_and_hashed() -> None:
    manifest, _ = _signed_manifest()
    gateway = PolicyGateway(manifest, clock=lambda: FIXED_NOW)

    result = gateway.execute(
        "support_api",
        "customer.read",
        lambda: "customer record found",
    )

    assert result.decision == "allow"
    assert result.executed is True
    assert result.result == "customer record found"
    assert len(result.event.evidence_hash) == 64


def test_undeclared_operation_is_denied_without_execution() -> None:
    manifest, _ = _signed_manifest()
    gateway = PolicyGateway(manifest, clock=lambda: FIXED_NOW)
    called = False

    def executor() -> str:
        nonlocal called
        called = True
        return "should not run"

    result = gateway.execute("support_api", "customer.delete", executor)

    assert result.decision == "deny"
    assert result.executed is False
    assert result.event.reason == "operation_not_declared"
    assert called is False


def test_review_operation_waits_for_human_approval() -> None:
    manifest, _ = _signed_manifest()
    gateway = PolicyGateway(manifest, clock=lambda: FIXED_NOW)

    result = gateway.execute(
        "support_api",
        "customer.export",
        lambda: "export complete",
    )

    assert result.decision == "review"
    assert result.executed is False
    assert result.event.reason == "human_approval_required"


def test_review_operation_executes_after_approval() -> None:
    manifest, _ = _signed_manifest()
    gateway = PolicyGateway(manifest, clock=lambda: FIXED_NOW)

    result = gateway.execute(
        "support_api",
        "customer.export",
        lambda: "export complete",
        approval_id="approval-001",
    )

    assert result.decision == "allow"
    assert result.executed is True
    assert result.event.reason == "human_approved"
    assert result.event.approval_id == "approval-001"


def test_revoked_agent_is_denied_without_execution() -> None:
    manifest, _ = _signed_manifest()
    gateway = PolicyGateway(
        manifest,
        revoked_agent_ids={manifest["agent_id"]},
        clock=lambda: FIXED_NOW,
    )

    result = gateway.execute("support_api", "customer.read", lambda: "should not run")

    assert result.decision == "deny"
    assert result.executed is False
    assert result.event.reason == "agent_revoked"