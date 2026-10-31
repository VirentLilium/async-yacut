# Короткие ссылки
DEFAULT_SHORT_ID_LENGTH = 6
FORBIDDEN_SHORT_ID = ('files',)
MAX_LENGTH_OF_SHORT_ID = 16
MAX_REPETITIONS = 100
MIN_LENGTH_OF_SHORT_ID = 1
SHORT_ID_PATTERN = r'^[a-zA-Z0-9]+$'

# API Яндекс Диска
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
