
# import json
# import re

# from app.services.groq_service import groq_service


# def extract_initial_resume_text(resume_text: str, word_limit: int = 70) -> str:
#     """
#     Extract the initial portion of the resume using a word limit.
#     """

#     words = resume_text.split()
#     return " ".join(words[:word_limit])


# async def extract_candidate_profile(resume_text: str) -> dict:
#     """
#     Extract candidate profile information from the initial resume text.
#     """

#     initial_text = extract_initial_resume_text(resume_text, 70)

#     if not initial_text.strip():
#         return {
#             "candidate_name": None,
#             "email": None,
#             "phone": None,
#             "linkedin": None,
#             "github": None,
#             "portfolio": None,
#             "other_links": [],
#             "professional_title": None,
#             "location": None,
#             "profile_summary": None
#         }

#     prompt = f"""
# Extract candidate profile information from the following resume text.

# Extract ONLY information explicitly present in the text.
# Do not guess, infer, or invent missing details.
# If a field is not found, return null.
# For other_links, return an empty list if none are found.

# Fields to extract:
# - candidate_name
# - email
# - phone
# - linkedin
# - github
# - portfolio
# - other_links
# - professional_title
# - location
# - profile_summary

# Return valid JSON only, using this structure:

# {{
#     "candidate_name": null,
#     "email": null,
#     "phone": null,
#     "linkedin": null,
#     "github": null,
#     "portfolio": null,
#     "other_links": [],
#     "professional_title": null,
#     "location": null,
#     "profile_summary": null
# }}

# Resume text:
# {initial_text}
# """

#     response = await groq_service.generate_text(
#         prompt,
#         max_completion_tokens=1000
#     )

#     response = re.sub(
#         r"```(?:json)?",
#         "",
#         response
#     ).strip()

#     response = re.sub(r"```$", "", response).strip()

#     try:
#         profile = json.loads(response)
#     except json.JSONDecodeError as exc:
#         raise ValueError(
#             f"Groq returned invalid profile JSON: {response}"
#         ) from exc

#     expected_fields = [
#         "candidate_name",
#         "email",
#         "phone",
#         "linkedin",
#         "github",
#         "portfolio",
#         "other_links",
#         "professional_title",
#         "location",
#         "profile_summary"
#     ]

#     # Ensure all expected fields exist.
#     for field in expected_fields:
#         if field not in profile:
#             profile[field] = [] if field == "other_links" else None

#     # Ensure other_links is always a list.
#     if not isinstance(profile["other_links"], list):
#         profile["other_links"] = []

#     return profile





















# import json
# import re

# from app.services.groq_service import groq_service


# def extract_initial_resume_text(resume_text: str, word_limit: int = 70) -> str:
#     """
#     Extract the initial portion of the resume using a word limit.
#     """

#     words = resume_text.split()
#     return " ".join(words[:word_limit])


# async def extract_candidate_profile(resume_text: str) -> dict:
#     """
#     Extract candidate profile information from the initial resume text.
#     """

#     initial_text = extract_initial_resume_text(resume_text, 70)

#     default_profile = {
#         "candidate_name": None,
#         "email": None,
#         "phone": None,
#         "linkedin": None,
#         "github": None,
#         "portfolio": None,
#         "other_links": [],
#         "professional_title": None,
#         "location": None,
#         "profile_summary": None,
#         "education": [],
#     }

#     if not initial_text.strip():
#         return default_profile

#     prompt = f"""
# Extract candidate profile information from the following resume text.

# Extract ONLY information explicitly present in the text.
# Do not guess, infer, or invent missing details.
# If a field is not found, return null.
# For list fields, return an empty list if no information is found.

# Fields to extract:
# - candidate_name
# - email
# - phone
# - linkedin
# - github
# - portfolio
# - other_links
# - professional_title
# - location
# - profile_summary
# - education

# For education:
# Extract explicitly mentioned degrees, qualifications and fields of study.

# Return valid JSON only, using this structure:

# {{
#     "candidate_name": null,
#     "email": null,
#     "phone": null,
#     "linkedin": null,
#     "github": null,
#     "portfolio": null,
#     "other_links": [],
#     "professional_title": null,
#     "location": null,
#     "profile_summary": null,
#     "education": [],
# }}

# Resume text:
# {initial_text}
# """

#     response = await groq_service.generate_text(
#         prompt,
#         max_completion_tokens=1000
#     )

#     response = re.sub(
#         r"```(?:json)?",
#         "",
#         response
#     ).strip()

#     response = re.sub(r"```$", "", response).strip()

#     try:
#         profile = json.loads(response)

#     except json.JSONDecodeError as exc:
#         raise ValueError(
#             f"Groq returned invalid profile JSON: {response}"
#         ) from exc

#     # Ensure all expected fields exist.
#     for field, default_value in default_profile.items():
#         if field not in profile:
#             profile[field] = default_value.copy() if isinstance(
#                 default_value, list
#             ) else default_value

#     # Ensure list fields always contain lists.
#     list_fields = [
#         "other_links",
#         "education",
#     ]

#     for field in list_fields:
#         if not isinstance(profile[field], list):
#             profile[field] = []

#     return profile







import json
import re

from app.services.groq_service import groq_service


MAX_RESUME_WORDS = 1800


def extract_initial_resume_text(
    resume_text: str,
    word_limit: int = MAX_RESUME_WORDS
) -> str:
    """Extract a bounded portion of resume text for profile extraction."""

    words = resume_text.split()
    return " ".join(words[:word_limit])


def parse_profile_json(response: str) -> dict:
    """Parse profile JSON, including responses wrapped in Markdown."""

    cleaned = response.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        cleaned,
        flags=re.IGNORECASE
    ).strip()

    try:
        profile = json.loads(cleaned)
    except json.JSONDecodeError:
        # Attempt to isolate the JSON object if extra text is present.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError("Groq returned invalid profile JSON.")

        try:
            profile = json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError as exc:
            raise ValueError("Groq returned invalid profile JSON.") from exc

    if not isinstance(profile, dict):
        raise ValueError("Groq returned an invalid profile structure.")

    return profile


async def extract_candidate_profile(resume_text: str) -> dict:
    """Extract candidate profile information from resume text."""

    initial_text = extract_initial_resume_text(
        resume_text,
        MAX_RESUME_WORDS
    )

    default_profile = {
        "candidate_name": None,
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None,
        "other_links": [],
        "professional_title": None,
        "location": None,
        "profile_summary": None,
        "education": [],
    }

    if not initial_text.strip():
        return default_profile

    prompt = f"""
Extract candidate profile information from the resume below.

RULES:
- Extract only information explicitly present in the resume.
- Never invent or infer personal details.
- Use null for unavailable scalar fields.
- Use [] for unavailable list fields.
- Keep profile_summary concise (maximum 2 sentences).
- Extract education entries including degree, field, institution,
  and graduation year when explicitly available.
- Do not extract certifications.
- Return JSON only. No Markdown or explanations.
- Return every field in the schema.

JSON SCHEMA:
{{
    "candidate_name": null,
    "email": null,
    "phone": null,
    "linkedin": null,
    "github": null,
    "portfolio": null,
    "other_links": [],
    "professional_title": null,
    "location": null,
    "profile_summary": null,
    "education": []
}}

RESUME:
{initial_text}
"""

    response = await groq_service.generate_text(
        prompt,
        max_completion_tokens=1400
    )

    profile = parse_profile_json(response)

    # Ensure all expected fields exist.
    for field, default_value in default_profile.items():
        if field not in profile:
            profile[field] = (
                default_value.copy()
                if isinstance(default_value, list)
                else default_value
            )

    # Ensure list fields always contain lists.
    for field in ["other_links", "education"]:
        if not isinstance(profile[field], list):
            profile[field] = []

    return profile