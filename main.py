import time
import os
import logging
from configparser import ConfigParser
from yandex_disk import YandexDisk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Чтение конфигурационного файла
config = ConfigParser()
config.read('config.ini', encoding='utf-8')


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
