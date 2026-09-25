"""Isolated subprocess adapter for the pinned TradingAgents data layer."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

SOURCE_REPOSITORY = "https://github.com/wcheng2001-del/TradingAgents-Astock-auto"
SOURCE_COMMIT = "001c8463302707faf6cb8843c864b08454836060"


class TradingAgentsProvider:
    """Call upstream functions in a separate environment to isolate dependencies."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[2]

    def _python(self) -> Path:
        override = os.environ.get("SERENITY_PROVIDER_PYTHON")
        if override:
            path = Path(override).expanduser().resolve()
            if path.is_file():
                return path
            raise RuntimeError("SERENITY_PROVIDER_PYTHON does not point to a file")

        candidates = [
            self.root / ".provider-venv" / "Scripts" / "python.exe",
            self.root / ".provider-venv" / "bin" / "python",
        ]
        python = next((candidate for candidate in candidates if candidate.is_file()), None)
        if python is None:
            raise RuntimeError(
                "The isolated data provider is not installed. "
                "Run `python scripts/setup.py` from serenity-data-bridge."
            )
        return python

    def call(self, function_name: str, *args: Any, **kwargs: Any) -> str:
        worker = self.root / "scripts" / "provider_worker.py"
        request = json.dumps(
            {"function": function_name, "args": args, "kwargs": kwargs},
            ensure_ascii=False,
        )
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        completed = subprocess.run(
            [str(self._python()), str(worker)],
            input=request,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            timeout=180,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or "provider worker failed"
            raise RuntimeError(detail[-2000:])
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("provider worker returned invalid JSON") from exc
        if not response.get("ok"):
            raise RuntimeError(str(response.get("error", "provider call failed")))
        result = response.get("result", "")
        return result if isinstance(result, str) else str(result)
