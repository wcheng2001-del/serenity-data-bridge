"""Launch the MCP server from the repository-local virtual environment."""

from __future__ import annotations

import subprocess
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / ".venv" / "Scripts" / "python.exe",
        root / ".venv" / "bin" / "python",
    ]
    python = next((candidate for candidate in candidates if candidate.is_file()), None)
    if python is None:
        raise SystemExit(
            "Serenity Data Bridge is not installed. From the plugin root run: "
            "python -m venv .venv, then install with the .venv Python: "
            "python -m pip install -e ."
        )
    completed = subprocess.run(
        [str(python), "-m", "serenity_data_bridge.server"],
        check=False,
    )
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
