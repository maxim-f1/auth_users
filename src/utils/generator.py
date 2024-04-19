from typing import Iterable

import asyncio


async def sleep_generator[T](iterable: Iterable[T], sleep_sec: int | float = 0) -> T:
    for item in iterable:
        yield item
        await asyncio.sleep(sleep_sec)