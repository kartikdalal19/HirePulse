
import fitz


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""

    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        for page in document:
            text_parts.append(page.get_text("text"))

    extracted_text = "\n".join(text_parts).strip()

    if not extracted_text:
        raise ValueError(
            "No readable text found. The PDF may be scanned or image-based."
        )

    return extracted_text
