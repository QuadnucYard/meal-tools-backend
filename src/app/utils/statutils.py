from typing import Any, Callable, Coroutine, Sequence

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import DateCount


async def counter_helper(
    db: AsyncSession,
    *counters: tuple[Callable[[AsyncSession], Coroutine[Any, Any, Sequence[DateCount]]], str]
):
    res = (
        pd.concat(
            [
                pd.DataFrame(await cnt[0](db), columns=["date", "count"]).set_index("date").rename(columns={"count": cnt[1]})
                for cnt in counters
            ],
            axis=1,
            join="outer",
        )
        .sort_index()
        .fillna(0)
    )
    res.insert(0, "date", res.index)
    return res.dropna().to_dict("records")
