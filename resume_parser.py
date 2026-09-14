"""Safe PDF text extraction for uploaded resumes."""

from io import BytesIO

import fitz


def extract_resume_text(uploaded_file) -> dict:
    """Extract all page text from an uploaded PDF without raising UI-breaking errors."""
    filename = getattr(uploaded_file, "name", "Unnamed resume.pdf")
    try:
        document = fitz.open(stream=BytesIO(uploaded_file.getvalue()), filetype="pdf")
        text = "\n".join(page.get_text("text") for page in document).strip()
        document.close()
        if not text:
            return {"filename": filename, "extracted_text": "", "status": "No extractable text"}
        return {"filename": filename, "extracted_text": text, "status": "Ready"}
    except (fitz.FileDataError, RuntimeError, ValueError):
        return {"filename": filename, "extracted_text": "", "status": "Invalid or unreadable PDF"}
    except Exception:
        return {"filename": filename, "extracted_text": "", "status": "Could not process PDF"}
