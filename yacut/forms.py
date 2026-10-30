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
            Length(max=16),
            Regexp(r'^[a-zA-Z0-9]+$'),
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
