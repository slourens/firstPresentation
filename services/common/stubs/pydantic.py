"""Minimal Pydantic-compatible interfaces for tests without dependency installs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


def Field(default: Any | None = None, **_: Any) -> Any:  # pragma: no cover - trivial
    return default


@dataclass
class BaseModel:
    def __init__(self, **data: Any) -> None:  # type: ignore[override]
        for key, value in data.items():
            setattr(self, key, value)

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:  # pragma: no cover - trivial
        return self.__dict__.copy()
