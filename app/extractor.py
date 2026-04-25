from io import BytesIO
from pypdf import PdfReader


def extract_text(filename: str, content: bytes) -> str:
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext == 'pdf':
        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or '' for page in reader.pages]
        text = '\n'.join(pages).strip()
        if not text:
            raise ValueError("No extractable text found in PDF (may be scanned/image-based)")
        return text
    if ext == 'txt':
        return content.decode('utf-8', errors='replace').strip()
    raise ValueError(f"Unsupported file type: .{ext}")
