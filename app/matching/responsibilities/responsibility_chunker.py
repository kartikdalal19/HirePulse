
# import re


# def split_resume_into_chunks(
#     resume_text: str,
#     max_chunk_size: int = 500
# ) -> list[str]:
#     """
#     Split resume text into meaningful chunks.

#     First split by paragraphs, then split long paragraphs
#     into smaller sentence-based chunks.
#     """

#     if not resume_text or not resume_text.strip():
#         return []

#     # Split text into paragraphs
#     paragraphs = [
#         paragraph.strip()
#         for paragraph in re.split(r"\n+", resume_text)
#         if paragraph.strip()
#     ]

#     chunks = []

#     for paragraph in paragraphs:

#         # Keep short paragraphs as individual chunks
#         if len(paragraph) <= max_chunk_size:
#             chunks.append(paragraph)
#             continue

#         # Split long paragraphs into sentences
#         sentences = re.split(
#             r"(?<=[.!?])\s+",
#             paragraph
#         )

#         current_chunk = ""

#         for sentence in sentences:

#             if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:

#                 current_chunk = (
#                     f"{current_chunk} {sentence}".strip()
#                 )

#             else:

#                 if current_chunk:
#                     chunks.append(current_chunk)

#                 current_chunk = sentence

#         if current_chunk:
#             chunks.append(current_chunk)

#     return chunks




import re

MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_resume_into_chunks(
    resume_text: str,
    max_chunk_size: int = MAX_CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> list[dict]:

    if not resume_text or not resume_text.strip():
        return []

    if overlap >= max_chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    # Normalize line breaks and whitespace.
    text = re.sub(r"\r\n?", "\n", resume_text)
    paragraphs = re.split(r"\n\s*\n+", text)

    chunks = []

    for paragraph in paragraphs:
        paragraph = re.sub(r"\s+", " ", paragraph).strip()

        if not paragraph:
            continue

        # Keep short paragraphs intact.
        if len(paragraph) <= max_chunk_size:
            chunks.append(paragraph)
            continue

        # Split long paragraphs into sentences.
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)

        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            # Handle sentences longer than the chunk limit.
            if len(sentence) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                start = 0

                while start < len(sentence):
                    end = min(start + max_chunk_size, len(sentence))

                    if end < len(sentence):
                        boundary = sentence.rfind(" ", start, end)
                        if boundary > start:
                            end = boundary

                    chunks.append(sentence[start:end].strip())

                    if end >= len(sentence):
                        break

                    start = max(start + 1, end - overlap)

                continue

            candidate = f"{current_chunk} {sentence}".strip()

            if len(candidate) <= max_chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                # Carry a small amount of context into the next chunk.
                previous_context = current_chunk[-overlap:].strip()
                current_chunk = f"{previous_context} {sentence}".strip()

                if len(current_chunk) > max_chunk_size:
                    current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

    return [
        {
            "chunk_id": index,
            "text": chunk
        }
        for index, chunk in enumerate(chunks)
    ]
