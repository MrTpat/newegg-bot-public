from typing import Optional
from typing import Any
import json

def universal_function_limiter(func, limit: int, options: dict, repeatWhile: Any) -> Optional[Any]:
    tries = 0
    while tries < limit:
        val = func(**options)
        if val != repeatWhile:
            return val
        tries += 1
    return None

def gather_cookies(file_name: str) -> Optional[dict]:
    f = open(f'cookies/{file_name}')
    try:
        return json.load(f)
    except Exception as e:
        from . import logger
        logger.Logger().handle_err(e)

def ensure_dir_exists(dir_name: str) -> None:
        import os
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

