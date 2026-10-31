import re

from yacut.constants import (
    MAX_LENGTH_OF_SHORT_ID,
    MIN_LENGTH_OF_SHORT_ID,
    SHORT_ID_PATTERN,
)


def is_valid_short_id(short_id: str) -> bool:
    """
    Проверяет длину и допустимые символы короткого идентификатора.

    :param short_id: Идентификатор короткой ссылки.
    :return: True, если идентификатор корректен, иначе False.
    """
    return (
        isinstance(short_id, str)
        and MIN_LENGTH_OF_SHORT_ID <= len(short_id) <= MAX_LENGTH_OF_SHORT_ID
        and re.fullmatch(SHORT_ID_PATTERN, short_id) is not None
    )
