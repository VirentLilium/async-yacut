from http import HTTPStatus

from flask import Response, jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.exceptions import ShortLinkError
from yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link() -> tuple[Response, int]:
    """
    Создаёт короткую ссылку через API.

    :return: JSON с исходным и коротким URL, HTTP 201 Created.
    :raises InvalidAPIUsage: При некорректных данных запроса.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    url = data.get('url')
    if url is None or url == '':
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    try:
        link_object = URLMap.create_short_link(url, custom_id)
    except ShortLinkError as error:
        raise InvalidAPIUsage(str(error)) from error

    return jsonify(link_object.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id: str) -> Response:
    """
    Возвращает исходный URL по короткому идентификатору.

    :param short_id: Идентификатор короткой ссылки.
    :return: JSON с исходным URL, HTTP 200.
    :raises InvalidAPIUsage: Если идентификатор не найден.
    """
    link_object = URLMap.get_by_short_id(short_id)

    if link_object is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': link_object.original})
