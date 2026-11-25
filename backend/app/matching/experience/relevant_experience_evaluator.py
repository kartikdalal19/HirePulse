
# import json
# import re

# from app.services.groq_service import groq_service
# from app.matching.experience.experience_calculator import (
#     calculate_experience
# )


# async def evaluate_relevant_experience(
#     jd_data: dict,
#     employment_records: list[dict]
# ) -> dict:
#     """
#     Identify employment records relevant to the JD and calculate
#     relevant experience using Python.
#     """

#     if not employment_records:
#         return {
#             "relevant_records": [],
#             "relevant_experience": {
#                 "years": 0,
#                 "months": 0,
#                 "total_months": 0
#             },
#             "total_experience": {
#                 "years": 0,
#                 "months": 0,
#                 "total_months": 0
#             }
#         }

#     # Calculate total employment experience.
#     total_result = calculate_experience(employment_records)

#     # Prepare employment records for Groq.
#     records_for_llm = []

#     for index, record in enumerate(employment_records):
#         records_for_llm.append({
#             "record_id": index,
#             "job_title": record.get("job_title"),
#             "company_name": record.get("company_name"),
#             "employment_type": record.get("employment_type"),
#             "description": record.get("description"),
#             "evidence": record.get("evidence")
#         })

#     prompt = f"""
# You are an employment relevance evaluator for a resume matching system.

# Your task is to determine which employment records are relevant
# to the given job description.

# JOB DESCRIPTION:

# {json.dumps(jd_data, indent=2)}

# EMPLOYMENT RECORDS:

# {json.dumps(records_for_llm, indent=2)}

# INSTRUCTIONS:

# 1. Evaluate each employment record independently.
# 2. Consider the job title and actual work responsibilities.
# 3. Consider overlap between the candidate's work and the JD.
# 4. Do not classify a position as relevant based only on its title.
# 5. Internships can be relevant employment experience.
# 6. Do not consider education, projects or certifications as employment.
# 7. Do not calculate employment duration.
# 8. Do not invent information.
# 9. A record can be partially relevant if its responsibilities
#    overlap with the target role.
# 10. Return a relevance decision for every record.

# Return ONLY valid JSON in this structure:

# {{
#     "evaluations": [
#         {{
#             "record_id": 0,
#             "is_relevant": true,
#             "relevance_reason": "Explanation based on the supplied evidence"
#         }}
#     ]
# }}
# """

#     response = await groq_service.generate_text(
#         prompt,
#         max_completion_tokens=1500
#     )

#     response = re.sub(
#         r"^```(?:json)?\s*|\s*```$",
#         "",
#         response.strip(),
#         flags=re.IGNORECASE
#     )

#     try:
#         evaluation_data = json.loads(response)
#     except json.JSONDecodeError as error:
#         raise ValueError(
#             f"Groq returned invalid JSON: {error}"
#         )

#     evaluations = evaluation_data.get("evaluations")

#     if not isinstance(evaluations, list):
#         raise ValueError("Invalid Groq response: evaluations must be a list.")

#     # Validate and map Groq decisions to original records.
#     relevant_records = []
#     evaluated_ids = set()

#     for evaluation in evaluations:
#         record_id = evaluation.get("record_id")
#         is_relevant = evaluation.get("is_relevant")

#         if (
#             not isinstance(record_id, int)
#             or isinstance(record_id, bool)
#             or record_id < 0
#             or record_id >= len(employment_records)
#         ):
#             continue

#         if record_id in evaluated_ids:
#             continue

#         evaluated_ids.add(record_id)

#         if not isinstance(is_relevant, bool):
#             continue

#         if is_relevant:
#             record = employment_records[record_id].copy()

#             record["record_id"] = record_id
#             record["relevance_reason"] = evaluation.get(
#                 "relevance_reason"
#             )

#             relevant_records.append(record)

#     # Calculate relevant experience using Python.
#     relevant_calculation = calculate_experience(
#         relevant_records
#     )

#     return {
#         "total_experience": total_result["total_experience"],
#         "relevant_experience": relevant_calculation["total_experience"],
#         "relevant_records": relevant_calculation["employment_records"],
#         "total_employment_records": len(employment_records),
#         "relevant_employment_records": len(relevant_records)
#     }

import json
import re

from app.services.groq_service import groq_service
from app.matching.experience.experience_calculator import (
    calculate_experience,
    parse_date,
    calculate_month_difference
)


RELEVANCE_WEIGHTS = {
    "highly_relevant": 1.0,
    "partially_relevant": 0.5,
    "not_relevant": 0.0
}


async def evaluate_relevant_experience(
    jd_data: dict,
    employment_records: list[dict]
) -> dict:

    if not employment_records:
        return {
            "total_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            },
            "relevant_experience": {
                "years": 0,
                "months": 0,
                "total_months": 0
            },
            "relevant_records": [],
            "total_employment_records": 0
        }

    # Calculate total employment experience.
    total_result = calculate_experience(employment_records)

    records_for_llm = []

    for index, record in enumerate(employment_records):
        records_for_llm.append({
            "record_id": index,
            "job_title": record.get("job_title"),
            "company_name": record.get("company_name"),
            "employment_type": record.get("employment_type"),
            "description": record.get("description"),
            "evidence": record.get("evidence")
        })

    prompt = f"""
You are an employment relevance evaluator for a resume matching system.

Determine how relevant each employment record is to the given job description.

JOB DESCRIPTION:

{json.dumps(jd_data, indent=2)}

EMPLOYMENT RECORDS:

{json.dumps(records_for_llm, indent=2)}

CLASSIFICATION RULES:

1. highly_relevant:
   Most of the role's responsibilities directly relate to the target job.

2. partially_relevant:
   Some responsibilities relate to the target job, but the role
   is not primarily focused on the target job's requirements.

3. not_relevant:
   The role has little or no meaningful connection to the target job.

ADDITIONAL INSTRUCTIONS:

- Evaluate actual responsibilities, not just job titles.
- Consider required skills and job responsibilities.
- Internships can be relevant.
- Do not calculate employment duration.
- Do not invent information.
- Evaluate every supplied record independently.

Return ONLY valid JSON in this structure:

{{
    "evaluations": [
        {{
            "record_id": 0,
            "relevance_level": "partially_relevant",
            "relevance_reason": "Explanation based on resume evidence"
        }}
    ]
}}
"""

    response = await groq_service.generate_text(
        prompt,
        max_completion_tokens=1500
    )

    response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response.strip(),
        flags=re.IGNORECASE
    )

    try:
        evaluation_data = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Groq returned invalid JSON: {error}"
        )

    evaluations = evaluation_data.get("evaluations")

    if not isinstance(evaluations, list):
        raise ValueError(
            "Invalid Groq response: evaluations must be a list."
        )

    relevant_records = []
    weighted_periods = []
    evaluated_ids = set()

    for evaluation in evaluations:

        record_id = evaluation.get("record_id")
        relevance_level = evaluation.get("relevance_level")

        if (
            not isinstance(record_id, int)
            or isinstance(record_id, bool)
            or record_id < 0
            or record_id >= len(employment_records)
        ):
            continue

        if record_id in evaluated_ids:
            continue

        evaluated_ids.add(record_id)

        if relevance_level not in RELEVANCE_WEIGHTS:
            continue

        record = employment_records[record_id].copy()

        weight = RELEVANCE_WEIGHTS[relevance_level]

        record["record_id"] = record_id
        record["relevance_level"] = relevance_level
        record["relevance_weight"] = weight
        record["relevance_reason"] = evaluation.get(
            "relevance_reason"
        )

        start_date = parse_date(record.get("start_date"))
        end_date = parse_date(
            record.get("end_date"),
            is_end_date=True
        )

        if (
            start_date
            and end_date
            and start_date <= end_date
            and weight > 0
        ):
            duration_months = calculate_month_difference(
                start_date,
                end_date
            )

            record["duration_months"] = duration_months
            record["weighted_duration_months"] = (
                duration_months * weight
            )

            weighted_periods.append({
                "start": start_date,
                "end": end_date,
                "weight": weight,
                "record_id": record_id
            })

        else:
            record["duration_months"] = 0
            record["weighted_duration_months"] = 0

        relevant_records.append(record)

    # Calculate weighted relevant experience.
    # Overlapping employment periods are not double-counted.
    weighted_months = 0

    if weighted_periods:

        boundaries = sorted(
            {
                boundary
                for period in weighted_periods
                for boundary in (
                    period["start"].year * 12 + period["start"].month,
                    period["end"].year * 12 + period["end"].month + 1
                )
            }
        )

        for index in range(len(boundaries) - 1):
            segment_start = boundaries[index]
            segment_end = boundaries[index + 1]

            active_weights = [
                period["weight"]
                for period in weighted_periods
                if (
                    period["start"].year * 12 + period["start"].month
                    <= segment_start
                    and
                    period["end"].year * 12 + period["end"].month + 1
                    >= segment_end
                )
            ]

            if active_weights:
                # Prevent overlapping jobs from exceeding 100%.
                segment_weight = min(1.0, max(active_weights))

                weighted_months += (
                    segment_end - segment_start
                ) * segment_weight

    weighted_months = round(weighted_months)

    return {
        "total_experience": total_result["total_experience"],
        "relevant_experience": {
            "years": weighted_months // 12,
            "months": weighted_months % 12,
            "total_months": weighted_months
        },
        "relevant_records": relevant_records,
        "total_employment_records": len(employment_records),
        "evaluated_employment_records": len(evaluated_ids),
        "relevance_breakdown": {
            level: sum(
                record["relevance_level"] == level
                for record in relevant_records
            )
            for level in RELEVANCE_WEIGHTS
        }
    }
