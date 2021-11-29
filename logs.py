from os import path, remove
import logging.config

# Удалите существующий файл лога, если он есть, чтобы создавать новый файл во время каждого выполнения
from typing import AbstractSet, Mapping

if path.isfile("python_logging.log"):
    remove("python_logging.log")


# Создайте Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создайте обработчик для записи данных в файл
logger_handler = logging.FileHandler('python_logging.log')
logger_handler.setLevel(logging.DEBUG)

# Создайте Formatter для форматирования сообщений в логе
logger_formatter = logging.Formatter('%(asctime)s  %(levelname)-8s %(message)s (%(filename)s:%(lineno)d)')

# Добавьте Formatter в обработчик
logger_handler.setFormatter(logger_formatter)

# Добавте обработчик в Logger
logger.addHandler(logger_handler)
# logger.info('Настройка логгирования окончена!')

