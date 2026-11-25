
import json
import re

from app.services.groq_service import groq_service
from app.schemas.resume_schema import CandidateProfile


def extract_contact_details(text: str) -> dict:
    """Extract email and phone using regular expressions."""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    phone_match = re.search(
        r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?\d{10}(?!\d)",
        text
    )

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None
    }


async def extract_candidate_profile(resume_text: str) -> CandidateProfile:
    """Extract structured candidate information using Groq."""

    contact_details = extract_contact_details(resume_text)

    prompt = f"""
Analyze the following resume and extract candidate information.

Return ONLY valid JSON. Do not include Markdown or explanations.

Required JSON structure:
{{
    "candidate_name": null,
    "email": null,
    "phone": null,
    "skills": [],
    "total_experience_years": null,
    "work_experience": [
        {{
            "job_title": null,
            "company": null,
            "start_date": null,
            "end_date": null,
            "description": []
        }}
    ],
    "education": [
        {{
            "degree": null,
            "institution": null,
            "graduation_year": null,
            "grade": null
        }}
    ],
    "projects": [
        {{
            "name": null,
            "technologies": [],
            "description": null
        }}
    ],
    "certifications": []
}}

Rules:
1. Extract only information supported by the resume.
2. Do not invent missing information.
3. Use null for missing single values and [] for missing lists.
4. Include technical and relevant professional skills.
5. Estimate total professional work experience only from employment dates.
6. Do not count education, personal projects or internships as full-time employment unless explicitly stated.
7. Avoid double-counting overlapping employment periods.
8. Return graduation_year as an integer when available.
9. Keep project descriptions concise.

Resume:
{resume_text}
"""

    response = await groq_service.generate_text(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        # Handle JSON accidentally wrapped in Markdown fences.
        cleaned = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            response.strip(),
            flags=re.IGNORECASE
        )
        data = json.loads(cleaned)

    # Prefer regex-extracted contact details.
    data["email"] = contact_details["email"] or data.get("email")
    data["phone"] = contact_details["phone"] or data.get("phone")

    return CandidateProfile.model_validate(data)
