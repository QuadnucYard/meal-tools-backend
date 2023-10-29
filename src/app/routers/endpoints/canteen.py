from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.routers import deps
from app.schemas.canteen import CanteenRead

router = APIRouter()


@router.get("/", response_model=list[CanteenRead])
async def get_canteens(
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.canteen.get_many(db)
