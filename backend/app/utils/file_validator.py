
from fastapi import UploadFile


ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def validate_resume(file: UploadFile) -> None:

    filename = file.filename or ""

    if not filename:
        raise ValueError("Filename is missing.")

    extension = "." + filename.rsplit(".", 1)[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF and DOCX files are supported.")

    file_bytes = await file.read()

    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size exceeds the 5 MB limit.")

    await file.seek(0)
