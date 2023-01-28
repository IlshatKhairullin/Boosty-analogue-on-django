FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.3.2 && poetry config virtualenvs.create false

WORKDIR /app

RUN git init  # for pre commit hook

COPY pyproject.toml .
COPY poetry.lock .
COPY .pre-commit-config.yaml .
RUN poetry install --no-root && pre-commit install --install-hooks


COPY . .

RUN pre-commit run -a && python3 src/manage.py collectstatic --noinput

EXPOSE 8000


CMD python src/manage.py migrate && uwsgi deploy/app/uwsgi.ini
