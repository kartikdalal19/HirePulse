
import re
import numpy as np

from app.services.embedding_service import embedding_service


# Initial threshold for testing.
# We will calibrate this using sample resumes later.
SEMANTIC_THRESHOLD = 0.72


def split_resume_into_chunks(resume_text: str) -> list[str]:
    """
    Split resume text into smaller meaningful chunks.
    Each paragraph is split further if it is too long.
    """
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n+", resume_text)
        if paragraph.strip()
    ]

    chunks = []

    for paragraph in paragraphs:
        if len(paragraph) <= 500:
            chunks.append(paragraph)
        else:
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)

            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= 500:
                    current_chunk += " " + sentence
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence

            if current_chunk.strip():
                chunks.append(current_chunk.strip())

    return chunks


def calculate_cosine_similarity(
    query_embedding: list[float],
    chunk_embeddings: list[list[float]]
) -> list[float]:

    query_vector = np.array(query_embedding, dtype=float)
    chunk_vectors = np.array(chunk_embeddings, dtype=float)

    query_norm = np.linalg.norm(query_vector)
    chunk_norms = np.linalg.norm(chunk_vectors, axis=1)

    if query_norm == 0:
        return [0.0] * len(chunk_embeddings)

    similarities = np.dot(chunk_vectors, query_vector) / (
        chunk_norms * query_norm + 1e-10
    )

    return similarities.tolist()


async def match_skills_semantically(
    skills_not_found: list[dict],
    resume_text: str
) -> dict:

    if not skills_not_found:
        return {
            "results": [],
            "semantic_matches": [],
            "missing_skills": []
        }

    chunks = split_resume_into_chunks(resume_text)

    if not chunks:
        return {
            "results": [],
            "semantic_matches": [],
            "missing_skills": skills_not_found
        }

    skills = [item["skill"] for item in skills_not_found]

    # Generate all embeddings in one API request.
    texts_to_embed = (
        [f"Skill: {skill}" for skill in skills] + chunks
    )

    embeddings = await embedding_service.generate_embeddings(
        texts_to_embed
    )

    skill_embeddings = embeddings[:len(skills)]
    chunk_embeddings = embeddings[len(skills):]

    results = []

    for index, skill in enumerate(skills):
        similarities = calculate_cosine_similarity(
            skill_embeddings[index],
            chunk_embeddings
        )

        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])

        found = best_score >= SEMANTIC_THRESHOLD

        results.append({
            "skill": skill,
            "found": found,
            "method": "semantic" if found else None,
            "similarity": round(best_score, 4),
            "evidence": chunks[best_index] if found else None
        })

    semantic_matches = [
        item for item in results if item["found"]
    ]

    missing_skills = [
        item for item in results if not item["found"]
    ]

    return {
        "results": results,
        "semantic_matches": semantic_matches,
        "missing_skills": missing_skills
    }
