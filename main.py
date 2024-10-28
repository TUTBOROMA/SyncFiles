import time
import os
import logging
import configparser
from configparser import ConfigParser
from yandex_disk import YandexDisk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import time
# Чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
def check_internet_connection():
    try:
        # Проверяем соединение с общедоступным сайтом (например, Google)
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def main():
    while True:
        if not check_internet_connection():
            print("Интернета нет. Проверьте подключение.")
        else:
            print("Интернет подключен.")
        
        # Задержка перед следующей проверкой (например, 10 секунд)
        time.sleep(10)
logging.basicConfig(filename='sync_log.log', level=logging.ERROR)

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

SYNC_FOLDER = config.get('settings', 'sync_folder')

# Проверка существования папки
if not os.path.exists(SYNC_FOLDER):
    error_message = f"Ошибка: Папка {SYNC_FOLDER} не существует."
    print(error_message)
    logging.error(error_message)
else:
    print(f"Папка {SYNC_FOLDER} найдена. Продолжаем работу.")
SYNC_FOLDER = config.get('settings', 'sync_folder')
REMOTE_FOLDER = config.get('settings', 'remote_folder')
TOKEN = config.get('settings', 'token')
SYNC_INTERVAL = config.getint('settings', 'sync_interval')
LOG_FILE = config.get('settings', 'log_file')

# Настройка логирования
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Инициализация API Яндекс Диска
disk = YandexDisk(TOKEN, REMOTE_FOLDER)

class SyncHandler(FileSystemEventHandler):
    """ Класс для обработки изменений в папке """
    
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f'Создан файл: {event.src_path}')
            disk.load(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f'Изменен файл: {event.src_path}')
            disk.reload(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f'Удален файл: {event.src_path}')
            disk.delete(os.path.basename(event.src_path))

def monitor_folder():
    """ Функция для отслеживания изменений в папке """
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, SYNC_FOLDER, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(SYNC_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    logging.info("Запуск программы синхронизации")
    monitor_folder()
    main()
