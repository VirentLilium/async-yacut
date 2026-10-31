import asyncio
from uuid import uuid4

import aiohttp
from werkzeug.datastructures import FileStorage

from yacut import app
from yacut.constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL

AUTH_HEADER = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


async def async_upload_file_and_get_url(
    files: list[FileStorage],
) -> list[str]:
    """
    Асинхронная функция конкурентно загружает файлы на Яндекс Диск.

    :param files: Список объектов FileStorage из Flask-WTF.
    :return: Список URL для скачивания файлов.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_and_get_url(session, file) for file in files]
        download_urls = await asyncio.gather(*tasks)

    return download_urls


async def upload_file_and_get_url(
    session: aiohttp.ClientSession,
    file: FileStorage,
) -> str:
    """
    Загружает один файл и возвращает URL для скачивания.

    :param session: Объект aiohttp.ClientSession.
    :param file: Объект FileStorage из Flask-WTF.
    :return: URL для скачивания файла.
    """
    filename = file.filename
    unique_name = f'{uuid4().hex}_{filename}'
    path = 'app:/' + unique_name

    async with session.get(
        url=REQUEST_UPLOAD_URL,
        headers=AUTH_HEADER,
        params={
            'path': path,
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        data = await response.json()
        upload_url = data['href']

    async with session.put(
        url=upload_url,
        data=file.read(),
    ) as response:
        response.raise_for_status()

    async with session.get(
        headers=AUTH_HEADER,
        url=DOWNLOAD_LINK_URL,
        params={
            'path': path,
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        data = await response.json()
        download_url = data['href']

    return download_url
