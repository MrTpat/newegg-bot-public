from typing import Optional
from typing import Any

def universal_function_limiter(func, limit: int, options: dict, repeatWhile: Any) -> Optional[Any]:
    tries = 0
    while tries < limit:
        val = func(**options)
        if val != repeatWhile:
            return val
        tries += 1
    return None
