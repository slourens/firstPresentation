import logging
from datetime import datetime, timezone
from typing import Any, Dict

from contracts.validator import validate_message
from services.common.middleware import idempotent_middleware, logging_middleware
from services.common.queue import InMemoryQueue, consume_queue

logger = logging.getLogger("ocr.worker")
message_bus = InMemoryQueue()
processed: set[str] = set()


def perform_ocr(message: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Performing OCR", extra={"upload_id": message["upload_id"]})
    return {
        "upload_id": message["upload_id"],
        "text_path": f"ocr/{message['upload_id']}.json",
        "engine": "stub-ocr",
        "language": "en",
        "completed_at": datetime.now(tz=timezone.utc).isoformat(),
    }


def handle_upload_received(message: Dict[str, Any]) -> None:
    ocr_payload = perform_ocr(message)
    validate_message("ocr.completed", ocr_payload)
    message_bus.publish(ocr_payload)


def main(queue: InMemoryQueue, consumer=consume_queue) -> None:
    handler = logging_middleware(idempotent_middleware(processed, handle_upload_received))
    consumer(queue, handler)


if __name__ == "__main__":
    example_queue = InMemoryQueue()
    example_queue.publish({"upload_id": "demo", "object_path": "uploads/demo.pdf"})
    main(example_queue)
