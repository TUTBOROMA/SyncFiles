import os
import requests
import logging

class YandexDisk:
    """ Класс для работы с API Яндекс Диска """
    
    def __init__(self, token, remote_folder):
        self.token = token
        self.remote_folder = remote_folder
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def _get_upload_link(self, path):
        """ Получение ссылки для загрузки файла на Яндекс Диск """
        upload_url = f"{self.base_url}/upload"
        params = {"path": os.path.join(self.remote_folder, os.path.basename(path)), "overwrite": "true"}
        response = requests.get(upload_url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()['href']

    def load(self, path):
        """ Загрузка нового файла на Яндекс Диск """
        try:
            upload_link = self._get_upload_link(path)
            with open(path, 'rb') as f:
                response = requests.put(upload_link, files={'file': f})
            response.raise_for_status()
            logging.info(f"Файл {path} загружен на Яндекс Диск.")
        except Exception as e:
            logging.error(f"Ошибка загрузки файла {path}: {e}")

    def reload(self, path):
        """ Перезапись измененного файла на Яндекс Диск """
        self.load(path)

    def delete(self, filename):
        """ Удаление файла с Яндекс Диска """
        try:
            delete_url = f"{self.base_url}?path={os.path.join(self.remote_folder, filename)}"
            response = requests.delete(delete_url, headers=self.headers)
            response.raise_for_status()
            logging.info(f"Файл {filename} удален с Яндекс Диска.")
        except Exception as e:
            logging.error(f"Ошибка удаления файла {filename}: {e}")

    def get_info(self):
        """ Получение информации о файлах на Яндекс Диске """
        try:
            params = {"path": self.remote_folder}
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Ошибка получения информации: {e}")
            return None
