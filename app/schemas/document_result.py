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

    def to_chunks(self, pages_per_chunk: int = 10) -> list[str]:
        return [
            "\n\n".join(p.to_text_block() for p in self.pages[i : i + pages_per_chunk])
            for i in range(0, len(self.pages), pages_per_chunk)
        ]
