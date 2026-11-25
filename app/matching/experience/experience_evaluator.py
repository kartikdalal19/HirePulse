
from app.matching.experience.semantic_experience_search import (
    search_experience_chunks
)

from app.matching.experience.experience_extractor import (
    extract_employment_records
)

from app.matching.experience.relevant_experience_evaluator import (
    evaluate_relevant_experience
)


async def evaluate_experience(
    jd_data: dict,
    resume_text: str
) -> dict:
    """
    Execute the complete experience evaluation pipeline.
    """

    # Step 1: Retrieve relevant resume chunks.
    search_result = await search_experience_chunks(resume_text)

    contexts = search_result["contexts"]

    if not contexts:
        return {
            "status": "completed",
            "message": "No relevant resume content was found.",
            "retrieved_chunks": 0,
            "employment_records": [],
            "total_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            },
            "relevant_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            }
        }

    # Step 2: Extract employment records using Groq.
    extraction_result = await extract_employment_records(contexts)

    employment_records = extraction_result["employment_records"]

    if not employment_records:
        return {
            "status": "completed",
            "message": "No employment records could be identified.",
            "retrieved_chunks": len(contexts),
            "employment_records": [],
            "total_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            },
            "relevant_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            }
        }

    # Step 3 and 4: Calculate total and weighted relevant experience.
    evaluation_result = await evaluate_relevant_experience(
        jd_data,
        employment_records
    )

    return {
        "status": "completed",
        "retrieved_chunks": len(contexts),
        "total_experience": evaluation_result["total_experience"],
        "relevant_experience": evaluation_result["relevant_experience"],
        "total_employment_records": extraction_result["total_records"],
        "evaluated_employment_records": evaluation_result[
            "evaluated_employment_records"
        ],
        "relevance_breakdown": evaluation_result["relevance_breakdown"],
        "employment_records": evaluation_result["relevant_records"]
    }
