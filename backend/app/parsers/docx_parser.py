
from io import BytesIO
from docx import Document


def extract_docx_text(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""

    document = Document(BytesIO(file_bytes))

    text_parts = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text.strip())

    # Extract tables
    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if cells:
                text_parts.append(" | ".join(cells))

    extracted_text = "\n".join(text_parts).strip()

    if not extracted_text:
        raise ValueError("No readable text found in DOCX file.")

    return extracted_text
