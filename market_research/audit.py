"""Deterministic identities, local traces, and verifiable artifact checksums."""

import hashlib
import json
import os
from pathlib import Path
import tempfile


def canonical_json(value) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def digest(value) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def atomic_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=".writing-",
            delete=False,
        ) as f:
            temporary = Path(f.name)
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_json(path: Path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def code_digest() -> str:
    root = Path(__file__).parent
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob("*.py"))}
    return digest(files)


def write_audit(out: Path, meta: dict, entries: list[dict]):
    events = []
    for entry in entries:
        a, agent = entry["analysis"], entry["agent"]
        identity = {
            "run_id": meta["run_id"],
            "market_key": f"{a['market']['source']}:{a['market']['market_id']}",
            "analysis_sha256": digest(a),
        }
        for step, output in [
            ("market_analyst", agent["analyst"]),
            ("risk_reviewer", agent["risk_review"]),
            ("research_manager", agent["decision"]),
        ]:
            events.append(
                {**identity, "step": step, "output": output, "output_sha256": digest(output)}
            )
        events.append(
            {
                **identity,
                "step": "validation",
                "mode": agent["mode"],
                "model": agent["model"],
                "error": agent["error"],
                "latency_ms": agent["latency_ms"],
                "usage": agent["usage"],
                "checks": agent.get("validation", {}),
            }
        )
    atomic_text(out / "trace.jsonl", "".join(canonical_json(event) + "\n" for event in events))
    names = ["report.html", "report.json", "report.md", "trace.jsonl"]
    files = {name: hashlib.sha256((out / name).read_bytes()).hexdigest() for name in names}
    write_json(
        out / "manifest.json",
        {
            "schema_version": "1.0",
            "run_id": meta["run_id"],
            "code_sha256": meta["code_sha256"],
            "files": files,
            "note": "Integrity checksum, not a signature or trusted timestamp.",
        },
    )


def verify_manifest(out: Path) -> dict:
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    mismatches = []
    if set(manifest.get("files", {})) != {"report.html", "report.json", "report.md", "trace.jsonl"}:
        raise ValueError("Unexpected manifest file set")
    for name, expected in manifest["files"].items():
        path = out / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            mismatches.append(name)
    return {"valid": not mismatches, "run_id": manifest["run_id"], "mismatches": mismatches}
