import pytest

from contracts.validator import SchemaRegistry, validate_message


def test_validate_message_success():
    payload = {
        "upload_id": "abc",
        "filename": "file.pdf",
        "content_type": "application/pdf",
        "account_id": "acct1",
        "object_path": "uploads/acct1/file.pdf",
        "received_at": "2024-01-01T00:00:00Z",
    }
    validate_message("upload.received", payload)


def test_validate_message_failure():
    payload = {"upload_id": "abc"}
    registry = SchemaRegistry()
    with pytest.raises(Exception):
        registry.validate("upload.received", payload)
