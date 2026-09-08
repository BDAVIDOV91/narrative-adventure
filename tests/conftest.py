"""Shared fixtures.

The build scripts live in data/scripts/ and are not an installed package, so
they are loaded by path rather than imported by module name.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "data" / "scripts"


def load_script(name: str) -> ModuleType:
    """Import a script from data/scripts/ by filename (they use dashes)."""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def validate_levels() -> ModuleType:
    return load_script("validate-levels")


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT
