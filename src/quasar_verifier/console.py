"""Local read-only console for Trust Layer evidence."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .demo import run_demo


WEB_ROOT = Path(__file__).resolve().parents[2] / "web"
DEFAULT_EVENTS_PATH = Path("docs/examples/demo-evidence.json")


def load_events(events_path: Path) -> list[dict[str, Any]]:
    if events_path.exists():
        return json.loads(events_path.read_text(encoding="utf-8"))
    return run_demo(events_path)


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = {"allow": 0, "review": 0, "deny": 0}
    for event in events:
        decision = event.get("decision")
        if decision in decisions:
            decisions[decision] += 1
    agents = sorted({event.get("agent_id", "unknown") for event in events})
    domain_aliases = sorted(
        {event["domain_alias"] for event in events if event.get("domain_alias")}
    )
    return {
        "total_events": len(events),
        "decisions": decisions,
        "agents": agents,
        "domain_aliases": domain_aliases,
        "last_timestamp": events[-1].get("timestamp") if events else None,
    }


class ConsoleHandler(BaseHTTPRequestHandler):
    server: "ConsoleServer"

    def do_GET(self) -> None:
        route = urlsplit(self.path).path
        if route == "/":
            self._send_file(WEB_ROOT / "console.html", "text/html; charset=utf-8")
        elif route == "/api/events":
            self._send_json(self.server.events)
        elif route == "/api/summary":
            self._send_json(summarize_events(self.server.events))
        else:
            self.send_error(404, "Not found")

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[console] {format % args}")

    def _send_file(self, path: Path, content_type: str) -> None:
        try:
            content = path.read_bytes()
        except FileNotFoundError:
            self.send_error(404, "Console asset not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload: Any) -> None:
        content = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


class ConsoleServer(ThreadingHTTPServer):
    events: list[dict[str, Any]]


def serve(events_path: Path, host: str, port: int) -> None:
    events = load_events(events_path)
    server = ConsoleServer((host, port), ConsoleHandler)
    server.events = events
    print(f"QuasarChain console: http://{host}:{port}")
    print(f"Loaded events: {len(events)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nConsole stopped")
    finally:
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the local QuasarChain evidence console")
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS_PATH)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    arguments = parser.parse_args()
    serve(arguments.events, arguments.host, arguments.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
