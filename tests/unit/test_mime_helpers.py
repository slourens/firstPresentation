from services.upload.utils import ALLOWED_CONTENT_TYPES, is_supported_content_type


def test_supported_content_type_defaults():
    assert is_supported_content_type("application/pdf")
    assert not is_supported_content_type("application/zip")


def test_supported_content_type_override():
    assert is_supported_content_type("custom/type", allowed=["custom/type"])
    assert "application/pdf" in ALLOWED_CONTENT_TYPES
