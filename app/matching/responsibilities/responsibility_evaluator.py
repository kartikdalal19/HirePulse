
# from app.matching.responsibilities.semantic_responsibility_matcher import (
#     match_responsibilities_semantically
# )
# from app.matching.responsibilities.llm_responsibility_verifier import (
#     verify_responsibilities_with_llm
# )


# async def evaluate_responsibilities(
#     responsibilities: list[str],
#     resume_text: str,
#     use_llm_verification: bool = False
# ) -> dict:

#     semantic_result = await match_responsibilities_semantically(
#         responsibilities,
#         resume_text
#     )

#     if use_llm_verification:
#         result = await verify_responsibilities_with_llm(
#             semantic_result
#         )

#         for item in result["results"]:
#             item["verification_method"] = "llm" if item["found"] else "none"

#     else:
#         result = {
#             "total_responsibilities": semantic_result["total_responsibilities"],
#             "results": [
#                 {
#                     **item,
#                     "considered": item["found"],
#                     "verification_reason": (
#                         "Relevant evidence retrieved through semantic search."
#                         if item["found"]
#                         else "No evidence passed the semantic retrieval threshold."
#                     ),
#                     "verification_method": (
#                         "semantic" if item["found"] else "none"
#                     )
#                 }
#                 for item in semantic_result["results"]
#             ]
#         }

#     total = result["total_responsibilities"]
#     considered = sum(
#         item["considered"] for item in result["results"]
#     )

#     coverage = (
#         (considered / total) * 100
#         if total > 0 else 0.0
#     )

#     result["considered_count"] = considered
#     result["not_considered_count"] = total - considered
#     result["coverage_percentage"] = round(coverage, 2)
#     result["verification_enabled"] = use_llm_verification
#     result.pop("verified_count", None)
#     return result

from app.matching.responsibilities.semantic_responsibility_matcher import (
    match_responsibilities_semantically
)
from app.matching.responsibilities.llm_responsibility_verifier import (
    verify_responsibilities_with_llm
)


async def evaluate_responsibilities(
    responsibilities: list[str],
    resume_text: str,
    use_llm_verification: bool = False
) -> dict:

    semantic_result = await match_responsibilities_semantically(
        responsibilities,
        resume_text
    )

    if use_llm_verification:

        result = await verify_responsibilities_with_llm(
            semantic_result
        )

        for item in result["results"]:
            item["verification_method"] = (
                "llm" if item["found"] else "none"
            )

    else:

        result = {
            "total_responsibilities": semantic_result["total_responsibilities"],
            "results": [
                {
                    **item,
                    "responsibility_score": (
                        1.0 if item["found"] else 0.0
                    ),
                    "sub_actions": [],
                    "considered": item["found"],
                    "verification_reason": (
                        "Relevant evidence retrieved through semantic search."
                        if item["found"]
                        else "No evidence passed the semantic retrieval threshold."
                    ),
                    "verification_method": (
                        "semantic" if item["found"] else "none"
                    )
                }
                for item in semantic_result["results"]
            ]
        }

    total = result["total_responsibilities"]

    # Calculate coverage using decimal responsibility scores.
    total_score = sum(
        item.get("responsibility_score", 0.0)
        for item in result["results"]
    )

    coverage = (
        (total_score / total) * 100
        if total > 0 else 0.0
    )

    considered = sum(
        item["considered"] for item in result["results"]
    )

    result["considered_count"] = considered
    result["not_considered_count"] = total - considered
    result["coverage_percentage"] = round(coverage, 2)
    result["verification_enabled"] = use_llm_verification

    result.pop("verified_count", None)

    return result
