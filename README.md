# Boosty/pikabu analogue

Для работы с проектом нужно установить [python](http://python.org) и 
[poetry](https://python-poetry.org/) <= `poetry init` после установки. 

- `docker compose up -d` - поднять PostgreSQL с помощью Docker

- `poetry shell` - вход в виртуальное окружение

- `poetry install` - установка зависимостей

- `python src/manage.py migrate` - выполнить миграции

- `python src/manage.py runserver` - запуск сервера для разработки на http://127.0.0.1:8000


Для того, чтобы узнать расположение интерпретатора для настройки в PyCharm можно выполнить
команду `poetry env info -p`

Для того, чтобы выйти(деактивировать) окружение можно выполнить команду `exit`
