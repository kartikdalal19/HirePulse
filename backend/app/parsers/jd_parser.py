
from io import BytesIO

import fitz
from docx import Document


def extract_jd_file(filename: str, file_bytes: bytes) -> str:

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":

        document = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        try:
            pages = [
                page.get_text("text")
                for page in document
            ]
            text = "\n".join(pages)
        finally:
            document.close()

    elif extension == "docx":

        document = Document(BytesIO(file_bytes))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        text = "\n".join(paragraphs)

        # Also extract text from tables.
        for table in document.tables:
            for row in table.rows:
                text += "\n" + " | ".join(
                    cell.text.strip() for cell in row.cells
                )

    else:
        raise ValueError("Only PDF and DOCX files are supported")

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found. The document may be scanned."
        )

    return text
