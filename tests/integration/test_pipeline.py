from datetime import datetime

from services.common.queue import InMemoryQueue
from services.extract import worker as extract_worker
from services.ocr import worker as ocr_worker
from services.upload.app import main as upload_app


def test_upload_to_extract_pipeline():
    upload_payload = {
        "upload_id": "int-1",
        "filename": "doc.pdf",
        "content_type": "application/pdf",
        "account_id": "acct",
        "object_path": "uploads/acct/doc.pdf",
        "received_at": datetime.utcnow().isoformat() + "Z",
    }

    upload_app.message_bus.publish(upload_payload)

    ocr_input = InMemoryQueue()
    for message in upload_app.message_bus.consume():
        ocr_input.publish(message)

    ocr_worker.main(ocr_input)

    extract_input = InMemoryQueue()
    for message in ocr_worker.message_bus.consume():
        extract_input.publish(message)

    extract_worker.main(extract_input)

    extracted = list(extract_worker.message_bus.consume())
    assert extracted, "Extract worker should emit a message"
    assert extracted[0]["upload_id"] == upload_payload["upload_id"]
