import json
import re

from app.services.groq_service import groq_service


async def evaluate_profile_criterion(
    criterion_name: str,
    jd_requirements: list[str],
    extracted_items: list[str]
) -> dict:
    """
    Evaluate a profile-based criterion such as education.

    Each JD requirement is evaluated individually against the extracted
    profile information. Python calculates the final percentage.
    """

    component_name = criterion_name.lower().strip()

    if component_name not in {"education"}:
        raise ValueError(
            "criterion_name must be 'education'"
        )

    if not jd_requirements:
        return {
            "component": component_name,
            "score": 0,
            "status": "not_required",
            "matched_evidence": [],
            "missing_evidence": [],
            "results": [],
            "reason": "No requirements specified in the job description."
        }

    if not extracted_items:
        return {
            "component": component_name,
            "score": 0,
            "status": "not_found",
            "matched_evidence": [],
            "missing_evidence": jd_requirements,
            "results": [],
            "reason": (
                f"No {component_name} information was found "
                "in the extracted candidate profile."
            )
        }

    prompt = f"""
Evaluate the candidate's extracted {component_name} information
against the job description requirements.

Evaluate each requirement independently.

General rules:
- Use ONLY the candidate information provided.
- Do not invent, assume, or infer unsupported qualifications.
- Evaluate meaning and equivalence, not exact wording.
- Consider recognized equivalent terminology, abbreviations,
  alternate degree naming conventions and closely equivalent
  qualification titles where appropriate.
- Do not reject a valid match merely because the wording differs.
- Return a boolean matched value for every requirement.
- Give a brief reason based only on the provided information.
- Do not assign numerical scores.

For education:
- Consider degree equivalence and the field of study.
- B.Tech in Computer Science and Engineering and B.Tech
  in Computer Science are generally equivalent for this comparison.
- Consider relevant equivalent degree titles where appropriate.
- Do not treat a lower qualification as equivalent to a
  higher qualification.


Job requirements:
{json.dumps(jd_requirements, indent=2)}

Candidate extracted {component_name}:
{json.dumps(extracted_items, indent=2)}

Return valid JSON only in this format:

{{
    "results": [
        {{
            "requirement": "requirement text",
            "matched": false,
            "reason": "brief explanation"
        }}
    ]
}}
"""
    response = await groq_service.generate_text(
        prompt,
        max_completion_tokens=1500
    )

    response = re.sub(r"```(?:json)?", "", response).strip()
    response = re.sub(r"```$", "", response).strip()

    try:
        verification = json.loads(response)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Groq returned invalid {component_name} JSON: {response}"
        ) from exc

    verified_results = verification.get("results", [])

    if not isinstance(verified_results, list):
        raise ValueError(
            f"Invalid results structure returned for {component_name}."
        )

    # Map returned results to the original JD requirements.
    result_map = {}

    for item in verified_results:
        if not isinstance(item, dict):
            continue

        requirement = item.get("requirement")

        if requirement in jd_requirements:
            result_map[requirement] = item

    results = []

    # Ensure every JD requirement is represented.
    for requirement in jd_requirements:

        item = result_map.get(requirement)

        if item is None:
            raise ValueError(
                f"Groq did not evaluate requirement: {requirement}"
            )

        matched = item.get("matched")

        if not isinstance(matched, bool):
            raise ValueError(
                f"Invalid matched value for requirement: {requirement}"
            )

        results.append({
            "requirement": requirement,
            "matched": matched,
            "reason": str(item.get("reason", ""))
        })

    matched_evidence = [
        item for item in results
        if item["matched"]
    ]

    missing_evidence = [
        item for item in results
        if not item["matched"]
    ]

    score = (
        len(matched_evidence) / len(jd_requirements)
    ) * 100

    status = "evaluated" if matched_evidence else "not_found"

    return {
        "component": component_name,
        "score": round(score, 2),
        "status": status,
        "matched_evidence": matched_evidence,
        "missing_evidence": missing_evidence,
        "results": results,
        "reason": (
            f"{len(matched_evidence)} of "
            f"{len(jd_requirements)} {component_name} requirements matched."
        )
    }