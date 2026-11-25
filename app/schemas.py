
from pydantic import BaseModel, Field


class JobDescriptionData(BaseModel):

    job_title: str | None = None
    role_summary: str | None = None

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    minimum_experience_years: float | None = Field(
        default=None,
        ge=0
    )

    education_requirements: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)

    job_location: str | None = None
    employment_type: str | None = None


class JobDescriptionResponse(BaseModel):

    job_id: str
    status: str
    original_text: str
    extracted_requirements: JobDescriptionData
