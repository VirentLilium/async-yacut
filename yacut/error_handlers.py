from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    """Исключение при некорректном обращении к API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик ошибок API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработчик ошибки HTTP 404."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработчик ошибки HTTP 500."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
