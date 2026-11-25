# # import numpy as np

# # from app.services.embedding_service import embedding_service


# # EXPERIENCE_QUERIES = [
# #     "Work experience",
# #     "Professional experience",
# #     "Years of experience",
# #     "Internship experience",
# #     "Employment history",
# #     "Previous jobs",
# #     "Work duration",
# #     "Employment start and end dates",
# #     "Worked at an organization",
# #     "Currently working"
# # ]

# # SEMANTIC_THRESHOLD = 0.65
# # WORDS_BEFORE = 20
# # WORDS_AFTER = 200


# # def calculate_cosine_similarity(query_embedding, chunk_embeddings):
# #     query_vector = np.array(query_embedding, dtype=float)
# #     chunk_vectors = np.array(chunk_embeddings, dtype=float)

# #     query_norm = np.linalg.norm(query_vector)
# #     chunk_norms = np.linalg.norm(chunk_vectors, axis=1)

# #     if query_norm == 0:
# #         return [0.0] * len(chunk_embeddings)

# #     similarities = np.dot(chunk_vectors, query_vector) / (
# #         chunk_norms * query_norm + 1e-10
# #     )

# #     return similarities.tolist()


# # def extract_context(text: str, start: int, end: int) -> str:
# #     words = text.split()

# #     before_start = max(0, start - WORDS_BEFORE)
# #     after_end = min(len(words), end + WORDS_AFTER)

# #     return " ".join(words[before_start:after_end])


# # async def search_experience_context(resume_text: str) -> dict:

# #     if not resume_text or not resume_text.strip():
# #         return {
# #             "total_matches": 0,
# #             "contexts": []
# #         }

# #     words = resume_text.split()

# #     # Create word-based chunks for semantic searching.
# #     chunk_size = 150
# #     overlap = 30

# #     chunks = []

# #     for start in range(0, len(words), chunk_size - overlap):
# #         end = min(start + chunk_size, len(words))

# #         chunk_text = " ".join(words[start:end])

# #         chunks.append({
# #             "start": start,
# #             "end": end,
# #             "text": chunk_text
# #         })

# #         if end == len(words):
# #             break

# #     texts_to_embed = EXPERIENCE_QUERIES + [
# #         chunk["text"] for chunk in chunks
# #     ]

# #     embeddings = await embedding_service.generate_embeddings(
# #         texts_to_embed
# #     )

# #     query_embeddings = embeddings[:len(EXPERIENCE_QUERIES)]
# #     chunk_embeddings = embeddings[len(EXPERIENCE_QUERIES):]

# #     matches = []

# #     for query_index, query in enumerate(EXPERIENCE_QUERIES):

# #         similarities = calculate_cosine_similarity(
# #             query_embeddings[query_index],
# #             chunk_embeddings
# #         )

# #         best_index = int(np.argmax(similarities))
# #         best_score = float(similarities[best_index])
# #         print(f"\nQuery: {query}")
# #         print(f"Best similarity: {best_score:.4f}")
# #         if best_score >= SEMANTIC_THRESHOLD:

# #             chunk = chunks[best_index]

# #             context = extract_context(
# #                 resume_text,
# #                 chunk["start"],
# #                 chunk["end"]
# #             )

# #             matches.append({
# #                 "query": query,
# #                 "similarity": round(best_score, 4),
# #                 "context": context
# #             })

# #     return {
# #         "total_matches": len(matches),
# #         "contexts": matches
# #     }



















# # version 2
# import numpy as np

# from app.services.embedding_service import embedding_service


# EXPERIENCE_QUERIES = [
#     "Work experience",
#     "Professional experience",
#     "Years of experience",
#     "Internship experience",
#     "Employment history",
#     "Previous jobs",
#     "Work duration",
#     "Employment start and end dates",
#     "Worked at an organization",
#     "Currently working"
# ]

# WORDS_BEFORE = 20
# WORDS_AFTER = 200

# CHUNK_SIZE = 60
# CHUNK_OVERLAP = 15
# TOP_K = 3


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


# def extract_context(text: str, start: int, end: int) -> str:
#     words = text.split()

#     before_start = max(0, start - WORDS_BEFORE)
#     after_end = min(len(words), end + WORDS_AFTER)

#     return " ".join(words[before_start:after_end])


# async def search_experience_context(resume_text: str) -> dict:

#     if not resume_text or not resume_text.strip():
#         return {
#             "total_matches": 0,
#             "contexts": []
#         }

#     words = resume_text.split()

#     # Divide resume into overlapping chunks.
#     chunks = []

#     step = CHUNK_SIZE - CHUNK_OVERLAP

#     for start in range(0, len(words), step):

#         end = min(start + CHUNK_SIZE, len(words))

#         chunks.append({
#             "start": start,
#             "end": end,
#             "text": " ".join(words[start:end])
#         })

#         if end == len(words):
#             break

#     # Generate embeddings in one API request.
#     texts_to_embed = EXPERIENCE_QUERIES + [
#         chunk["text"] for chunk in chunks
#     ]

#     embeddings = await embedding_service.generate_embeddings(
#         texts_to_embed
#     )

#     query_embeddings = embeddings[:len(EXPERIENCE_QUERIES)]
#     chunk_embeddings = embeddings[len(EXPERIENCE_QUERIES):]

#     matches = []

#     for query_index, query in enumerate(EXPERIENCE_QUERIES):

#         similarities = calculate_cosine_similarity(
#             query_embeddings[query_index],
#             chunk_embeddings
#         )

#         top_indices = np.argsort(similarities)[::-1][:TOP_K]

#         print(f"\nQuery: {query}")

#         for rank, index in enumerate(top_indices, start=1):

#             score = float(similarities[index])

#             print(f"\nRank: {rank}")
#             print(f"Similarity: {score:.4f}")
#             print(f"Chunk: {chunks[index]['text']}")

#             context = extract_context(
#                 resume_text,
#                 chunks[index]["start"],
#                 chunks[index]["end"]
#             )

#             matches.append({
#                 "query": query,
#                 "rank": rank,
#                 "similarity": round(score, 4),
#                 "context": context
#             })

#     return {
#         "total_matches": len(matches),
#         "contexts": matches
#     }






















# version 3

# import numpy as np

# from app.services.embedding_service import embedding_service


# # EXPERIENCE_QUERIES = [
# #     "Work experience",
# #     "Professional experience",
# #     "Years of experience",
# #     "Internship experience",
# #     "Employment history",
# #     "Previous jobs",
# #     "Work duration",
# #     "Employment start and end dates",
# #     "Worked at an organization",
# #     "Currently working"
# # ]
# EXPERIENCE_QUERIES = [
#     "Work experience"   
# ]

# CHUNK_SIZE = 60
# CHUNK_OVERLAP = 15
# TOP_K = 3

# WORDS_BEFORE = 20
# WORDS_AFTER = 200


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


# def search_and_collect_chunks(
#     query_embeddings,
#     chunk_embeddings,
#     chunks
# ):
#     selected_chunks = {}

#     for query_index, query in enumerate(EXPERIENCE_QUERIES):

#         similarities = calculate_cosine_similarity(
#             query_embeddings[query_index],
#             chunk_embeddings
#         )

#         top_indices = np.argsort(similarities)[::-1][:TOP_K]

#         print(f"\nQuery: {query}")

#         for index in top_indices:

#             score = float(similarities[index])

#             print(
#                 f"Chunk {index} | Similarity: {score:.4f}"
#             )

#             if index not in selected_chunks:
#                 selected_chunks[index] = {
#                     "chunk_index": int(index),
#                     "similarity": score,
#                     "matched_queries": [query]
#                 }
#             else:
#                 selected_chunks[index]["similarity"] = max(
#                     selected_chunks[index]["similarity"],
#                     score
#                 )

#                 selected_chunks[index]["matched_queries"].append(
#                     query
#                 )

#     return list(selected_chunks.values())


# def merge_contexts(selected_chunks, words):

#     regions = []

#     # Create context windows around selected chunks.
#     for item in selected_chunks:

#         chunk = item["chunk_index"]

#         # Chunk positions are stored separately below.
#         start = item["start"]
#         end = item["end"]

#         context_start = max(0, start - WORDS_BEFORE)
#         context_end = min(len(words), end + WORDS_AFTER)

#         regions.append({
#             "start": context_start,
#             "end": context_end,
#             "similarity": item["similarity"],
#             "matched_queries": item["matched_queries"],
#             "chunk_indexes": [chunk]
#         })

#     # Sort regions by their original resume positions.
#     regions.sort(key=lambda item: item["start"])

#     merged = []

#     for region in regions:

#         if not merged or region["start"] > merged[-1]["end"]:

#             merged.append(region.copy())

#         else:
#             current = merged[-1]

#             current["end"] = max(
#                 current["end"],
#                 region["end"]
#             )

#             current["similarity"] = max(
#                 current["similarity"],
#                 region["similarity"]
#             )

#             current["matched_queries"].extend(
#                 region["matched_queries"]
#             )

#             current["chunk_indexes"].extend(
#                 region["chunk_indexes"]
#             )

#     # Build final text contexts.
#     contexts = []

#     for index, region in enumerate(merged):

#         contexts.append({
#             "context_id": index,
#             "similarity": round(region["similarity"], 4),
#             "matched_queries": list(
#                 dict.fromkeys(region["matched_queries"])
#             ),
#             "chunk_indexes": sorted(
#                 set(region["chunk_indexes"])
#             ),
#             "context": " ".join(
#                 words[region["start"]:region["end"]]
#             )
#         })

#     return contexts


# async def search_experience_context(resume_text: str) -> dict:

#     if not resume_text or not resume_text.strip():
#         return {
#             "total_matches": 0,
#             "contexts": []
#         }

#     words = resume_text.split()

#     chunks = []

#     step = CHUNK_SIZE - CHUNK_OVERLAP

#     for start in range(0, len(words), step):

#         end = min(start + CHUNK_SIZE, len(words))

#         chunks.append({
#             "start": start,
#             "end": end,
#             "text": " ".join(words[start:end])
#         })

#         if end == len(words):
#             break

#     texts_to_embed = EXPERIENCE_QUERIES + [
#         chunk["text"] for chunk in chunks
#     ]

#     embeddings = await embedding_service.generate_embeddings(
#         texts_to_embed
#     )

#     query_embeddings = embeddings[:len(EXPERIENCE_QUERIES)]
#     chunk_embeddings = embeddings[len(EXPERIENCE_QUERIES):]

#     selected_chunks = search_and_collect_chunks(
#         query_embeddings,
#         chunk_embeddings,
#         chunks
#     )

#     # Attach original word positions to selected chunks.
#     for item in selected_chunks:

#         chunk = chunks[item["chunk_index"]]

#         item["start"] = chunk["start"]
#         item["end"] = chunk["end"]

#     contexts = merge_contexts(selected_chunks, words)

#     return {
#         "total_matches": len(contexts),
#         "contexts": contexts
#     }














# version 4
import numpy as np

from app.services.embedding_service import embedding_service


EXPERIENCE_QUERY = "Work experience"

CHUNK_SIZE =150
CHUNK_OVERLAP = 20
TOP_K = 3


def create_resume_chunks(
    resume_text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> list[dict]:
    """
    Split resume text into overlapping word-based chunks.
    """

    if not resume_text or not resume_text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    words = resume_text.split()
    step = chunk_size - overlap

    chunks = []

    for start in range(0, len(words), step):
        end = min(start + chunk_size, len(words))

        chunk_text = " ".join(words[start:end])

        chunks.append({
            "chunk_id": len(chunks),
            "start": start,
            "end": end,
            "text": chunk_text
        })

        if end == len(words):
            break

    return chunks


def calculate_cosine_similarities(
    query_embedding: list[float],
    chunk_embeddings: list[list[float]]
) -> list[float]:
    """
    Calculate cosine similarity between the query and each chunk.
    """

    query_vector = np.array(query_embedding, dtype=float)
    chunk_vectors = np.array(chunk_embeddings, dtype=float)

    query_norm = np.linalg.norm(query_vector)
    chunk_norms = np.linalg.norm(chunk_vectors, axis=1)

    if query_norm == 0:
        return [0.0] * len(chunk_embeddings)

    similarities = np.dot(
        chunk_vectors,
        query_vector
    ) / (chunk_norms * query_norm + 1e-10)

    return similarities.tolist()


async def search_experience_chunks(resume_text: str) -> dict:
    """
    Retrieve the top 3 resume chunks relevant to work experience.
    """

    chunks = create_resume_chunks(resume_text)

    if not chunks:
        return {
            "query": EXPERIENCE_QUERY,
            "total_chunks": 0,
            "total_matches": 0,
            "contexts": []
        }

    # Generate embeddings for the query and all resume chunks.
    texts_to_embed = [
        EXPERIENCE_QUERY
    ] + [
        chunk["text"] for chunk in chunks
    ]

    embeddings = await embedding_service.generate_embeddings(
        texts_to_embed
    )

    query_embedding = embeddings[0]
    chunk_embeddings = embeddings[1:]

    # Calculate similarity between the query and every chunk.
    similarities = calculate_cosine_similarities(
        query_embedding,
        chunk_embeddings
    )

    # Select the three most relevant chunks.
    top_indices = np.argsort(similarities)[::-1][:TOP_K]

    # Preserve original resume order when sending chunks to the LLM.
    selected_chunks = sorted(
        top_indices,
        key=lambda index: chunks[index]["start"]
    )

    contexts = []

    for index in selected_chunks:
        contexts.append({
            "chunk_id": chunks[index]["chunk_id"],
            "rank": int(
                np.where(top_indices == index)[0][0] + 1
            ),
            "similarity": round(float(similarities[index]), 4),
            "text": chunks[index]["text"]
        })

    return {
        "query": EXPERIENCE_QUERY,
        "total_chunks": len(chunks),
        "total_matches": len(contexts),
        "contexts": contexts
    }
