"""Storage routes: upload, list, delete files."""
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import get_current_user
from app.core.storage_service import upload_file as do_upload, delete_file as do_delete, get_public_url
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.storage_file import StorageFile

router = APIRouter()

ALLOWED_FILE_TYPES: list[str] = ["cv", "cover_letter", "document"]


@router.post("/upload")
async def upload(
    file_type: str = Form(..., description="One of: cv, cover_letter, document"),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a file (cv, cover_letter, document)."""
    if file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"file_type must be one of {ALLOWED_FILE_TYPES}")
    storage_path, file_name, size_bytes = await do_upload(current_user.id, file_type, file)
    record = StorageFile(
        user_id=current_user.id,
        file_type=file_type,
        file_name=file_name,
        storage_path=storage_path,
        mime_type=file.content_type,
        size_bytes=size_bytes,
    )
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return {
        "id": str(record.id),
        "file_type": record.file_type,
        "file_name": record.file_name,
        "storage_path": record.storage_path,
        "size_bytes": record.size_bytes,
        "created_at": record.created_at.isoformat(),
    }


@router.get("/files")
async def list_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List current user's files."""
    result = await db.execute(
        select(StorageFile).where(StorageFile.user_id == current_user.id).order_by(StorageFile.created_at.desc())
    )
    files = result.scalars().all()
    return [
        {
            "id": str(f.id),
            "file_type": f.file_type,
            "file_name": f.file_name,
            "storage_path": f.storage_path,
            "size_bytes": f.size_bytes,
            "created_at": f.created_at.isoformat(),
            "url": get_public_url(f.storage_path),
        }
        for f in files
    ]


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a file (only own)."""
    result = await db.execute(
        select(StorageFile).where(StorageFile.id == file_id).where(StorageFile.user_id == current_user.id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    do_delete(record.storage_path)
    await db.delete(record)
    await db.flush()
    return {"message": "File deleted"}
