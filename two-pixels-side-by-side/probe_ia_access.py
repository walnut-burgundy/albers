#!/usr/bin/env python3
"""Probe authenticated IA access to the two Interaction of Color editions."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ITEMS = [
    ("interactionofcol00albe", "1971 selected-plates edition"),
    ("interactionofcol0000albe", "1975 revised-plate edition"),
]

FORMAT_SCORE = {
    "text pdf": 0,
    "pdf": 1,
    "djvutxt": 2,
    "djvu text": 2,
    "text": 3,
    "epub": 4,
}
SUFFIX_SCORE = {".pdf": 1, ".txt": 3, ".epub": 4}


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="local ia.ini; never copy it into the repository",
    )
    parser.add_argument("--ia", default="ia", help="path to the ia executable")
    parser.add_argument("--max-files", type=int, default=4)
    return parser.parse_args()


def run(command: list[str], *, stdout=None) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        stdout=stdout if stdout is not None else subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def fmt(file_meta: dict) -> str:
    value = file_meta.get("format", "")
    if isinstance(value, list):
        return "; ".join(str(x) for x in value)
    return str(value)


def score(file_meta: dict) -> tuple[int, str] | None:
    name = str(file_meta.get("name", ""))
    values: list[int] = []
    normalized_format = fmt(file_meta).strip().lower()
    if normalized_format in FORMAT_SCORE:
        values.append(FORMAT_SCORE[normalized_format])
    suffix = Path(name.lower()).suffix
    if suffix in SUFFIX_SCORE:
        values.append(SUFFIX_SCORE[suffix])
    if not values:
        return None
    return min(values), name


def candidates(files: list[dict], limit: int) -> list[dict]:
    ranked = []
    for file_meta in files:
        if not file_meta.get("name"):
            continue
        file_score = score(file_meta)
        if file_score is not None:
            ranked.append((file_score[0], file_score[1], file_meta))
    ranked.sort(key=lambda x: (x[0], x[1]))
    return [file_meta for _, _, file_meta in ranked[:limit]]


def probe(prefix: list[str], identifier: str, filename: str) -> str:
    result = run(
        prefix
        + [
            "download",
            identifier,
            filename,
            "--range",
            "0-0",
            "--stdout",
            "--quiet",
        ],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        return "readable"
    error = result.stderr.lower()
    if "403" in error or "forbidden" in error:
        return "forbidden"
    if "401" in error or "unauthorized" in error:
        return "unauthorized"
    if "404" in error or "not found" in error:
        return "not_found"
    return f"error_{result.returncode}"


def clean(value: object) -> str:
    return str(value).replace("\t", " ").replace("\n", " ")


def main() -> int:
    parsed = args()
    if parsed.max_files < 1:
        raise SystemExit("--max-files must be at least 1")

    prefix = [parsed.ia, "-c", str(parsed.config)]
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(
        [
            "identifier",
            "edition",
            "access_restricted",
            "candidate",
            "format",
            "byte0_probe",
        ]
    )

    had_error = False
    for identifier, edition in ITEMS:
        result = run(prefix + ["metadata", identifier])
        if result.returncode != 0:
            had_error = True
            writer.writerow(
                [identifier, edition, "", "", "", f"metadata_error_{result.returncode}"]
            )
            continue
        try:
            metadata = json.loads(result.stdout)
        except json.JSONDecodeError:
            had_error = True
            writer.writerow([identifier, edition, "", "", "", "metadata_json_error"])
            continue

        restricted = metadata.get("metadata", {}).get("access-restricted-item", "")
        selected = candidates(metadata.get("files", []), parsed.max_files)
        if not selected:
            writer.writerow([identifier, edition, clean(restricted), "", "", "no_candidate"])
            continue

        for file_meta in selected:
            filename = str(file_meta["name"])
            writer.writerow(
                [
                    identifier,
                    edition,
                    clean(restricted),
                    clean(filename),
                    clean(fmt(file_meta)),
                    clean(probe(prefix, identifier, filename)),
                ]
            )

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
