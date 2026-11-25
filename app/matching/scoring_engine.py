
# BASE_WEIGHTS = {
#     "required_skills": 40,
#     "responsibilities": 30,
#     "relevant_experience": 20,
#     "preferred_skills": 10
# }

BASE_WEIGHTS = {
    "required_skills": 40,
    "responsibilities": 30,
    "relevant_experience": 20,
    "preferred_skills": 10,
    "education": 10
}

# def get_active_components(jd_data: dict) -> dict:
#     """
#     Determines which scoring components are applicable
#     based on the job description.
#     """

#     active = {}

#     if jd_data.get("required_skills"):
#         active["required_skills"] = BASE_WEIGHTS["required_skills"]

#     if jd_data.get("responsibilities"):
#         active["responsibilities"] = BASE_WEIGHTS["responsibilities"]

#     if jd_data.get("minimum_experience_years") is not None:
#         active["relevant_experience"] = BASE_WEIGHTS["relevant_experience"]

#     if jd_data.get("preferred_skills"):
#         active["preferred_skills"] = BASE_WEIGHTS["preferred_skills"]

#     return active
def get_active_components(jd_data: dict) -> dict:
    """
    Determines which scoring components are applicable
    based on the job description.
    """

    active = {}

    if jd_data.get("required_skills"):
        active["required_skills"] = BASE_WEIGHTS["required_skills"]

    if jd_data.get("responsibilities"):
        active["responsibilities"] = BASE_WEIGHTS["responsibilities"]

    if jd_data.get("minimum_experience_years") is not None:
        active["relevant_experience"] = BASE_WEIGHTS["relevant_experience"]

    if jd_data.get("preferred_skills"):
        active["preferred_skills"] = BASE_WEIGHTS["preferred_skills"]

    if jd_data.get("education_requirements"):
        active["education"] = BASE_WEIGHTS["education"]


    return active

def normalize_weights(active_components: dict) -> dict:
    """
    Normalizes active component weights so their total is 100%.
    """

    total_weight = sum(active_components.values())

    if total_weight == 0:
        return {}

    normalized = {}

    for component, weight in active_components.items():
        normalized[component] = round(
            (weight / total_weight) * 100, 2
        )

    return normalized


def prepare_scoring_structure(jd_data: dict) -> dict:
    """
    Prepares active scoring components and normalized weights.
    """

    active_components = get_active_components(jd_data)
    normalized_weights = normalize_weights(active_components)

    return {
        "active_components": active_components,
        "normalized_weights": normalized_weights,
        "total_active_weight": sum(active_components.values())
    }





def calculate_skill_component(result: dict, component_name: str) -> dict:
    """
    Calculates a skill component score using the evaluator's
    match percentage.
    """

    score = result.get("match_percentage", 0)

    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])

    return {
        "component": component_name,
        "score": round(float(score), 2),
        "status": "evaluated" if matched else "not_found",
        "matched_evidence": matched,
        "missing_evidence": missing,
        "reason": (
            f"{len(matched)} of "
            f"{len(matched) + len(missing)} skills matched."
        )
    }


# def calculate_responsibility_component(result: dict) -> dict:
#     """
#     Calculates responsibility score using the evaluator's
#     coverage percentage.
#     """

#     score = result.get("coverage_percentage", 0)
#     responsibilities = result.get("results", [])

#     matched = [
#         item for item in responsibilities
#         if item.get("considered", False)
#     ]

#     missing = [
#         item for item in responsibilities
#         if not item.get("considered", False)
#     ]

#     return {
#         "component": "responsibilities",
#         "score": round(float(score), 2),
#         "status": "evaluated" if matched else "not_found",
#         "matched_evidence": matched,
#         "missing_evidence": missing,
#         "reason": (
#             f"{len(matched)} of "
#             f"{len(responsibilities)} responsibilities verified."
#         )
#     }


def calculate_responsibility_component(result: dict) -> dict:
    """
    Calculates the responsibility component using partial-credit scores.
    """

    score = result.get("coverage_percentage", 0)
    responsibilities = result.get("results", [])

    fully_matched = [
        item for item in responsibilities
        if item.get("responsibility_score", 0) >= 1.0
    ]

    partially_matched = [
        item for item in responsibilities
        if 0 < item.get("responsibility_score", 0) < 1.0
    ]

    missing = [
        item for item in responsibilities
        if item.get("responsibility_score", 0) <= 0
    ]

    total = len(responsibilities)

    return {
        "component": "responsibilities",
        "score": round(float(score), 2),
        "status": (
            "evaluated"
            if fully_matched or partially_matched
            else "not_found"
        ),
        "matched_evidence": fully_matched,
        "partial_evidence": partially_matched,
        "missing_evidence": missing,
        "reason": (
            f"{len(fully_matched)} fully supported, "
            f"{len(partially_matched)} partially supported, "
            f"{len(missing)} unsupported out of {total} responsibilities."
        )
    }

def calculate_experience_component(
    result: dict,
    required_months: int
) -> dict:
    """
    Calculates the relevant experience score
    against the JD's minimum experience.
    """

    relevant_experience = result.get("relevant_experience", {})
    relevant_months = relevant_experience.get("total_months", 0)

    if required_months <= 0:
        score = 100 if relevant_months > 0 else 0
    else:
        score = min(
            (relevant_months / required_months) * 100,
            100
        )

    return {
        "component": "relevant_experience",
        "score": round(score, 2),
        "status": "evaluated" if relevant_months > 0 else "not_found",
        "matched_evidence": result.get("employment_records", []),
        "missing_evidence": [],
        "reason": (
            f"{relevant_months} relevant months evaluated "
            f"against {required_months} required months."
        )
    }





def calculate_overall_score(component_results: list, normalized_weights: dict) -> dict:
    """
    Calculates the overall score using component scores
    and normalized weights.
    """

    overall_score = 0
    breakdown = []

    for result in component_results:
        component = result["component"]

        if component not in normalized_weights:
            continue

        weight = normalized_weights[component]
        score = result["score"]
        contribution = round((score * weight) / 100, 2)

        overall_score += contribution

        breakdown.append({
            **result,
            "weight": weight,
            "contribution": contribution
        })

    return {
        "overall_score": round(overall_score, 2),
        "breakdown": breakdown,
        "total_weight": sum(
            item["weight"] for item in breakdown
        )
    }


def calculate_education_component(result: dict) -> dict:
    return {
        "component": "education",
        "score": round(float(result.get("score", 0)), 2),
        "status": result.get("status", "not_found"),
        "matched_evidence": result.get("matched_evidence", []),
        "missing_evidence": result.get("missing_evidence", []),
        "reason": result.get("reason", "")
    }