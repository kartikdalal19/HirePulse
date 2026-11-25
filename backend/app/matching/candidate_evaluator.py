
from app.matching.skills.required_skills_evaluator import (
    evaluate_required_skills
)
from app.matching.skills.preferred_skills_evaluator import (
    evaluate_preferred_skills
)
from app.matching.responsibilities.responsibility_evaluator import (
    evaluate_responsibilities
)
from app.matching.experience.experience_evaluator import (
    evaluate_experience
)
from app.nlp.candidate_profile_extractor import (
    extract_candidate_profile
)
from app.matching.profile_criteria_evaluator import (
    evaluate_profile_criterion
)
from app.matching.scoring_engine import (
    prepare_scoring_structure,
    calculate_skill_component,
    calculate_responsibility_component,
    calculate_experience_component,
    calculate_education_component,
    calculate_overall_score
)


async def evaluate_candidate(
    jd_data: dict,
    resume_text: str,
    use_llm_responsibility_verification: bool = True
) -> dict:
    """
    Run all applicable candidate evaluation components
    and calculate the final overall score.
    """

    # Step 1: Prepare dynamic scoring structure.
    scoring_structure = prepare_scoring_structure(jd_data)

    active_components = scoring_structure["active_components"]
    normalized_weights = scoring_structure["normalized_weights"]

    component_results = []

    # Step 2: Required skills evaluation.
    if "required_skills" in active_components:

        result = await evaluate_required_skills(
            jd_data.get("required_skills", []),
            resume_text
        )

        component_results.append(
            calculate_skill_component(
                result,
                "required_skills"
            )
        )

    # Step 3: Preferred skills evaluation.
    if "preferred_skills" in active_components:

        result = await evaluate_preferred_skills(
            jd_data.get("preferred_skills", []),
            resume_text
        )

        component_results.append(
            calculate_skill_component(
                result,
                "preferred_skills"
            )
        )

    # Step 4: Responsibilities evaluation.
    if "responsibilities" in active_components:

        result = await evaluate_responsibilities(
            jd_data.get("responsibilities", []),
            resume_text,
            use_llm_verification=(
                use_llm_responsibility_verification
            )
        )

        component_results.append(
            calculate_responsibility_component(result)
        )

    # Step 5: Relevant experience evaluation.
    if "relevant_experience" in active_components:

        result = await evaluate_experience(
            jd_data,
            resume_text
        )

        required_months = int(
            jd_data.get("minimum_experience_years", 0) * 12
        )

        component_results.append(
            calculate_experience_component(
                result,
                required_months
            )
        )

    # Step 6: Candidate profile extraction.
    profile = await extract_candidate_profile(resume_text)

    # Step 7: Education evaluation.
    if "education" in active_components:

        education_result = await evaluate_profile_criterion(
            "education",
            jd_data.get("education_requirements", []),
            profile.get("education", [])
        )

        component_results.append(
            calculate_education_component(education_result)
        )

    # Step 8: Calculate final overall score.
    scoring_result = calculate_overall_score(
        component_results,
        normalized_weights
    )

    # Step 9: Return unified result.
    return {
        "status": "completed",
        "candidate_profile": profile,
        "scoring_structure": scoring_structure,
        "overall_score": scoring_result["overall_score"],
        "total_weight": scoring_result["total_weight"],
        "component_breakdown": scoring_result["breakdown"]
    }
