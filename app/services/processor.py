import logging

logger = logging.getLogger(__name__)


class PDFProcessingService:
    def __init__(self, parser, summarizer, repo):
        self._parser = parser
        self._summarizer = summarizer
        self._repo = repo

    async def process(self, file_id: int, content: bytes, filename: str):
        await self._repo.mark_processing(file_id)

        try:
            logger.info("Start processing file_id=%s filename=%s", file_id, filename)

            doc = await self._parser.parse(content, filename)

            if doc.total_pages == 0:
                raise ValueError("No pages extracted from PDF")

            logger.info(
                "Parsed file_id=%s pages=%s",
                file_id,
                doc.total_pages,
            )

            summary = await self._summarizer.summarize(doc.to_chunks())

            await self._repo.mark_done(
                file_id=file_id,
                summary=summary,
                page_count=doc.total_pages,
            )

            logger.info("Completed file_id=%s", file_id)

        except Exception as e:
            logger.exception("Processing failed file_id=%s", file_id)

            await self._repo.mark_failed(
                file_id=file_id,
                error=str(e),
            )
