from quasar_verifier.console import summarize_events


def test_summary_counts_decisions_and_agents() -> None:
    events = [
        {"agent_id": "agent-a", "decision": "allow", "timestamp": "2026-09-29T12:00:00Z"},
        {"agent_id": "agent-a", "domain_alias": "agent-a.quasarchain.crypto", "decision": "review", "timestamp": "2026-09-29T12:01:00Z"},
        {"agent_id": "agent-b", "decision": "deny", "timestamp": "2026-09-29T12:02:00Z"},
    ]

    assert summarize_events(events) == {
        "total_events": 3,
        "decisions": {"allow": 1, "review": 1, "deny": 1},
        "agents": ["agent-a", "agent-b"],
        "domain_aliases": ["agent-a.quasarchain.crypto"],
        "last_timestamp": "2026-09-29T12:02:00Z",
    }
