
import asyncio
import json

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from app.matching.batch_evaluator import evaluate_batch
from app.parsers.pdf_parser import extract_pdf_text
from app.parsers.docx_parser import extract_docx_text
from app.utils.file_validator import validate_resume


router = APIRouter(prefix="/api/batch", tags=["Batch Evaluation"])


def format_sse(event_data: dict) -> str:
    return f"data: {json.dumps(event_data)}\n\n"


@router.post("/evaluate")
async def evaluate_resumes(
    jd_data: str = Form(...),
    files: list[UploadFile] = File(...)
):

    # Parse JD JSON.
    try:
        parsed_jd = json.loads(jd_data)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid JD JSON format."
        }

    # Validate and parse resumes.
    resumes = []

    for file in files:
        filename = file.filename or "unknown"

        try:
            await validate_resume(file)
            file_bytes = await file.read()

            extension = "." + filename.rsplit(".", 1)[-1].lower()

            if extension == ".pdf":
                resume_text = extract_pdf_text(file_bytes)
            elif extension == ".docx":
                resume_text = extract_docx_text(file_bytes)
            else:
                raise ValueError("Unsupported file format.")

            resumes.append({
                "filename": filename,
                "text": resume_text
            })

        except Exception as exc:
            resumes.append({
                "filename": filename,
                "text": "",
                "validation_error": str(exc)
            })

    async def event_stream():

        queue = asyncio.Queue()

        def on_update(update: dict):
            queue.put_nowait(update)

        evaluation_task = asyncio.create_task(
            evaluate_batch(
                jd_data=parsed_jd,
                resumes=resumes,
                on_candidate_update=on_update
            )
        )

        try:
            while True:
                update = await queue.get()

                yield format_sse(update)

                if update.get("event") == "batch_completed":
                    break

            await evaluation_task

        except asyncio.CancelledError:
            evaluation_task.cancel()
            raise

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
