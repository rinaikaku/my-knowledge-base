#!/usr/bin/env python3
"""Save a PM Hub context JSON packet under contexts/[context_id].json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def safe_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", value).strip()
    return cleaned or "Context-ID-Unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", required=True, help="Path to a JSON file containing the context packet.")
    parser.add_argument("--contexts-dir", default="contexts", help="Directory where context packets are saved.")
    args = parser.parse_args()

    source = Path(args.json_file)
    data = json.loads(source.read_text(encoding="utf-8"))
    context_id = data.get("context_id")
    if not isinstance(context_id, str) or not context_id.strip():
        raise SystemExit("context_id is required in the JSON packet")

    target_dir = Path(args.contexts_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{safe_filename(context_id)}.json"
    target.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(str(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
