from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.routers import deps
from app.schemas.weigh import WeighCreate, WeighRead

router = APIRouter()


@router.get("/", response_model=list[WeighRead])
async def get_weighs(
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.weigh.get_many(db, limit=10000)


@router.post("/", response_model=WeighRead)
async def add_weigh(
    body: WeighCreate,
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.weigh.create(db, body)
