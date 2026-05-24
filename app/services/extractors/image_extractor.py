from __future__ import annotations

import base64

import fitz

from app.services.openai import OpenAIClient

RENDER_DPI = 150
VISION_MODEL = "gpt-4o"
VISION_PROMPT = (
    "Describe the content of this document page concisely. "
    "Include any text, tables, charts, or diagrams you see. "
    "Focus on information content, not layout."
)


class VisionExtractor:
    def __init__(self, client: OpenAIClient) -> None:
        self._client = client

    async def extract(self, page: fitz.Page) -> str:
        b64 = self._render(page)
        return await self._client.complete(
            model=VISION_MODEL,
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64}",
                            "detail": "high",
                        },
                    },
                    {"type": "text", "text": VISION_PROMPT},
                ],
            }],
        )

    def _render(self, page: fitz.Page) -> str:
        scale = RENDER_DPI / 72.0
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        return base64.b64encode(pix.tobytes("png")).decode()
