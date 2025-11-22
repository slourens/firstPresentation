import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from contracts.validator import validate_message
from services.common.middleware import idempotent_middleware, logging_middleware
from services.common.queue import InMemoryQueue, consume_queue

logger = logging.getLogger("extract.worker")
message_bus = InMemoryQueue()
processed: set[str] = set()


def extract_entities(ocr_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    logger.info("Extracting entities", extra={"upload_id": ocr_payload["upload_id"]})
    return [
        {"type": "date", "value": "2024-01-01", "confidence": 0.9},
        {"type": "org", "value": "Example Corp", "confidence": 0.85},
    ]


def handle_ocr_completed(message: Dict[str, Any]) -> None:
    entities = extract_entities(message)
    payload = {
        "upload_id": message["upload_id"],
        "entities": entities,
        "summary": "Stub summary",
        "confidence": 0.88,
        "completed_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    validate_message("extract.completed", payload)
    message_bus.publish(payload)


def main(queue: InMemoryQueue, consumer=consume_queue) -> None:
    handler = logging_middleware(idempotent_middleware(processed, handle_ocr_completed))
    consumer(queue, handler)


if __name__ == "__main__":
    example_queue = InMemoryQueue()
    example_queue.publish({"upload_id": "demo", "text_path": "ocr/demo.json"})
    main(example_queue)
