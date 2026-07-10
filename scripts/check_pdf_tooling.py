#!/usr/bin/env python3

from __future__ import annotations

import os
import shlex
import shutil

def main() -> int:
    missing: list[str] = []

    command = os.environ.get("ANTHROPIC_PDF_SKILL_COMMAND", "").strip()
    if command:
        command_head = shlex.split(command)[0]
        resolved = shutil.which(command_head) if command_head and "/" not in command_head else command_head
        if resolved:
            print(f"pdf skill bridge ok: {command}")
        else:
            print(f"pdf skill bridge missing: {command_head}")
            missing.append("ANTHROPIC_PDF_SKILL_COMMAND")
    else:
        print("pdf skill bridge missing: ANTHROPIC_PDF_SKILL_COMMAND")
        missing.append("ANTHROPIC_PDF_SKILL_COMMAND")

    optional_binaries = ["pdftoppm", "pdfinfo"]
    for binary in optional_binaries:
        path = shutil.which(binary)
        if path:
            print(f"optional binary ok: {binary} -> {path}")
        else:
            print(f"optional binary missing: {binary}")

    if missing:
        print("pdf skill bridge incomplete")
        return 1

    print("pdf skill bridge ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
