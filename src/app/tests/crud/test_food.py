import time
from typing import Any, AsyncGenerator

import pytest
from app import crud
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_foods_time(db: AsyncGenerator[AsyncSession, Any]) -> None:
    db_ = await anext(db)
    t1 = time.time()
    for _ in range(100):
        await crud.food.get_with_weight(db_)
    t2 = time.time()
    print("Duration:", t2 - t1)
