from fastapi import APIRouter, File, UploadFile

from app.utils.futils import save_file

router = APIRouter()


@router.post("/image", response_model=str)
async def upload_image(image: UploadFile):
    return await save_file(image)


@router.post("/images", response_model=list[str])
async def upload_images(images: list[UploadFile] = File(alias="images[]")):
    return [await save_file(image) for image in images]
