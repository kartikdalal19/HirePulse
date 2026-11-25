# HirePulse — AI-Based Resume Matching & Ranking System

HirePulse is an AI-powered resume screening and ranking system that evaluates multiple candidate resumes against a Job Description (JD). It combines keyword matching, semantic similarity, experience evaluation, responsibility analysis and explainable scoring to help recruiters assess candidate relevance.

The system supports batch resume evaluation, candidate ranking, detailed candidate-level analysis and downloadable PDF screening reports.

---

## Features

- **Job Description Analysis:** Paste or upload a Job Description and extract structured requirements, skills, responsibilities, experience and qualifications.
- **Batch Resume Upload:** Upload and evaluate multiple PDF and DOCX resumes in a single screening session.
- **Resume Parsing:** Extract candidate profiles, contact details, education and employment information.
- **Semantic Skill Matching:** Identify relevant skills beyond exact keyword matches using embeddings.
- **Responsibility Matching:** Compare candidate experience against job responsibilities using semantic similarity and optional LLM-based verification.
- **Relevant Experience Evaluation:** Identify relevant employment records and calculate weighted relevant experience.
- **Explainable Scoring:** Generate a score out of 100 using weighted evaluation components.
- **Candidate Ranking:** Automatically rank candidates based on their overall matching scores.
- **Candidate-Level Analysis:** View detailed profiles, matched and missing skills, responsibility evidence, experience records and score explanations.
- **Live Evaluation Progress:** Track batch evaluation progress and view completed candidates as they are evaluated.
- **Detailed PDF Report:** Generate a consolidated report containing rankings and detailed evaluation results for all successfully evaluated candidates.

---

## Technology Stack

| Category              | Technology                                       |
| --------------------- | ------------------------------------------------ |
| Frontend              | HTML5, CSS3, JavaScript                          |
| UI Styling            | Custom CSS, Font Awesome                         |
| Backend               | Python, FastAPI                                  |
| API Communication     | REST API, Server-Sent Events (SSE)               |
| Resume Parsing        | PyMuPDF, python-docx                             |
| LLM                   | Groq API                                         |
| LLM Model             | `openai/gpt-oss-20b` (configurable)              |
| Embeddings            | Cloudflare Workers AI                            |
| Embedding Model       | `@cf/baai/bge-small-en-v1.5`                     |
| Semantic Similarity   | Embeddings, Cosine Similarity                    |
| Skill Matching        | Keyword Matching, Semantic Matching              |
| Experience Analysis   | Python, Semantic Retrieval, LLM-based Extraction |
| PDF Report Generation | jsPDF, jsPDF-AutoTable                           |
| Configuration         | pydantic-settings, python-dotenv                 |

---

## Project Architecture

HirePulse follows a modular architecture separating the frontend, API layer, parsing, NLP processing, matching, scoring and ranking.

```
User
 │
 ▼
Frontend (HTML, CSS, JavaScript)
 │
 │ HTTP / Fetch / FormData
 ▼
FastAPI Backend
 │
 ├── Job Description Processing
 │
 ├── Resume Parsing
 │
 ├── Candidate Profile Extraction
 │
 ├── Skill Matching
 │      ├── Keyword Matching
 │      └── Semantic Matching
 │
 ├── Responsibility Matching
 │      ├── Semantic Retrieval
 │      └── LLM Verification
 │
 ├── Relevant Experience Evaluation
 │
 ├── Education Evaluation
 │
 ├── Scoring Engine
 │
 └── Ranking Engine
        │
        ▼
   Candidate Results
        │
        ▼
Frontend Ranking Dashboard
        │
        ├── Candidate Analysis
        └── Downloadable PDF Report
```

---

## Project Directory Structure

```
HirePulse/
│
├── backend/
│   ├── .env
│   ├── .env.example
│   ├── resume_schema.py
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── schemas.py
│       │
│       ├── api/
│       │   ├── batch_routes.py
│       │   ├── jd_routes.py
│       │   └── resume_routes.py
│       │
│       ├── nlp/
│       │   └── candidate_profile_extractor.py
│       │
│       ├── parsers/
│       │   ├── docx_parser.py
│       │   ├── jd_parser.py
│       │   └── pdf_parser.py
│       │
│       ├── services/
│       │   ├── embedding_service.py
│       │   ├── groq_service.py
│       │   ├── jd_processor.py
│       │   └── resume_extraction_service.py
│       │
│       ├── matching/
│       │   ├── batch_evaluator.py
│       │   ├── candidate_evaluator.py
│       │   ├── profile_criteria_evaluator.py
│       │   ├── ranking_engine.py
│       │   ├── scoring_engine.py
│       │   │
│       │   ├── skills/
│       │   │   ├── keyword_matcher.py
│       │   │   ├── preferred_skills_evaluator.py
│       │   │   ├── required_skills_evaluator.py
│       │   │   ├── semantic_skill_matcher.py
│       │   │   └── skill_matcher.py
│       │   │
│       │   ├── responsibilities/
│       │   │   ├── llm_responsibility_verifier.py
│       │   │   ├── responsibility_chunker.py
│       │   │   ├── responsibility_evaluator.py
│       │   │   ├── responsibility_matcher.py
│       │   │   ├── responsibility_verifier.py
│       │   │   └── semantic_responsibility_matcher.py
│       │   │
│       │   └── experience/
│       │       ├── experience_calculator.py
│       │       ├── experience_evaluator.py
│       │       ├── experience_extractor.py
│       │       ├── relevant_experience_evaluator.py
│       │       └── semantic_experience_search.py
│       │
│       ├── storage/
│       │   └── memory_store.py
│       │
│       └── utils/
│           └── file_validator.py
│
├── frontend/
│   ├── index.html
│   ├── index1.html
│   ├── screening.html
│   ├── upload-resumes.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── script.js
│       ├── screening.js
│       └── upload-resumes.js
│
├── sample_data/
│   ├── job_descriptions/
│   └── resumes/
│
│
├── README.md
└── requirements.txt
```

---

## File and Module Description

### 1. Backend

The backend is built using FastAPI and handles job description processing, resume extraction, candidate evaluation, scoring and ranking.

#### Core application

| File                      | Description                                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `app/main.py`             | Main FastAPI application entry point. Registers API routers, configures CORS and exposes application endpoints. |
| `app/config.py`           | Loads application settings, API credentials and model configuration from environment variables.                 |
| `app/schemas.py`          | Defines data structures and validation schemas used throughout the application.                                 |
| `app/__init__.py`.        | Marks the application directory as a Python package.                                                            |
| `backend/resume_schema.py`| Defines Pydantic models for structured resume data, including work experience, education, projects, candidate   | |                           |   profiles and resume processing results. Provides validation for extracted candidate information.              |

#### API Routes — `app/api/`

| File               | Description                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `batch_routes.py`  | Handles batch resume evaluation requests and streams evaluation progress and results through Server-Sent Events (SSE). |
| `jd_routes.py`     | Accepts pasted or uploaded Job Descriptions and returns structured job requirements.                                   |
| `resume_routes.py` | Handles individual resume upload and processing API operations.                                                        |

#### NLP — `app/nlp/`

| File                             | Description                                                                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `candidate_profile_extractor.py` | Extracts candidate information such as name, contact details, professional title, location, summary, education and profile links using the LLM. |

#### Parsing — `app/parsers/`

| File             | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `pdf_parser.py`  | Extracts textual content from PDF resumes using PyMuPDF.                    |
| `docx_parser.py` | Extracts text and table content from DOCX documents using python-docx.      |
| `jd_parser.py`   | Provides parsing utilities for Job Description text and related processing. |

#### Services — `app/services/`

| File                           | Description                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| `groq_service.py`              | Manages Groq API requests, retries and request rate limiting.                            |
| `embedding_service.py`         | Communicates with Cloudflare Workers AI to generate text embeddings.                     |
| `jd_processor.py`              | Processes Job Descriptions and converts them into structured requirements using the LLM. |
| `resume_extraction_service.py` | Handles resume text extraction and related resume processing operations.                 |

#### Matching Engine — `app/matching/`

| File                            | Description                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `candidate_evaluator.py`        | Orchestrates the complete evaluation of an individual candidate against the Job Description.           |
| `batch_evaluator.py`            | Evaluates multiple resumes sequentially, tracks progress, handles failures and prepares batch results. |
| `ranking_engine.py`             | Sorts successfully evaluated candidates based on their overall matching scores.                        |
| `scoring_engine.py`             | Calculates component scores, normalized weights, score contributions and the final matching score.     |
| `profile_criteria_evaluator.py` | Evaluates profile-related criteria such as educational qualifications against the JD.                  |

#### Skills Matching — `app/matching/skills/`

| File                            | Description                                                                                               |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `keyword_matcher.py`            | Performs normalized, case-insensitive keyword matching with evidence extraction.                          |
| `semantic_skill_matcher.py`     | Uses embeddings and cosine similarity to identify skills that are semantically relevant to the resume.    |
| `skill_matcher.py`              | Coordinates keyword and semantic skill matching.                                                          |
| `required_skills_evaluator.py`  | Evaluates mandatory skills, identifies matched and missing skills and calculates required skill coverage. |
| `preferred_skills_evaluator.py` | Evaluates preferred or optional skills and calculates preferred skill coverage.                           |

#### Responsibility Matching — `app/matching/responsibilities/`

| File                                 | Description                                                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `responsibility_chunker.py`          | Splits resume text into meaningful chunks for responsibility-related retrieval.                     |
| `semantic_responsibility_matcher.py` | Retrieves relevant resume chunks for each Job Description responsibility using semantic similarity. |
| `responsibility_matcher.py`          | Provides responsibility matching functionality and related matching operations.                     |
| `responsibility_verifier.py`         | Provides responsibility verification logic.                                                         |
| `llm_responsibility_verifier.py`     | Uses the LLM to evaluate evidence supporting responsibility sub-actions and provide partial credit. |
| `responsibility_evaluator.py`        | Aggregates responsibility matching and verification results into a responsibility coverage score.   |

#### Experience Evaluation — `app/matching/experience/`

| File                               | Description                                                                                                           |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `semantic_experience_search.py`    | Retrieves relevant employment-related resume chunks using embeddings and semantic similarity.                         |
| `experience_extractor.py`          | Extracts employment records, job titles, companies, employment dates and descriptions from retrieved resume evidence. |
| `experience_calculator.py`         | Calculates total employment duration while handling date formats and overlapping employment periods.                  |
| `relevant_experience_evaluator.py` | Evaluates the relevance of individual employment records to the target role.                                          |
| `experience_evaluator.py`          | Coordinates experience retrieval, extraction, calculation and relevance evaluation.                                   |

#### Storage — `app/storage/`

| File              | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `memory_store.py` | Provides in-memory storage functionality for application data. |

#### Utilities — `app/utils/`

| File                | Description                                                                      |
| ------------------- | -------------------------------------------------------------------------------- |
| `file_validator.py` | Validates uploaded resume file types, file sizes and related upload constraints. |

---

### 2. Frontend

The frontend is built using HTML, CSS and vanilla JavaScript.

#### HTML Pages

| File                  | Description                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `index.html`          | Main landing page introducing HirePulse, its capabilities and screening workflow.                                       |
| `screening.html`      | Interface for entering or uploading a Job Description and initiating analysis.                                          |
| `upload-resumes.html` | Interface for uploading resumes, tracking evaluation progress, viewing rankings and accessing candidate-level analysis. |
| `index1.html`         | Additional HTML page retained in the project.                                                                           |

#### CSS — `frontend/css/`

| File        | Description                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `style.css` | Contains the application's UI styling, layouts, navigation, forms, tables, modals, responsive styles and visual components. |

#### JavaScript — `frontend/js/`

| File                | Description                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `script.js`         | Handles common frontend interactions and homepage navigation.                                                                                |
| `screening.js`      | Handles Job Description input, API submission, response processing and navigation to the resume evaluation screen.                           |
| `upload-resumes.js` | Handles resume uploads, file validation, SSE progress tracking, dynamic ranking tables, candidate analysis modals and PDF report generation. |

---

### 3. Sample Data

The `sample_data/` directory contains test data used during development and testing.

| Directory                       | Description                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------- |
| `sample_data/job_descriptions/` | Sample Job Descriptions for testing the screening workflow.                   |
| `sample_data/resumes/`          | Sample PDF and DOCX resumes used for candidate evaluation and matching tests. |

Sample data should be synthetic or publicly licensed. Do not use real candidate personal information.

---

## How HirePulse Works

### Step 1: Job Description Input

The recruiter enters or uploads a Job Description.

The system processes the JD using the Groq API and extracts structured information such as:

- Job title
- Required skills
- Preferred skills
- Required responsibilities
- Minimum experience
- Educational qualifications

The extracted requirements are used as the reference for candidate evaluation.

### Step 2: Resume Upload and Parsing

The recruiter uploads multiple PDF or DOCX resumes.

The backend:

1. Validates file types and file sizes.
2. Extracts text from PDF and DOCX documents.
3. Processes extracted text for matching and retrieval.
4. Extracts candidate profile information.
5. Prepares resume evidence for evaluation.

### Step 3: Skill Matching

The system evaluates required and preferred skills using two approaches:

**Keyword Matching**

- Normalizes text and skill names.
- Performs case-insensitive matching.
- Identifies relevant skill mentions.
- Extracts evidence from the resume.

**Semantic Matching**

- Generates embeddings for JD skills and resume text chunks.
- Calculates cosine similarity.
- Identifies semantically relevant evidence even when exact keywords are not present.
- Uses a configurable similarity threshold to determine whether semantic evidence qualifies as a match.

This hybrid approach reduces reliance on exact keyword matching.

### Step 4: Responsibility Matching

The Job Description responsibilities are compared with relevant resume chunks.

The process includes:

1. Splitting resume text into meaningful chunks.
2. Generating embeddings for responsibilities and resume chunks.
3. Retrieving relevant evidence using semantic similarity.
4. Using LLM-based verification to assess supporting evidence where enabled.
5. Evaluating responsibility sub-actions and assigning partial credit where applicable.

Responsibilities are evaluated based on supporting evidence rather than exact textual similarity alone.

### Step 5: Relevant Experience Evaluation

The experience evaluation pipeline:

1. Retrieves employment-related resume chunks.
2. Extracts employment records.
3. Identifies job titles, companies, descriptions and dates.
4. Calculates employment duration.
5. Evaluates role relevance against the target Job Description.
6. Assigns relevance weights to employment records.
7. Calculates weighted relevant experience while avoiding double-counting overlapping employment periods.

### Step 6: Education Evaluation

The system evaluates educational qualifications using extracted education information and the criteria specified in the Job Description.

### Step 7: Score Calculation

The scoring engine combines active evaluation components using weighted scoring.

The final score is calculated using component scores and normalized component weights.

### Step 8: Ranking

Candidates are sorted by overall matching score in descending order.

The ranking dashboard displays:

- Rank
- Candidate name
- Experience evaluation
- Overall matching score
- Matched skills
- Candidate-level analysis

### Step 9: Candidate-Level Analysis

Recruiters can open an individual candidate's analysis to view:

- Extracted candidate information
- Overall score
- Component score breakdown
- Required and preferred skill matching
- Missing skill evidence
- Responsibility evaluation
- Employment records
- Relevant experience
- Matching explanations

### Step 10: PDF Report

The recruiter can generate a consolidated PDF screening report containing candidate rankings and detailed candidate evaluation results.

---

## Scoring Methodology

HirePulse uses a weighted scoring system combining required skills, responsibilities, relevant experience, preferred skills and education.

### Base Component Weights

| Component           | Base Weight |
| ------------------- | ----------- |
| Required Skills     | 40%         |
| Responsibilities    | 30%         |
| Relevant Experience | 20%         |
| Preferred Skills    | 10%         |
| Education           | 10%         |
| **Total**           | **110%**    |

The base weights are not used as a fixed 110% scoring formula. Instead, weights are dynamically normalized based on which evaluation components are applicable to the Job Description.

### Dynamic Weight Normalization

If a component is not applicable, its weight is excluded and the remaining weights are proportionally normalized to total 100%.

For each active component:

[\
W_i = \frac{B_i}{\sum\_{j \in A} B_j}\times100\
]

Where:

- (W_i) = normalized weight of component (i)
- (B_i) = base weight of component (i)
- (A) = set of active components

### Overall Score

The final score is calculated using:

[\
S = \sum\_{i \in A} \left(\frac{C_i \times W_i}{100}\right)\
]

Where:

- (S) = overall candidate score
- (C_i) = component score between 0 and 100
- (W_i) = normalized component weight

The final score ranges from 0 to 100.

### Component Evaluation

| Component           | Evaluation Method                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| Required Skills     | Keyword matching and semantic matching of required skills.                                     |
| Responsibilities    | Semantic retrieval, evidence evaluation and optional LLM-based partial verification.           |
| Relevant Experience | Role relevance and weighted relevant employment duration compared against required experience. |
| Preferred Skills    | Keyword and semantic evaluation of preferred skills.                                           |
| Education           | Evaluation of extracted educational qualifications against the JD.                             |

The numerical score is calculated by Python. The LLM is used for extraction and evidence evaluation, not as an independent authority that assigns the final numerical matching score.

### Relevant Experience Scoring

Relevant experience is evaluated using weighted employment duration.

Employment records are classified according to their relevance to the target role. Relevant and partially relevant employment records contribute differently to the total weighted experience.

The experience score is capped at 100.

The experience component is included when a minimum experience requirement is specified in the Job Description.

### Important Scoring Considerations

- Components are dynamically weighted according to applicable JD criteria.
- Matching scores are based on evidence extracted from resumes.
- Missing evidence does not necessarily mean a candidate lacks a skill or qualification.
- Semantic matching helps identify relevant information expressed differently.
- Scores are intended to support recruiter decisions, not replace human judgment.

---

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Groq API key
- Cloudflare Workers AI API token
- Cloudflare Account ID

### 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/HirePulse.git
cd HirePulse
```

### 2. Create a Virtual Environment

```
python -m venv venv
```

Activate it:

**macOS/Linux**

```
source venv/bin/activate
```

**Windows**

```
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create or update `backend/.env`.

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_EMBEDDING_MODEL=@cf/baai/bge-small-en-v1.5
```

Use the `.env.example` file as a reference for configuration.

Never commit your actual `.env` file or API keys to GitHub.

### 5. Run the Backend

From the project root:

```
cd backend
uvicorn app.main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

### 6. Access API Documentation

FastAPI automatically provides interactive API documentation.

`http://127.0.0.1:8000/docs`

### 7. Run the Frontend

Open a separate terminal.

From the project root:

```
cd frontend
python -m http.server 5500
```

Open:

`http://localhost:5500`

---

## API Endpoints

| Endpoint              | Method | Description                                                                                    |
| --------------------- | ------ | ---------------------------------------------------------------------------------------------- |
| `/`                   | GET    | Root endpoint for the backend application.                                                     |
| `/health`             | GET    | Health-check endpoint.                                                                         |
| `/api/jd/analyze`     | POST   | Accepts a Job Description and extracts structured requirements.                                |
| `/api/resumes/upload` | POST   | Handles individual resume upload and processing.                                               |
| `/api/batch/evaluate` | POST   | Evaluates multiple resumes against the supplied JD and streams progress and results using SSE. |

The API documentation is available through FastAPI Swagger UI at `/docs`.

---

## Limitations

- The application currently uses in-memory storage rather than a persistent database.
- Data is not permanently stored between sessions or application restarts.
- Semantic matching thresholds are configurable and may require tuning for different job roles.
- LLM-based extraction and verification can produce imperfect results.
- Resume parsing accuracy depends on document formatting and text extraction quality.
- Scanned PDFs containing images may require OCR, which is not currently integrated.
- The application is a screening prototype and is not intended to make automated hiring decisions.
- Evaluation results should be reviewed by a human recruiter before making hiring decisions.

---

## Responsible Use

HirePulse is designed as a decision-support tool for recruitment screening.

- Use synthetic or publicly licensed test resumes.
- Do not use sensitive personal attributes to calculate matching scores.
- Do not treat missing evidence as definitive proof that a candidate lacks a qualification.
- Review candidate results manually before making hiring decisions.
- Use the system transparently and responsibly.

---

## Future Improvements

- Persistent PostgreSQL database integration.
- OCR support for scanned resumes.
- Advanced recruiter filters and candidate comparison.
- Improved experience timeline analysis.
- Deployment optimizations and asynchronous processing.
- Additional evaluation metrics and scoring calibration.
- Authentication and role-based access control.

---

## Author

**Developed by Kartik Dalal**

- GitHub: [kartikdalal19](https://github.com/kartikdalal19)

---

## License

This project was developed as an AI-based resume matching and ranking system prototype for educational and development purposes.


Next, I'd recommend generating your `requirements.txt` and `.gitignore` properly before pushing HirePulse to GitHub and deploying it on Render.
