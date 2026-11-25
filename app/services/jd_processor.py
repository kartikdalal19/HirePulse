
import json
import re

from app.services.groq_service import groq_service


def extract_json(response: str) -> dict:
    """
    Extract JSON from the model response.
    Handles responses containing Markdown code fences.
    """

    cleaned = response.strip()

    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to locate a JSON object within the response.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("The AI did not return valid JSON")

        return json.loads(cleaned[start:end + 1])


async def process_job_description(jd_text: str) -> dict:

    prompt = f"""
Analyze the following job description and extract its requirements.

Return ONLY a valid JSON object with these exact keys:

{{
    "job_title": "string or null",
    "role_summary": "string or null",
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "minimum_experience_years": 2,
    "education_requirements": ["qualification1"],
    "responsibilities": ["responsibility1"],
    "job_location": "string or null",
    "employment_type": "string or null"
}}

Rules:
1. Extract only information supported by the job description.
2. Do not invent skills, qualifications or experience requirements.
3. Separate mandatory skills from preferred or optional skills.
4. If a skill is not clearly categorized, do not assume it is mandatory.
5. minimum_experience_years must be a number or null.
6. If experience is given as a range, use the minimum number.
7. If experience is not specified, return null.
8. Keep skill names concise and avoid duplicates.
9. Do not include protected personal attributes as job requirements.
10. Return empty arrays when no information is available.
11. Return valid JSON only. Do not add explanations or Markdown.

JOB DESCRIPTION:
{jd_text}
"""

    response = await groq_service.generate_text(
        prompt,
        max_completion_tokens=2000
    )

    extracted_data = extract_json(response)

    return extracted_data
