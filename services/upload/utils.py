from typing import Iterable


ALLOWED_CONTENT_TYPES: set[str] = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
}


def is_supported_content_type(content_type: str, allowed: Iterable[str] | None = None) -> bool:
    allowed_types = set(allowed or ALLOWED_CONTENT_TYPES)
    normalized = content_type.strip().lower()
    return normalized in allowed_types
