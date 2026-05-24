import fitz

from fastapi import UploadFile


class PDFInspector:
    async def inspect(self, file: UploadFile, max_pages: int = 100, max_size: int = 50 * 1024 * 1024) -> dict:
        content = await file.read()
        size = len(content)

        if size == 0:
            raise ValueError("Empty file")

        if size > max_size:
            raise ValueError(f"File too large: {size} bytes")

        doc = None

        try:
            doc = fitz.open(stream=content, filetype="pdf")
            page_count = len(doc)

            if page_count == 0:
                raise ValueError("Empty PDF")

            if page_count > max_pages:
                raise ValueError(f"Too many pages: {page_count}")

            return {
                "content": content,
                "page_count": page_count,
                "file_size": size,
                "filename": file.filename,
            }

        finally:
            if doc is not None:
                doc.close()
