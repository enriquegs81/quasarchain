"""Command-line entry point for manifest verification."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .manifest import verify_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a QuasarChain agent manifest")
    parser.add_argument("manifest", type=Path, help="Path to a JSON manifest")
    parser.add_argument(
        "--revoked-agent",
        action="append",
        default=[],
        help="Agent ID that should be treated as revoked; repeatable",
    )
    parser.add_argument(
        "--now",
        help="ISO 8601 timestamp used for deterministic verification",
    )
    arguments = parser.parse_args()

    manifest = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    now = datetime.fromisoformat(arguments.now.replace("Z", "+00:00")) if arguments.now else None
    result = verify_manifest(
        manifest,
        revoked_agent_ids=arguments.revoked_agent,
        now=now,
    )
    print(json.dumps(result.as_dict(), ensure_ascii=True))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
