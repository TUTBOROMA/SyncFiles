
# SyncFiles

## Описание
SyncFiles — это простое приложение для синхронизации файлов между локальной папкой и Яндекс Диском. Оно позволяет автоматически загружать новые или измененные файлы в указанную папку на Яндекс Диске через заданные интервалы времени.

## Установка

1. Склонируйте репозиторий или скачайте проект на свой компьютер:
   ```bash
   git clone https://your-repo-url.git
   cd SyncFiles
   ```

2. Убедитесь, что у вас установлен Python (рекомендуется версия 3.6 и выше). Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте файл конфигурации `config.ini`:
   ```ini
   [settings]
   sync_folder = C:\Users\Рома\Desktop\SyncFiles-master   # Путь к локальной папке для синхронизации
   remote_folder = /  # Папка на Яндекс Диске
   token = "ваш_токен_яндекс_диска"        # Токен доступа к API Яндекс Диска
   sync_interval = 60                    # Интервал синхронизации в секундах
   log_file = C:\Users\Рома\Desktop\sync_log.log  # Путь к файлу лога
   ```

   **Примечание:** Получить токен можно [здесь](https://oauth.yandex.ru/).

## Запуск

Для запуска приложения выполните следующую команду в терминале:
```bash
python main.py
```

### Примеры ввода и вывода

- **Добавление файла:**
  1. Создайте файл в локальной папке, указанной в `sync_folder`.
  2. После заданного интервала времени приложение автоматически загрузит файл на Яндекс Диск.

- **Изменение файла:**
  1. Измените существующий файл в локальной папке.
  2. Приложение обнаружит изменения и синхронизирует их на Яндекс Диск.

- **Логи:**
  - Все действия и возможные ошибки записываются в файл, указанный в `log_file`. Вы можете открыть его для проверки статуса синхронизации.

## Заключение

SyncFiles — это удобный инструмент для автоматизации процесса синхронизации файлов между локальным хранилищем и Яндекс Диском. При возникновении вопросов или предложений по улучшению, пожалуйста, свяжитесь с автором проекта.
