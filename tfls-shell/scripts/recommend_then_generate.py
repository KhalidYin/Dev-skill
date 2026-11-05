from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _bootstrap_repo_imports() -> None:
    current_path = Path(__file__).resolve()
    repo_root = next(
        (
            parent
            for parent in current_path.parents
            if (parent / "pyproject.toml").exists() and (parent / "src" / "tflshell").exists()
        ),
        None,
    )
    package_root = current_path.parents[1]
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))
    if repo_root is not None:
        src_path = repo_root / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
    else:
        from importlib.util import find_spec

        if find_spec("tflshell") is None:
            raise RuntimeError(
                "缺少 tflshell Product 依赖；请按 Skill references/integration.md 安装上游 Product。"
            )

_bootstrap_repo_imports()

from delivery import cli_main


if __name__ == "__main__":
    sys.exit(cli_main(full=False))
