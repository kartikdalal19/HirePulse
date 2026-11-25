
# from fastapi import APIRouter, UploadFile, File
# from typing import List
# import uuid

# from app.parsers.pdf_parser import extract_pdf_text
# from app.parsers.docx_parser import extract_docx_text
# from app.utils.file_validator import validate_resume


# router = APIRouter(prefix="/api/resumes", tags=["Resume Processing"])


# @router.post("/upload")
# async def upload_resumes(
#     files: List[UploadFile] = File(...)
# ):

#     batch_id = str(uuid.uuid4())
#     results = []

#     for file in files:

#         try:
#             await validate_resume(file)
#             file_bytes = await file.read()

#             filename = file.filename or "unknown"

#             if filename.lower().endswith(".pdf"):
#                 extracted_text = extract_pdf_text(file_bytes)

#             else:
#                 extracted_text = extract_docx_text(file_bytes)

#             results.append({
#                 "filename": filename,
#                 "status": "success",
#                 "extracted_text": extracted_text
#             })

#         except Exception as error:

#             results.append({
#                 "filename": file.filename or "unknown",
#                 "status": "failed",
#                 "error": str(error)
#             })

#         finally:
#             await file.close()

#     return {
#         "batch_id": batch_id,
#         "total_files": len(files),
#         "successful": sum(
#             item["status"] == "success" for item in results
#         ),
#         "failed": sum(
#             item["status"] == "failed" for item in results
#         ),
#         "results": results
#     }






from fastapi import APIRouter, UploadFile, File
from typing import List
import uuid

from app.parsers.pdf_parser import extract_pdf_text
from app.parsers.docx_parser import extract_docx_text
from app.utils.file_validator import validate_resume

router = APIRouter(prefix="/api/resumes", tags=["Resume Processing"])


@router.post("/upload")
async def upload_resumes(
    files: List[UploadFile] = File(
        ...,
        description="Select multiple PDF or DOCX resumes"
    )
):
    batch_id = str(uuid.uuid4())
    results = []

    for file in files:
        try:
            await validate_resume(file)
            file_bytes = await file.read()

            filename = file.filename or "unknown"

            if filename.lower().endswith(".pdf"):
                extracted_text = extract_pdf_text(file_bytes)
            else:
                extracted_text = extract_docx_text(file_bytes)

            results.append({
                "filename": filename,
                "status": "success",
                "extracted_text": extracted_text
            })

        except Exception as error:
            results.append({
                "filename": file.filename or "unknown",
                "status": "failed",
                "error": str(error)
            })

        finally:
            await file.close()

    return {
        "batch_id": batch_id,
        "total_files": len(files),
        "successful": sum(r["status"] == "success" for r in results),
        "failed": sum(r["status"] == "failed" for r in results),
        "results": results
    }
