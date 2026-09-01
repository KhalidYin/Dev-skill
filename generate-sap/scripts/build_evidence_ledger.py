#!/usr/bin/env python3
"""Validate individual evidence records and deterministically assemble Ledger YAML."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml


MAX_RECORD_CHARS = 3500
MAX_STAGING_CHARS = 2_000_000
STAGING_NAME = ".generation-evidence-ledger.records.jsonl"
OUTPUT_NAME = "generation-evidence-ledger.yaml"
SCHEMA_VERSION = "0.1"

SINGLETON_TYPES = {"document", "search_summary"}
LIST_TYPES = {
    "section_status": ("section_status", "section_id"),
    "content_unit": ("content_units", "content_id"),
    "open_question": ("open_questions", "query_id"),
    "reference": ("references", "reference_id"),
    "consistency_finding": ("consistency_findings", "finding_id"),
}
RECORD_TYPES = SINGLETON_TYPES | LIST_TYPES.keys()


def strip_one_newline(payload: str) -> str:
    if payload.endswith("\r\n"):
        return payload[:-2]
    if payload.endswith(("\n", "\r")):
        return payload[:-1]
    return payload


def resolve_output_root(output_root: Path) -> Path:
    root = output_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("output root is not a directory")
    return root


def parse_record_payload(payload: str) -> dict[str, Any]:
    if len(payload) > MAX_RECORD_CHARS:
        raise ValueError(f"record exceeds {MAX_RECORD_CHARS} characters")
    if not payload:
        raise ValueError("record is empty")
    if "\x00" in payload:
        raise ValueError("record contains a NUL character")
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"record must be valid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}") from exc
    if not isinstance(value, dict):
        raise ValueError("record JSON must be an object")
    return value


def load_envelopes(staging_path: Path) -> list[dict[str, Any]]:
    if not staging_path.exists():
        return []
    if not staging_path.is_file():
        raise ValueError("ledger staging path is not a regular file")

    envelopes: list[dict[str, Any]] = []
    for line_number, line in enumerate(staging_path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            envelope = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger staging line {line_number} is invalid JSON") from exc
        if (
            not isinstance(envelope, dict)
            or envelope.get("record_type") not in RECORD_TYPES
            or not isinstance(envelope.get("value"), dict)
        ):
            raise ValueError(f"ledger staging line {line_number} has an invalid envelope")
        envelopes.append(envelope)
    return envelopes


def validate_new_record(
    envelopes: list[dict[str, Any]], record_type: str, value: dict[str, Any]
) -> None:
    if record_type not in RECORD_TYPES:
        raise ValueError(f"record type is not allowed: {record_type!r}")

    existing = [item for item in envelopes if item["record_type"] == record_type]
    if record_type in SINGLETON_TYPES:
        if existing:
            raise ValueError(f"{record_type} already exists")
        return

    _, id_field = LIST_TYPES[record_type]
    stable_id = value.get(id_field)
    if not isinstance(stable_id, str) or not stable_id:
        raise ValueError(f"{record_type} requires a non-empty {id_field}")
    if any(item["value"].get(id_field) == stable_id for item in existing):
        raise ValueError(f"duplicate {id_field}: {stable_id}")


def append_record(
    output_root: Path, record_type: str, payload: str, *, strip_pipeline_newline: bool = False
) -> Path:
    root = resolve_output_root(output_root)
    output_path = root / OUTPUT_NAME
    if output_path.exists():
        raise ValueError(f"final ledger already exists: {OUTPUT_NAME}")

    if strip_pipeline_newline:
        payload = strip_one_newline(payload)
    value = parse_record_payload(payload)
    staging_path = root / STAGING_NAME
    envelopes = load_envelopes(staging_path)
    validate_new_record(envelopes, record_type, value)

    encoded = json.dumps(
        {"record_type": record_type, "value": value},
        ensure_ascii=False,
        separators=(",", ":"),
    ) + "\n"
    current_size = len(staging_path.read_text(encoding="utf-8")) if staging_path.exists() else 0
    if current_size + len(encoded) > MAX_STAGING_CHARS:
        raise ValueError(f"ledger staging would exceed {MAX_STAGING_CHARS} characters")

    mode = "a" if staging_path.exists() else "x"
    with staging_path.open(mode, encoding="utf-8", newline="") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    return staging_path


def finalize_ledger(output_root: Path) -> Path:
    root = resolve_output_root(output_root)
    output_path = root / OUTPUT_NAME
    if output_path.exists():
        raise ValueError(f"final ledger already exists: {OUTPUT_NAME}")

    staging_path = root / STAGING_NAME
    envelopes = load_envelopes(staging_path)
    if not envelopes:
        raise ValueError("no ledger records have been staged")

    singleton_values: dict[str, dict[str, Any]] = {}
    list_values: dict[str, list[dict[str, Any]]] = {
        output_key: [] for output_key, _ in LIST_TYPES.values()
    }
    for envelope in envelopes:
        record_type = envelope["record_type"]
        value = envelope["value"]
        if record_type in SINGLETON_TYPES:
            if record_type in singleton_values:
                raise ValueError(f"duplicate staged singleton: {record_type}")
            singleton_values[record_type] = value
        else:
            output_key, _ = LIST_TYPES[record_type]
            list_values[output_key].append(value)

    missing = sorted(SINGLETON_TYPES - singleton_values.keys())
    if missing:
        raise ValueError(f"required singleton records are missing: {', '.join(missing)}")

    ledger = {
        "schema_version": SCHEMA_VERSION,
        "document": singleton_values["document"],
        "section_status": list_values["section_status"],
        "content_units": list_values["content_units"],
        "open_questions": list_values["open_questions"],
        "references": list_values["references"],
        "consistency_findings": list_values["consistency_findings"],
        "search_summary": singleton_values["search_summary"],
    }
    serialized = yaml.safe_dump(
        ledger,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100,
    )

    with output_path.open("x", encoding="utf-8", newline="") as stream:
        stream.write(serialized)
        stream.flush()
        os.fsync(stream.fileno())
    staging_path.unlink()
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    add_parser = subparsers.add_parser("add", help="Validate and stage one JSON record from stdin.")
    add_parser.add_argument("--output-root", required=True, type=Path)
    add_parser.add_argument("--record-type", required=True, choices=sorted(RECORD_TYPES))
    add_parser.add_argument(
        "--strip-pipeline-newline",
        action="store_true",
        help="Remove exactly one newline appended by a PowerShell pipeline.",
    )

    finalize_parser = subparsers.add_parser("finalize", help="Build the final YAML Ledger.")
    finalize_parser.add_argument("--output-root", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.action == "add":
            payload = sys.stdin.read(MAX_RECORD_CHARS + 2)
            staging_path = append_record(
                args.output_root,
                args.record_type,
                payload,
                strip_pipeline_newline=args.strip_pipeline_newline,
            )
            print(f"STAGED {args.record_type}: {staging_path.name}")
        else:
            output_path = finalize_ledger(args.output_root)
            print(f"BUILT {output_path.name}")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"LEDGER-ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
