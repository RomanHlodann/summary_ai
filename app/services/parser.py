from __future__ import annotations

import io
import fitz
import asyncio
import logging
import pdfplumber

from app.services.openai import OpenAIClient
from app.services.extractors.text_extractor import TextExtractor
from app.services.extractors.table_extractor import TableExtractor
from app.services.extractors.image_extractor import VisionExtractor
from app.schemas.document_result import PageResult, ParsedDocument


logger = logging.getLogger(__name__)

TEXT_YIELD_THRESHOLD = 100


class PDFParser:
    def __init__(self, client: OpenAIClient) -> None:
        self._text = TextExtractor()
        self._tables = TableExtractor()
        self._vision = VisionExtractor(client)
 
    async def parse(self, pdf_bytes: bytes, filename: str = "") -> ParsedDocument:
        doc = ParsedDocument(filename=filename)
        fitz_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as plumber_doc:
                pages = await asyncio.gather(*[
                    self._parse_page(fitz_doc[i], plumber_doc.pages[i], page_num=i + 1)
                    for i in range(len(fitz_doc))
                ])
            doc.pages = list(pages)
        finally:
            fitz_doc.close()
 
        logger.info(
            "Parsed '%s': %d pages, %d image-heavy",
            filename, doc.total_pages, len(doc.image_heavy_pages),
        )
        return doc

    async def _parse_page(
        self,
        fitz_page: fitz.Page,
        plumber_page: pdfplumber.page.Page,
        page_num: int,
    ) -> PageResult:

        result = PageResult(page_num=page_num)

        try:
            text = self._text.extract(fitz_page)
            result.text = text
            result.tables_md = self._tables.extract(plumber_page)
        except Exception as exc:
            logger.warning("Page %d: extraction failed: %s", page_num, exc)
            text = ""

        has_images = bool(fitz_page.get_images(full=True))
        text_len = len(text.strip())
        low_text = text_len < 300
        should_use_vision = has_images and low_text

        if should_use_vision:
            try:
                result.vision_caption = await self._vision.extract(fitz_page)
            except Exception as exc:
                logger.warning("Page %d: vision failed: %s", page_num, exc)

        return result
