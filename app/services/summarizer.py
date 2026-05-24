from __future__ import annotations

import asyncio
import logging

from app.services.openai import OpenAIClient
from app.utils.prompts import CHUNK_SYSTEM, FINAL_SYSTEM


logger = logging.getLogger(__name__)

CHUNK_MODEL = "gpt-4o-mini"
FINAL_MODEL = "gpt-4o-mini"


class Summarizer:
    def __init__(self, client: OpenAIClient) -> None:
        self._client = client

    async def summarize(self, chunks: list[str]) -> str:
        chunk_summaries = await self._map(chunks)
        return await self._reduce(chunk_summaries)

    async def _map(self, chunks: list[str]) -> list[str]:
        results = await asyncio.gather(
            *[self._summarize_chunk(chunk) for chunk in chunks],
            return_exceptions=True,
        )
        summaries = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning("Chunk %d summarization failed: %s", i, result)
                summaries.append(f"[Chunk {i + 1} failed to summarize]")
            else:
                summaries.append(result)
        return summaries

    async def _reduce(self, chunk_summaries: list[str]) -> str:
        combined = "\n\n".join(
            f"[Chunk {i + 1}]\n{s}" for i, s in enumerate(chunk_summaries)
        )
        return await self._client.complete(
            model=FINAL_MODEL,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": FINAL_SYSTEM},
                {"role": "user", "content": combined},
            ],
        )

    async def _summarize_chunk(self, chunk: str) -> str:
        return await self._client.complete(
            model=CHUNK_MODEL,
            max_tokens=300,
            messages=[
                {"role": "system", "content": CHUNK_SYSTEM},
                {"role": "user", "content": chunk},
            ],
        )
