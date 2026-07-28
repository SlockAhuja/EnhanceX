import concurrent.futures
from typing import Callable, List, TypeVar, Any

T = TypeVar('T')
R = TypeVar('R')


class TaskScheduler:
    """Multi-threaded task scheduler for frame batch processing."""

    def __init__(self, num_workers: int = 4):
        self.num_workers = max(1, num_workers)
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers)

    def map(self, fn: Callable[[T], R], items: List[T]) -> List[R]:
        """Maps function fn over items in parallel preserving order."""
        return list(self._executor.map(fn, items))

    def submit(self, fn: Callable[..., R], *args: Any, **kwargs: Any) -> concurrent.futures.Future:
        """Submits a single task for asynchronous execution."""
        return self._executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)
