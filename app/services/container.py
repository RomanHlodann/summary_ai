from fastapi import Request, Depends

from app.services.inspector import PDFInspector
from app.services.parser import PDFParser
from app.services.summarizer import Summarizer
from app.services.processor import PDFProcessingService
from app.db.repos.file_record_repo import FileRepository
from app.db.session import get_session


class Container:
    def __init__(self, client, session):
        self.inspector = PDFInspector()
        self.parser = PDFParser(client)
        self.summarizer = Summarizer(client)

        self.repo = FileRepository(session)

        self.processor = PDFProcessingService(
            parser=self.parser,
            summarizer=self.summarizer,
            repo=self.repo,
        )


def get_container(request: Request, session = Depends(get_session)) -> Container:
    client = request.app.state.openai_client

    return Container(client=client, session=session)
