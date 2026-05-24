import fitz


class TextExtractor:
    def extract(self, page: fitz.Page) -> str:
        return page.get_text("text").strip()
