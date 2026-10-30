from flask import jsonify, request, url_for

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_valid_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """
    Создаёт короткую ссылку через API.

    :return: JSON с исходным и коротким URL, HTTP 201.
    :raises InvalidAPIUsage: При некорректных данных запроса.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    url = data.get('url')
    if url is None or url == '':
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id is None or custom_id == '':
        short_id = get_unique_short_id()
    elif not is_valid_short_id(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif (
        URLMap.query.filter_by(short=custom_id).first() is not None
        or custom_id == 'files'
    ):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    else:
        short_id = custom_id

    link_object = URLMap(original=url, short=short_id)
    db.session.add(link_object)
    db.session.commit()
    return jsonify(
        {
            'url': link_object.original,
            'short_link': url_for(
                'redirect_view', short_id=link_object.short, _external=True
            ),
        }
    ), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Возвращает исходный URL по короткому идентификатору.

    :param short_id: Идентификатор короткой ссылки.
    :return: JSON с исходным URL, HTTP 200.
    :raises InvalidAPIUsage: Если идентификатор не найден.
    """
    link_object = URLMap.query.filter_by(short=short_id).first()
    if not link_object:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link_object.original}), 200
