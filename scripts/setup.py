"""Create isolated MCP and market-data environments without dependency conflicts."""

from __future__ import annotations

import subprocess
import sys
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = (
    "git+https://github.com/wcheng2001-del/TradingAgents-Astock-auto.git"
    "@001c8463302707faf6cb8843c864b08454836060"
)


def env_python(folder: Path) -> Path:
    windows = folder / "Scripts" / "python.exe"
    return windows if windows.exists() else folder / "bin" / "python"


def run(python: Path, *args: str) -> None:
    subprocess.run([str(python), *args], cwd=ROOT, check=True)


def ensure_env(folder: Path) -> Path:
    if not env_python(folder).exists():
        venv.EnvBuilder(with_pip=True).create(folder)
    return env_python(folder)


def main() -> None:
    app_python = ensure_env(ROOT / ".venv")
    run(app_python, "-m", "pip", "install", "--disable-pip-version-check", "-e", ".")

    provider_python = ensure_env(ROOT / ".provider-venv")
    run(
        provider_python,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "pandas>=2.3",
        "requests>=2.32.4",
        "python-dateutil>=2.9",
        "parsel>=1.10",
        "mootdx==0.11.7",
        "stockstats>=0.6.5",
    )
    run(
        provider_python,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-deps",
        UPSTREAM,
    )
    print("Serenity Data Bridge setup complete.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
