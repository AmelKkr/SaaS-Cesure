"""Supabase Storage: upload CV, letters, documents."""
import uuid
from typing import Literal

from fastapi import HTTPException, UploadFile
from supabase import create_client, Client

from app.config import get_settings

FileType = Literal["cv", "cover_letter", "document"]

ALLOWED_TYPES: set[str] = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "image/jpeg", "image/png"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def get_supabase_client() -> Client:
    settings = get_settings()
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        raise HTTPException(status_code=503, detail="Supabase storage not configured")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


async def upload_file(
    user_id: uuid.UUID,
    file_type: FileType,
    file: UploadFile,
) -> tuple[str, str, int]:
    """Upload file to Supabase Storage; return (storage_path, file_name, size_bytes)."""
    client = get_supabase_client()
    settings = get_settings()
    bucket = settings.SUPABASE_STORAGE_BUCKET
    content_type = file.content_type or "application/octet-stream"
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type not allowed: {content_type}")
    content = await file.read()
    size = len(content)
    if size > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large (max 10 MB)")
    ext = (file.filename or "file").rsplit(".", 1)[-1] if "." in (file.filename or "") else "bin"
    path = f"{user_id}/{file_type}/{uuid.uuid4()}.{ext}"
    client.storage.from_(bucket).upload(
        path,
        content,
        file_options={"content-type": content_type},
    )
    return path, file.filename or "file", size


def delete_file(storage_path: str) -> None:
    """Delete file from Supabase Storage."""
    client = get_supabase_client()
    settings = get_settings()
    bucket = settings.SUPABASE_STORAGE_BUCKET
    client.storage.from_(bucket).remove([storage_path])


def get_public_url(storage_path: str) -> str:
    """Get signed URL for file (Supabase storage)."""
    client = get_supabase_client()
    settings = get_settings()
    bucket = settings.SUPABASE_STORAGE_BUCKET
    try:
        result = client.storage.from_(bucket).create_signed_url(storage_path, 3600)
        if isinstance(result, dict):
            return result.get("signedUrl") or result.get("path") or result.get("signed_url") or ""
        return ""
    except Exception:
        return ""
