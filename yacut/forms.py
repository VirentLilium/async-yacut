from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    URL,
    DataRequired,
    Length,
    Optional,
    Regexp,
)

from yacut.constants import MAX_LENGTH_OF_SHORT_ID, SHORT_ID_PATTERN


class LinkForm(FlaskForm):
    """Форма для ввода ссылок."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректный URL-адрес'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=MAX_LENGTH_OF_SHORT_ID),
            Regexp(SHORT_ID_PATTERN),
        ],
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    """Форма для загрузки файлов."""

    files = MultipleFileField(
        'Загрузить файлы',
        validators=[
            FileRequired(message='Файл обязателен'),
        ],
    )
    submit = SubmitField('Загрузить')
