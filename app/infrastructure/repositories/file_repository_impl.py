from app.domain.entities.file import File
from app.domain.repositories.file_repository import FileRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Optional, List

class FileRepositoryImpl(FileRepository):
    def _to_entity(self, db_file) -> File:
        return File(
            id=db_file.id,
            name=db_file.name,
            mimeType=db_file.mimeType,
            driveFileId=db_file.driveFileId,
            url=db_file.url,
            uploadedAt=db_file.uploadedAt,
            createdAt=db_file.createdAt,
            uploadedById=db_file.uploadedById,
            fileableId=db_file.fileableId,
            fileableType=db_file.fileableType
        )

    async def create(self, file: File) -> File:
        db_file = await prisma_client.client.file.create(data=file.__dict__)
        return self._to_entity(db_file)

    async def get_by_id(self, file_id: str) -> Optional[File]:
        db_file = await prisma_client.client.file.find_unique(where={"id": file_id})
        if db_file:
            return self._to_entity(db_file)
        return None

    async def list_by_user(self, userId: str) -> List[File]:
        db_files = await prisma_client.client.file.find_many(where={"uploadedById": userId})
        return [self._to_entity(f) for f in db_files]

    async def update(self, file_id: str, updates: dict) -> File:
        db_file = await prisma_client.client.file.update(where={'id': file_id}, data=updates)
        return self._to_entity(db_file)
