from http import HTTPStatus

from flask import Response, abort, flash, redirect, render_template

from yacut import app
from yacut.exceptions import ShortLinkError
from yacut.forms import FileForm, LinkForm
from yacut.models import URLMap
from yacut.yandex_disk import async_upload_file_and_get_url


@app.route('/<string:short_id>')
def redirect_view(short_id: str) -> Response:
    """
    Перенаправляет на исходный URL по короткому идентификатору.

    :param short_id: Идентификатор короткой ссылки.
    :return: HTTP-ответ с перенаправлением.
    """
    link_object = URLMap.get_by_short_id(short_id)

    if link_object is None:
        abort(HTTPStatus.NOT_FOUND)

    return redirect(link_object.original)


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    """Создает короткую ссылку на страницу."""
    form = LinkForm()

    if form.validate_on_submit():
        original_link = form.original_link.data
        short_id = form.custom_id.data
        try:
            new_link = URLMap.create_short_link(original_link, short_id)
        except ShortLinkError as error:
            flash(str(error))
            return render_template('index.html', form=form)
        short_url = new_link.get_short_url()
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view() -> str:
    """Загружает файлы и создаёт короткие ссылки."""
    form = FileForm()
    file_links = []

    if form.validate_on_submit():
        files = form.files.data
        download_urls = await async_upload_file_and_get_url(files)

        for file, download_url in zip(files, download_urls):
            file_url = URLMap.create_short_link(download_url)
            short_url = file_url.get_short_url()
            file_links.append((file.filename, short_url))
    return render_template('add_files.html', form=form, file_links=file_links)
