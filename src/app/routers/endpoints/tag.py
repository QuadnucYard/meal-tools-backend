from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.routers import deps
from app.schemas.tag import TagCreate, TagRead, TagReadWithFoods, TagUpdate

router = APIRouter()


@router.get("/", response_model=list[TagRead])
async def get_tags(
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.tag.get_many(db, limit=1000)


@router.get("/{tag_id}", response_model=TagReadWithFoods)
async def get_tag(
    tag_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    tag = await crud.tag.get(db, tag_id)
    if not tag:
        raise HTTPException(404, "Tag not found!")
    return await TagReadWithFoods.model_validate_async(tag)


@router.post("/", response_model=TagRead)
async def add_tag(
    tag_in: TagCreate,
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.tag.create(db, tag_in)


@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    db: AsyncSession = Depends(deps.get_db),
):
    tag = await crud.tag.get(db, tag_id)
    if not tag:
        raise HTTPException(404, "Tag not found!")
    return await crud.tag.update(db, db_obj=tag, obj_in=tag_in)


@router.delete("/{tag_id}", response_model=TagRead)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.tag.remove(db, id=tag_id)
