import asyncio
from uuid import uuid4

import aiohttp

from yacut import app

DISK_TOKEN = app.config['DISK_TOKEN']

AUTH_HEADER = {'Authorization': f'OAuth {DISK_TOKEN}'}

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def async_upload_file_and_get_url(files):
    """
    Асинхронная функция конкурентно загружает файлы на Яндекс Диск.

    :param files: Список объектов FileStorage из Flask-WTF.
    :return: Список URL для скачивания файлов.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_and_get_url(session, file) for file in files]
        download_urls = await asyncio.gather(*tasks)

    return download_urls


async def upload_file_and_get_url(session, file):
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
        data=file.stream,
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
