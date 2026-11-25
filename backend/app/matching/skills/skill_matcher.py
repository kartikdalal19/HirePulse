# from app.matching.skills.keyword_matcher import match_skills_by_keyword
# from app.matching.skills.semantic_skill_matcher import match_skills_semantically


# async def match_skills(
#     jd_skills: list[str],
#     resume_text: str
# ) -> dict:

#     # Stage 1: Exact keyword matching
#     keyword_result = match_skills_by_keyword(
#         jd_skills,
#         resume_text
#     )

#     keyword_matches = keyword_result["matched_skills"]
#     not_found_by_keyword = keyword_result["not_found_skills"]

#     # Stage 2: Semantic matching only for keyword-unmatched skills
#     semantic_result = await match_skills_semantically(
#     not_found_by_keyword,
#     resume_text
#     )

#     semantic_matches = semantic_result["matched_skills"]
#     semantic_missing = semantic_result["missing_skills"]

#     # Stage 3: Combine results
#     matched_skills = keyword_matches + semantic_matches

#     missing_skills = semantic_missing

#     return {
#         "total_skills": len(jd_skills),
#         "matched_count": len(matched_skills),
#         "missing_count": len(missing_skills),
#         "matched_skills": matched_skills,
#         "missing_skills": missing_skills,
#         "keyword_matches": keyword_matches,
#         "semantic_matches": semantic_matches
#     }









from app.matching.skills.keyword_matcher import match_skills_by_keyword
from app.matching.skills.semantic_skill_matcher import match_skills_semantically


async def match_skills(
    jd_skills: list[str],
    resume_text: str
) -> dict:

    # Stage 1: Keyword matching
    keyword_result = match_skills_by_keyword(
        jd_skills,
        resume_text
    )

    keyword_matches = keyword_result["matched_skills"]
    not_found_by_keyword = keyword_result["not_found_skills"]

    # Stage 2: Semantic matching for unmatched skills
    semantic_result = await match_skills_semantically(
        not_found_by_keyword,
        resume_text
    )

    semantic_matches = semantic_result["semantic_matches"]
    semantic_missing = semantic_result["missing_skills"]

    # Stage 3: Combine results
    matched_skills = keyword_matches + semantic_matches

    return {
        "total_skills": len(jd_skills),
        "matched_count": len(matched_skills),
        "missing_count": len(semantic_missing),
        "matched_skills": matched_skills,
        "missing_skills": semantic_missing,
        "keyword_matches": keyword_matches,
        "semantic_matches": semantic_matches
    }
