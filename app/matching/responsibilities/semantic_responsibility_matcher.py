
# import numpy as np

# from app.services.embedding_service import embedding_service
# from app.matching.responsibilities.responsibility_chunker import (
#     split_resume_into_chunks
# )

# SEMANTIC_THRESHOLD = 0.6


# def calculate_cosine_similarity(query_embedding, chunk_embeddings):
#     query_vector = np.array(query_embedding, dtype=float)
#     chunk_vectors = np.array(chunk_embeddings, dtype=float)

#     query_norm = np.linalg.norm(query_vector)
#     chunk_norms = np.linalg.norm(chunk_vectors, axis=1)

#     if query_norm == 0:
#         return [0.0] * len(chunk_embeddings)

#     similarities = np.dot(chunk_vectors, query_vector) / (
#         chunk_norms * query_norm + 1e-10
#     )

#     return similarities.tolist()


# async def match_responsibilities_semantically(
#     responsibilities: list[str],
#     resume_text: str
# ) -> dict:

#     if not responsibilities:
#         return {
#             "total_responsibilities": 0,
#             "results": []
#         }

#     chunks = split_resume_into_chunks(resume_text)

#     if not chunks:
#         return {
#             "total_responsibilities": len(responsibilities),
#             "results": [
#                 {
#                     "responsibility": responsibility,
#                     "found": False,
#                     "similarity": 0.0,
#                     "evidence": None,
#                     "chunk_id": None
#                 }
#                 for responsibility in responsibilities
#             ]
#         }

#     # Prepare all texts for a single embedding API request.
#     texts_to_embed = (
#         [f"Job responsibility: {item}" for item in responsibilities]
#         + [chunk["text"] for chunk in chunks]
#     )

#     embeddings = await embedding_service.generate_embeddings(texts_to_embed)

#     responsibility_embeddings = embeddings[:len(responsibilities)]
#     chunk_embeddings = embeddings[len(responsibilities):]

#     results = []

#     for index, responsibility in enumerate(responsibilities):

#         similarities = calculate_cosine_similarity(
#             responsibility_embeddings[index],
#             chunk_embeddings
#         )

#         best_index = int(np.argmax(similarities))
#         best_score = float(similarities[best_index])

#         found = best_score >= SEMANTIC_THRESHOLD

#         results.append({
#             "responsibility": responsibility,
#             "found": found,
#             "similarity": round(best_score, 4),
#             "evidence": chunks[best_index]["text"] if found else None,
#             "chunk_id": chunks[best_index]["chunk_id"] if found else None
#         })

#     return {
#         "total_responsibilities": len(responsibilities),
#         "results": results
#     }






import numpy as np

from app.services.embedding_service import embedding_service
from app.matching.responsibilities.responsibility_chunker import (
    split_resume_into_chunks
)

SEMANTIC_THRESHOLD = 0.6
TOP_K_CHUNKS = 3


def calculate_cosine_similarity(query_embedding, chunk_embeddings):
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


async def match_responsibilities_semantically(
    responsibilities: list[str],
    resume_text: str
) -> dict:

    if not responsibilities:
        return {
            "total_responsibilities": 0,
            "results": []
        }

    chunks = split_resume_into_chunks(resume_text)

    if not chunks:
        return {
            "total_responsibilities": len(responsibilities),
            "results": [
                {
                    "responsibility": responsibility,
                    "found": False,
                    "similarity": 0.0,
                    "evidence": None,
                    "chunk_id": None,
                    "chunk_ids": []
                }
                for responsibility in responsibilities
            ]
        }

    # Prepare all texts for a single embedding API request.
    texts_to_embed = (
        [f"Job responsibility: {item}" for item in responsibilities]
        + [chunk["text"] for chunk in chunks]
    )

    embeddings = await embedding_service.generate_embeddings(texts_to_embed)

    responsibility_embeddings = embeddings[:len(responsibilities)]
    chunk_embeddings = embeddings[len(responsibilities):]

    results = []

    for index, responsibility in enumerate(responsibilities):

        similarities = calculate_cosine_similarity(
            responsibility_embeddings[index],
            chunk_embeddings
        )

        # Sort chunk indices by descending similarity.
        ranked_indices = np.argsort(similarities)[::-1]

        # Keep only chunks that pass the semantic threshold.
        qualifying_indices = [
            int(chunk_index)
            for chunk_index in ranked_indices
            if similarities[chunk_index] >= SEMANTIC_THRESHOLD
        ]

        # Retrieve the top K qualifying chunks.
        selected_indices = qualifying_indices[:TOP_K_CHUNKS]

        found = len(selected_indices) > 0

        if found:

            selected_chunks = [
                {
                    "chunk_id": chunks[chunk_index]["chunk_id"],
                    "similarity": round(
                        float(similarities[chunk_index]), 4
                    ),
                    "text": chunks[chunk_index]["text"]
                }
                for chunk_index in selected_indices
            ]

            # Combine the retrieved evidence for LLM verification.
            combined_evidence = "\n\n".join(
                f"[Chunk {item['chunk_id']} | "
                f"Similarity: {item['similarity']}]\n"
                f"{item['text']}"
                for item in selected_chunks
            )

            best_score = float(similarities[selected_indices[0]])
            best_chunk_id = chunks[selected_indices[0]]["chunk_id"]

        else:

            selected_chunks = []
            combined_evidence = None

            best_index = int(np.argmax(similarities))
            best_score = float(similarities[best_index])
            best_chunk_id = chunks[best_index]["chunk_id"]

        results.append({
            "responsibility": responsibility,
            "found": found,
            "similarity": round(best_score, 4),
            "evidence": combined_evidence,
            "chunk_id": best_chunk_id,
            "chunk_ids": [
                item["chunk_id"] for item in selected_chunks
            ],
            "evidence_chunks": selected_chunks
        })

    return {
        "total_responsibilities": len(responsibilities),
        "results": results
    }