FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.3.2 && poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install


COPY . .

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000


CMD python src/manage.py migrate && uwsgi deploy/app/uwsgi.ini
