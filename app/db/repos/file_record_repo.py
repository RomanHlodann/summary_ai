from sqlalchemy import select, update

from app.db.models.file_record import FileRecord, FileStatus


class FileRepository:
    def __init__(self, session):
        self.session = session

    async def create(
        self,
        file_name: str,
        file_size: int,
    ) -> FileRecord:
        record = FileRecord(
            file_name=file_name,
            file_size=file_size,
            status=FileStatus.pending,
        )

        self.session.add(record)

        await self.session.commit()
        await self.session.refresh(record)

        return record

    async def get_by_id(self, file_id: int) -> FileRecord | None:
        return await self.session.get(FileRecord, file_id)

    async def update(
        self,
        file_id: int,
        **fields,
    ) -> None:
        record = await self.get_by_id(file_id)

        if not record:
            return

        for key, value in fields.items():
            setattr(record, key, value)

        await self.session.commit()

    async def mark_processing(self, file_id: int):
        await self.update(
            file_id,
            status=FileStatus.processing,
        )

    async def mark_done(
        self,
        file_id: int,
        summary: str,
        page_count: int,
    ):
        await self.update(
            file_id,
            status=FileStatus.done,
            result=summary,
            page_count=page_count,
        )

    async def mark_failed(
        self,
        file_id: int,
        error: str,
    ):
        await self.update(
            file_id,
            status=FileStatus.failed,
            error=error,
        )

    async def get_last(
        self,
        limit: int = 5,
    ) -> list[FileRecord]:
        stmt = (
            select(FileRecord)
            .order_by(FileRecord.created_at.desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()
