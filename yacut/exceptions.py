class ShortLinkError(ValueError):
    """Ошибка создания короткой ссылки."""


class ExcessRepetitionError(Exception):
    """Уникальный короткий идентификатор не создан, потрачены все попытки."""

    def __init__(
        self,
        message='Не удалось сгенерировать уникальный короткий идентификатор.',
    ) -> None:
        super().__init__(message)
