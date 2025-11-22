"""Compatibility shims for environments without optional deps."""
from __future__ import annotations

import importlib.util
from typing import Any, Callable


def _load_fastapi() -> tuple[type[Any], type[Exception], Callable[[str], Callable]]:
    if importlib.util.find_spec("fastapi") is not None:
        from fastapi import FastAPI, HTTPException

        return FastAPI, HTTPException
    from services.common.stubs.fastapi import FastAPI, HTTPException

    return FastAPI, HTTPException


def _load_pydantic() -> tuple[type[Any], Callable[..., Any]]:
    if importlib.util.find_spec("pydantic") is not None:
        from pydantic import BaseModel, Field

        return BaseModel, Field
    from services.common.stubs.pydantic import BaseModel, Field

    return BaseModel, Field


FastAPI, HTTPException = _load_fastapi()
BaseModel, Field = _load_pydantic()
