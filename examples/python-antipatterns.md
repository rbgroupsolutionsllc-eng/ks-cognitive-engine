# Python: Before and After Examples

## Scenario: Background Task Worker with Error Handling

### ❌ Before (Naive LLM Output with Anti-Patterns)
```python
import time

# BAD: mutable default argument, bare except
def process_batch(tasks=[], retries=3):
    results = []
    for t in tasks:
        try:
            res = execute_task(t)
            results.append(res)
        except:
            pass  # Swallows all errors including KeyboardInterrupt!
    return results
```

---

### ✅ After (KS Cognitive Engine Clean Code)
```python
import logging
from typing import Sequence, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class TaskResult:
    task_id: str
    success: bool
    data: Any | None = None
    error_message: str | None = None

def process_batch(
    tasks: Sequence[dict[str, Any]] | None = None, 
    max_retries: int = 3
) -> list[TaskResult]:
    """
    Process a batch of tasks safely with explicit error boundaries.
    """
    if tasks is None:
        return []

    results: list[TaskResult] = []
    for task in tasks:
        task_id = task.get("id", "unknown")
        try:
            output = execute_task(task)
            results.append(TaskResult(task_id=task_id, success=True, data=output))
        except (ValueError, KeyError) as e:
            logger.warning(f"Validation error processing task {task_id}: {e}")
            results.append(TaskResult(task_id=task_id, success=False, error_message=str(e)))
        except Exception as e:
            logger.exception(f"Unexpected operational failure on task {task_id}: {e}")
            results.append(TaskResult(task_id=task_id, success=False, error_message="Internal error"))

    return results
```
