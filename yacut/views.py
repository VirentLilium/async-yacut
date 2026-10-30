from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import FileForm, LinkForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import async_upload_file_and_get_url


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """
    Перенаправляет на оригинальную ссылку по короткому идентификатору.

    :param short_id: Идентификатор короткой ссылки.
    """
    link_object = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link_object.original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Создает короткую ссылку на страницу."""
    form = LinkForm()

    if form.validate_on_submit():
        original_link = form.original_link.data
        short_id = form.custom_id.data

        if not short_id:
            short_id = get_unique_short_id()
        elif (
            URLMap.query.filter_by(short=short_id).first()
            or short_id == 'files'
        ):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        new_link = URLMap(original=original_link, short=short_id)
        db.session.add(new_link)
        db.session.commit()
        short_url = url_for('redirect_view', short_id=short_id, _external=True)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    """Загружает файлы и создаёт короткие ссылки."""
    form = FileForm()
    file_links = []

    if form.validate_on_submit():
        files = form.files.data
        download_urls = await async_upload_file_and_get_url(files)

        for file, download_url in zip(files, download_urls):
            filename = file.filename
            short_id = get_unique_short_id()
            file_url = URLMap(original=download_url, short=short_id)
            db.session.add(file_url)
            short_url = url_for(
                'redirect_view', short_id=short_id, _external=True
            )
            file_links.append((filename, short_url))
        db.session.commit()
    return render_template('add_files.html', form=form, file_links=file_links)
