from dataclasses import dataclass, field


@dataclass
class PageResult:
    page_num: int
    text: str = ""
    tables_md: str = ""
    vision_caption: str | None = None

    def to_text_block(self) -> str:
        parts = [f"--- Page {self.page_num} ---"]
        if self.text:
            parts.append(self.text)
        if self.tables_md:
            parts.append(f"[TABLES]\n{self.tables_md}")
        if self.vision_caption:
            parts.append(f"[IMAGE DESCRIPTION]\n{self.vision_caption}")
        return "\n".join(parts)


@dataclass
class ParsedDocument:
    filename: str
    pages: list[PageResult] = field(default_factory=list)

    @property
    def total_pages(self) -> int:
        return len(self.pages)

    @property
    def image_heavy_pages(self) -> list[int]:
        return [p.page_num for p in self.pages if p.vision_caption is not None]

    def to_chunks(self, max_chars: int = 12000) -> list[str]:
        chunks = []
        current_chunk = []
        current_size = 0

        for page in self.pages:
            text = page.to_text_block()

            if current_size + len(text) > max_chars and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(text)
            current_size += len(text)

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks
