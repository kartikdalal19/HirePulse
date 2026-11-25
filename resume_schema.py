from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class WorkExperience(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: list[str] = Field(default_factory=list)


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    grade: Optional[str] = None


class Project(BaseModel):
    name: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    description: Optional[str] = None


class CandidateProfile(BaseModel):
    candidate_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    skills: list[str] = Field(default_factory=list)

    total_experience_years: Optional[float] = Field(
        default=None,
        ge=0
    )

    work_experience: list[WorkExperience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ResumeProcessingResult(BaseModel):
    resume_id: str
    filename: str
    status: str
    extracted_text: Optional[str] = None
    candidate_profile: Optional[CandidateProfile] = None
    error: Optional[str] = None