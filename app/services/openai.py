import os

from openai import AsyncOpenAI
from typing import Any

from app.utils.retry import with_retry


class OpenAIClient:
    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self._client = AsyncOpenAI(api_key=key)
 
    @with_retry()
    async def complete(
        self,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
    ) -> str:
        response = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
