from os import listdir, mkdir, path, remove, rmdir
from re import Pattern

import filetype  # type: ignore

from app.config import settings

from ..exceptions import FileDoesNotExistError, FileTooBigError, InvalidFileFormatError
from .IFileService import IFileService
from .IFileWrapper import IFileWrapper


class FileService(IFileService):

    async def add_file(
        self,
        file: IFileWrapper,
        allowed_formats: Pattern,
        file_name: str,
    ) -> None:

        if file.filename is None:
            raise InvalidFileFormatError()
        await self.__validate_file(file, allowed_formats)
        with open(path.join(settings.storage, file_name), "wb") as end_file:
            end_file.write(await file.read())

    async def remove_file(self, file_name: str) -> None:
        file_path = path.join(settings.storage, file_name)
        if not await self.exists(file_path):
            raise FileDoesNotExistError()
        remove(file_path)

    async def exists(self, file_path: str) -> bool:
        return path.isfile(path.join(settings.storage, file_path))

    async def __validate_file(
        self, file: IFileWrapper, allowed_formats: Pattern
    ) -> None:
        file_info = filetype.guess(file.file)
        if file_info is None:
            raise InvalidFileFormatError()

        detected_content_type = file_info.extension.lower()

        if not allowed_formats.match(file.content_type) or not allowed_formats.match(
            detected_content_type
        ):
            raise InvalidFileFormatError()

        real_file_size = 0
        for chunk in file.file:
            real_file_size += len(chunk)
            if real_file_size > settings.max_file_size:
                raise FileTooBigError()

    async def create_folder(self, folder_path: str, folder_name: str) -> None:
        new_path = path.join(folder_path, folder_name)
        end_path = path.join(settings.storage, new_path)
        if not path.exists(end_path):
            mkdir(end_path)

    async def remove_folder(self, folder_path: str) -> None:
        files = listdir(path.join(settings.storage, folder_path))
        for file in files:
            file_path = path.join(settings.storage, folder_path, file)
            if path.isfile(file_path):
                remove(file_path)
                continue
            await self.remove_folder(file_path)
        rmdir(path.join(settings.storage, folder_path))

    async def save_page(self, file_path: str, html: str) -> None:
        end_path = path.join(settings.storage, file_path, "index.html")
        with open(end_path, "wb") as new_page:
            new_page.write(html.encode("utf-8"))
