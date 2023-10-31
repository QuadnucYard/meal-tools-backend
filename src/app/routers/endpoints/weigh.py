from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.weigh import Weigh
from app.routers import deps
from app.schemas.weigh import WeighCreate, WeighRead, WeighUpdate

router = APIRouter()


async def dep_get_weigh(
    weigh_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    weigh = await crud.weigh.get(db, weigh_id)
    if not weigh:
        raise HTTPException(404, "Can't find weigh!")
    return weigh


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


@router.put("/{weigh_id}", response_model=WeighRead)
async def update_weigh(
    body: WeighUpdate,
    weigh: Weigh = Depends(dep_get_weigh),
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.weigh.update(db, db_obj=weigh, obj_in=body)


@router.delete("/{weigh_id}", response_model=WeighRead)
async def delete_weigh(
    weigh: Weigh = Depends(dep_get_weigh),
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.weigh.delete(db, weigh)
