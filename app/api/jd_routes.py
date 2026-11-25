import traceback
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import ValidationError

from app.parsers.jd_parser import extract_jd_file
from app.services.jd_processor import process_job_description
from app.schemas import JobDescriptionData, JobDescriptionResponse
from app.storage.memory_store import (
    save_job_description,
    get_job_description,
    get_all_job_descriptions
)


router = APIRouter(prefix="/api/jd", tags=["Job Descriptions"])


@router.post("/analyze", response_model=JobDescriptionResponse)
async def analyze_job_description(
    jd_text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None)
):

    # Accept either pasted text or an uploaded document.
    if file is not None and jd_text and jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Provide pasted text OR a file, not both."
        )

    if file is not None:

        filename = file.filename or ""

        if not filename.lower().endswith((".pdf", ".docx")):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported."
            )

        file_bytes = await file.read()

        if len(file_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File size cannot exceed 5 MB."
            )

        try:
            jd_text = extract_jd_file(filename, file_bytes)
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"Document extraction failed: {error}"
            )

    elif jd_text:
        jd_text = jd_text.strip()

    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide a job description or upload a file."
        )

    if len(jd_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short to analyze."
        )

    try:
        extracted = await process_job_description(jd_text)
        validated_data = JobDescriptionData.model_validate(extracted)

    except (ValueError, ValidationError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not validate AI extraction: {error}"
        )
    # except Exception:
    #     raise HTTPException(
    #         status_code=502,
    #         detail="Job description analysis failed. Check the AI API configuration."
    #     )

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=502,
            detail="Job description analysis failed. Check the AI API configuration."
        )
    
    job_id = str(uuid4())

    record = {
        "job_id": job_id,
        "status": "analyzed",
        "original_text": jd_text,
        "extracted_requirements": validated_data.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    save_job_description(job_id, record)

    return record


@router.get("/{job_id}")
async def get_jd(job_id: str):

    record = get_job_description(job_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Job description not found."
        )

    return record


@router.get("/")
async def get_all_jds():

    return get_all_job_descriptions()
