import hashlib
from pathlib import Path

from fastapi import UploadFile


async def save_file(file: UploadFile) -> str:
    bytes = await file.read()
    suffix = "." + file.content_type.split("/")[-1] if file.content_type else ""
    pt = Path("..") / "static" / "images" / f"{hashlib.md5(bytes).hexdigest()}{suffix}"
    pt.parent.mkdir(parents=True, exist_ok=True)
    with open(pt, "wb") as f:
        f.write(bytes)
    return pt.relative_to("..").as_posix()
