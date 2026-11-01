# YaCut — сервис сокращения ссылок

YaCut — веб-приложение на Flask для создания коротких ссылок. Сервис преобразует длинные URL-адреса в компактные ссылки, которые перенаправляют на исходную страницу. Создавать ссылки можно через веб-интерфейс или REST API.

Также приложение позволяет загружать несколько файлов на Яндекс Диск и получать короткие ссылки для их скачивания.

## Возможности

- Создание коротких ссылок на исходные URL.
- Автоматическая генерация уникального шестисимвольного идентификатора.
- Выбор собственного идентификатора длиной до 16 символов (латинские буквы и цифры).
- Проверка допустимости и уникальности идентификатора.
- Перенаправление с короткой ссылки на исходный адрес.
- Создание коротких ссылок и получение исходных URL через REST API.
- Загрузка нескольких файлов на Яндекс Диск и получение коротких ссылок для скачивания.

## Технологии

- Python 3
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- Flask-Migrate
- Flask-WTF / WTForms
- aiohttp / asyncio
- python-dotenv
- SQLite
- HTML, CSS, Bootstrap

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/VirentLilium/async-yacut.git
cd async-yacut
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

### 3. Установить зависимости

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

Создайте файл `.env` в корневой директории проекта:

```dotenv
FLASK_APP=yacut
SECRET_KEY=replace_with_a_random_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_oauth_token
```

- `FLASK_APP` — имя Flask-приложения.
- `SECRET_KEY` — секретный ключ приложения (задайте собственное случайное значение).
- `DATABASE_URI` — адрес базы данных SQLAlchemy.
- `DISK_TOKEN` — OAuth-токен Яндекс Диска, необходимый для загрузки файлов.

Не публикуйте файл `.env` с настоящими секретами в репозитории!

### 5. Подготовить базу данных

Если в репозитории есть каталог `migrations` с готовыми миграциями, примените их:

```bash
flask db upgrade
```

Если проект разворачивается **без каталога миграций**, сначала создайте и примените начальную миграцию:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Запустить приложение

```bash
flask run
```

Откройте в браузере http://127.0.0.1:5000/.

## Использование

### Веб-интерфейс

На главной странице введите длинную ссылку. При желании укажите свой короткий идентификатор. После отправки формы сервис покажет короткий URL.

На странице `/files` можно выбрать несколько файлов для загрузки на Яндекс Диск и получить короткие ссылки для скачивания. Для работы этой функции нужен действующий `DISK_TOKEN`.

### REST API

**Создать короткую ссылку — `POST /api/id/`**

Пример запроса:

```bash
curl -X POST http://127.0.0.1:5000/api/id/ \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://www.python.org/", "custom_id": "python"}'
```

Пример ответа (HTTP 201):

```json
{
  "url": "https://www.python.org/",
  "short_link": "http://127.0.0.1:5000/python"
}
```

Поле `custom_id` необязательно. Если его не передать, сервис автоматически создаст идентификатор.

**Получить исходный URL — `GET /api/id/<short_id>/`**

Пример запроса:

```bash
curl http://127.0.0.1:5000/api/id/python/
```

Пример ответа (HTTP 200):

```json
{
  "url": "https://www.python.org/"
}
```

При некорректных данных API возвращает JSON с описанием ошибки. Если идентификатор не найден, возвращается HTTP 404.

Спецификация API находится в файле [`openapi.yml`](openapi.yml).

## Автор

Тодышева Лилия — [GitHub](https://github.com/VirentLilium/).
