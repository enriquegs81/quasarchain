import json

from quasar_verifier.demo import run_demo


def test_demo_generates_ten_auditable_events(tmp_path) -> None:
    output_path = tmp_path / "demo-evidence.json"

    events = run_demo(output_path)

    assert len(events) == 10
    assert [event["decision"] for event in events].count("allow") == 5
    assert [event["decision"] for event in events].count("review") == 2
    assert [event["decision"] for event in events].count("deny") == 3
    assert events[3]["approval_id"] == "approval-004"
    assert events[8]["reason"] == "agent_revoked"
    assert json.loads(output_path.read_text(encoding="utf-8")) == events
    assert all(len(event["evidence_hash"]) == 64 for event in events)
