
from app.matching.skills.skill_matcher import match_skills


async def evaluate_preferred_skills(
    preferred_skills: list[str],
    resume_text: str
) -> dict:

    if not preferred_skills:
        return {
            "total_preferred_skills": 0,
            "matched_count": 0,
            "missing_count": 0,
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": []
        }

    # Perform keyword + semantic matching
    result = await match_skills(
        preferred_skills,
        resume_text
    )

    total = result["total_skills"]
    matched = result["matched_count"]

    match_percentage = (matched / total) * 100

    return {
        "total_preferred_skills": total,
        "matched_count": matched,
        "missing_count": result["missing_count"],
        "match_percentage": round(match_percentage, 2),
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "keyword_matches": result["keyword_matches"],
        "semantic_matches": result["semantic_matches"]
    }
