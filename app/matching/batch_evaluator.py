
# import uuid

# from app.matching.candidate_evaluator import evaluate_candidate
# from app.matching.ranking_engine import rank_candidates


# async def evaluate_batch(
#     jd_data: dict,
#     resumes: list[dict],
#     use_llm_responsibility_verification: bool = True
# ) -> dict:

#     candidate_results = []

#     for resume in resumes:
#         candidate_id = str(uuid.uuid4())

#         filename = resume.get("filename", "unknown")
#         resume_text = resume.get("text", "")

#         try:
#             if not resume_text.strip():
#                 raise ValueError("Resume text is empty")

#             evaluation = await evaluate_candidate(
#                 jd_data=jd_data,
#                 resume_text=resume_text,
#                 use_llm_responsibility_verification=
#                     use_llm_responsibility_verification
#             )

#             candidate_result = {
#                 "candidate_id": candidate_id,
#                 "filename": filename,
#                 **evaluation
#             }

#             candidate_results.append(candidate_result)

#         except Exception as exc:
#             candidate_results.append({
#                 "candidate_id": candidate_id,
#                 "filename": filename,
#                 "status": "failed",
#                 "error": str(exc)
#             })

#     # Rank only successfully evaluated candidates.
#     completed_candidates = [
#         candidate
#         for candidate in candidate_results
#         if candidate.get("status") == "completed"
#     ]

#     ranked_candidates = rank_candidates(completed_candidates)

#     # Preserve failed candidates separately in the overall batch.
#     failed_candidates = [
#         candidate
#         for candidate in candidate_results
#         if candidate.get("status") != "completed"
#     ]

#     return {
#         "status": "completed",
#         "total_candidates": len(resumes),
#         "successful_evaluations": len(ranked_candidates),
#         "failed_evaluations": len(failed_candidates),
#         "ranked_candidates": ranked_candidates,
#         "failed_candidates": failed_candidates
#     }








import uuid
from typing import Callable, Any

from app.matching.candidate_evaluator import evaluate_candidate
from app.matching.ranking_engine import rank_candidates


async def evaluate_batch(
    jd_data: dict,
    resumes: list[dict],
    use_llm_responsibility_verification: bool = True,
    on_candidate_update: Callable[[dict], Any] | None = None
) -> dict:

    candidate_results = []

    for index, resume in enumerate(resumes, start=1):
        candidate_id = str(uuid.uuid4())
        filename = resume.get("filename", "unknown")
        resume_text = resume.get("text", "")

        # Notify that the candidate evaluation has started.
        if on_candidate_update:
            on_candidate_update({
                "event": "candidate_started",
                "candidate_id": candidate_id,
                "filename": filename,
                "candidate_number": index,
                "total_candidates": len(resumes)
            })

        try:
            if resume.get("validation_error"):
                raise ValueError(resume["validation_error"])

            if not resume_text.strip():
                raise ValueError("Resume text is empty")

            evaluation = await evaluate_candidate(
                jd_data=jd_data,
                resume_text=resume_text,
                use_llm_responsibility_verification=
                    use_llm_responsibility_verification
            )

            candidate_result = {
                "candidate_id": candidate_id,
                "filename": filename,
                **evaluation
            }

            candidate_results.append(candidate_result)

            # Emit the complete evaluation immediately.
            if on_candidate_update:
                on_candidate_update({
                    "event": "candidate_completed",
                    "candidate": candidate_result
                })

        except Exception as exc:
            failed_candidate = {
                "candidate_id": candidate_id,
                "filename": filename,
                "status": "failed",
                "error": str(exc)
            }

            candidate_results.append(failed_candidate)

            # Emit failure immediately.
            if on_candidate_update:
                on_candidate_update({
                    "event": "candidate_failed",
                    "candidate": failed_candidate
                })

    # Rank successfully evaluated candidates.
    completed_candidates = [
        candidate
        for candidate in candidate_results
        if candidate.get("status") == "completed"
    ]

    ranked_candidates = rank_candidates(completed_candidates)

    failed_candidates = [
        candidate
        for candidate in candidate_results
        if candidate.get("status") != "completed"
    ]

    batch_result = {
        "status": "completed",
        "total_candidates": len(resumes),
        "successful_evaluations": len(ranked_candidates),
        "failed_evaluations": len(failed_candidates),
        "ranked_candidates": ranked_candidates,
        "failed_candidates": failed_candidates
    }

    # Notify that the batch is finished.
    if on_candidate_update:
        on_candidate_update({
            "event": "batch_completed",
            "result": batch_result
        })

    return batch_result
