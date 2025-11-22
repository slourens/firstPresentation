from collections import deque
from typing import Any, Callable, Deque, Dict, Iterable


class InMemoryQueue:
    def __init__(self) -> None:
        self._queue: Deque[Dict[str, Any]] = deque()

    def publish(self, message: Dict[str, Any]) -> None:
        self._queue.append(message)

    def consume(self) -> Iterable[Dict[str, Any]]:
        while self._queue:
            yield self._queue.popleft()

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._queue)


def consume_queue(queue: InMemoryQueue, handler: Callable[[Dict[str, Any]], None]) -> None:
    for message in list(queue.consume()):
        handler(message)
