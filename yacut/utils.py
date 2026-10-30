import random
import re
from string import ascii_letters, digits

from yacut.models import URLMap


def is_valid_short_id(short_id):
    """
    Проверяет корректность идентификатора short_id.

    Может содержать цифры и латинские буквы, длина от 1 до 16 символов.

    :param short_id: Идентификатор короткой ссылки.
    :return: bool.
    """
    return (
        isinstance(short_id, str)
        and re.fullmatch(r'[a-zA-Z0-9]{1,16}', short_id) is not None
    )


def get_unique_short_id(length=6):
    """
    Генерирует уникальный короткий идентификатор.

    Проверяет отсутствие идентификатора в БД и исключает
    зарезервированное имя files.

    :param length: Длина идентификатора, по умолчанию 6.
    :return: Уникальный короткий идентификатор.
    """
    symbols = ascii_letters + digits

    while True:
        short_id = ''.join(random.choice(symbols) for _ in range(length))

        if (
            URLMap.query.filter_by(short=short_id).first() is None
            and short_id != 'files'
        ):
            return short_id
