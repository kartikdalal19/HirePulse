
import re


def normalize_text(text: str) -> str:
    """Normalize text for keyword searching."""
    return " ".join(text.lower().split())


def find_skill_keyword(
    skill: str,
    resume_text: str
) -> dict:
    """
    Search for a skill as a complete phrase
    in the extracted resume text.
    """

    normalized_skill = normalize_text(skill)
    normalized_resume = normalize_text(resume_text)

    # Escape special regex characters and enforce word boundaries.
    pattern = r"(?<!\w)" + re.escape(normalized_skill) + r"(?!\w)"

    match = re.search(pattern, normalized_resume)

    if match:
        start = max(0, match.start() - 100)
        end = min(len(normalized_resume), match.end() + 100)

        return {
            "skill": skill,
            "found": True,
            "method": "keyword",
            "evidence": normalized_resume[start:end]
        }

    return {
        "skill": skill,
        "found": False,
        "method": None,
        "evidence": None
    }


def match_skills_by_keyword(
    jd_skills: list[str],
    resume_text: str
) -> dict:
    """Search all JD skills in the resume."""

    results = [
        find_skill_keyword(skill, resume_text)
        for skill in jd_skills
    ]

    matched = [
        item for item in results if item["found"]
    ]

    not_found = [
        item for item in results if not item["found"]
    ]

    return {
        "results": results,
        "matched_skills": matched,
        "not_found_skills": not_found
    }
