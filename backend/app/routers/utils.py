from typing import BinaryIO

from fastapi import UploadFile

from app.services.FileService.IFileWrapper import IFileWrapper


class FileWrapper(IFileWrapper):
    __file: UploadFile

    def __init__(self, file: UploadFile) -> None:
        self.__file = file

    async def read(self) -> bytes:
        await self.__file.seek(0)
        return await self.__file.read()

    @property
    def content_type(self) -> str | None:
        return self.__file.content_type

    @property
    def filename(self) -> str | None:
        return self.__file.filename

    @property
    def file(self) -> BinaryIO:
        return self.__file.file
