import functools
import logging
from typing import Any, Callable, Dict

logger = logging.getLogger("pipeline.middleware")


def logging_middleware(handler: Callable[[Dict[str, Any]], None]) -> Callable[[Dict[str, Any]], None]:
    @functools.wraps(handler)
    def wrapper(message: Dict[str, Any]) -> None:
        logger.info("Processing message", extra={"message": message})
        handler(message)
        logger.info("Finished processing", extra={"message": message})

    return wrapper


def idempotent_middleware(handled_store: set[str], handler: Callable[[Dict[str, Any]], None]) -> Callable[[Dict[str, Any]], None]:
    @functools.wraps(handler)
    def wrapper(message: Dict[str, Any]) -> None:
        message_id = str(message.get("upload_id"))
        if message_id in handled_store:
            logger.info("Skipping duplicate message", extra={"message_id": message_id})
            return
        handler(message)
        handled_store.add(message_id)

    return wrapper
