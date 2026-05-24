import pdfplumber


class TableExtractor:
    def extract(self, page: pdfplumber.page.Page) -> str:
        tables = page.extract_tables()
        if not tables:
            return ""
        return "\n\n".join(
            self._to_markdown(table)
            for table in tables
            if table
        )

    def _to_markdown(self, table: list[list[str | None]]) -> str:
        def fmt(row: list[str | None]) -> str:
            return "| " + " | ".join(str(cell or "") for cell in row) + " |"

        header, *rows = table
        separator = "| " + " | ".join("---" for _ in header) + " |"
        return "\n".join([fmt(header), separator, *map(fmt, rows)])
