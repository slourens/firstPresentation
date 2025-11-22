"""Minimal FastAPI stand-in for offline testing."""
from __future__ import annotations

from typing import Any, Callable, Dict


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str | Dict[str, Any] | None = None) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class FastAPI:
    def __init__(self, title: str | None = None) -> None:  # pragma: no cover - trivial
        self.title = title

    def get(self, path: str, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self._wrap_route

    def post(self, path: str, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self._wrap_route

    @staticmethod
    def _wrap_route(func: Callable[..., Any]) -> Callable[..., Any]:
        return func
