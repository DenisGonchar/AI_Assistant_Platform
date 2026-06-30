import logging
from pathlib import Path

# Папка для хранения логов
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

# Имя файла лога
LOG_FILE = LOG_DIR / 'app.log'

#Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger('AI_Assistant')