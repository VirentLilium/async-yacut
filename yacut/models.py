from __future__ import annotations

import random
from datetime import datetime
from string import ascii_letters, digits

from flask import url_for

from yacut import db
from yacut.constants import (
    DEFAULT_SHORT_ID_LENGTH,
    FORBIDDEN_SHORT_ID,
    MAX_LENGTH_OF_SHORT_ID,
    MAX_REPETITIONS,
)
from yacut.exceptions import ExcessRepetitionError, ShortLinkError
from yacut.utils import is_valid_short_id


class URLMap(db.Model):
    """Модель ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_OF_SHORT_ID), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self) -> dict[str, str]:
        return {
            'url': self.original,
            'short_link': self.get_short_url(),
        }

    @classmethod
    def get_by_short_id(cls, short_id: str) -> URLMap | None:
        """
        Находит объект URLMap по короткому идентификатору.

        :param short_id: Идентификатор короткой ссылки.
        :return: Объект класса или None, если объект не найден.
        """
        return cls.query.filter_by(short=short_id).first()

    def get_short_url(self) -> str:
        """Возвращает абсолютную короткую ссылку для объекта."""
        return url_for('redirect_view', short_id=self.short, _external=True)

    @classmethod
    def get_unique_short_id(cls, length: int = DEFAULT_SHORT_ID_LENGTH) -> str:
        """
        Метод генерации уникального короткого идентификатора.

        Проверяет отсутствие идентификатора в БД и исключает
        зарезервированные имена.

        :param length: Длина идентификатора.
        :return: Уникальный короткий идентификатор.
        """
        symbols = ascii_letters + digits

        for _ in range(MAX_REPETITIONS):
            short_id = ''.join(random.choice(symbols) for _ in range(length))
            if (
                cls.get_by_short_id(short_id) is None
                and short_id not in FORBIDDEN_SHORT_ID
            ):
                return short_id
        raise ExcessRepetitionError(
            'Не удалось сгенерировать уникальный короткий идентификатор.'
        )

    @staticmethod
    def create_short_link(
        original: str, short_id: str | None = None
    ) -> URLMap:
        """
        Создаёт и сохраняет в БД объект короткой ссылки.

        Если пользовательский идентификатор не указан, генерирует уникальный.
        Проверяет допустимость и доступность пользовательского идентификатора.

        :param original: Исходный URL.
        :param short_id: Пользовательский короткий идентификатор или None.
        :return: Созданный объект URLMap.
        :raises ShortLinkError: Если идентификатор некорректен или занят.
        """
        if short_id is None or short_id == '':
            short_id = URLMap.get_unique_short_id()
        elif not is_valid_short_id(short_id):
            raise ShortLinkError(
                'Указано недопустимое имя для короткой ссылки'
            )
        elif (
            URLMap.get_by_short_id(short_id) is not None
            or short_id in FORBIDDEN_SHORT_ID
        ):
            raise ShortLinkError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        new_link = URLMap(original=original, short=short_id)
        db.session.add(new_link)
        db.session.commit()
        return new_link
