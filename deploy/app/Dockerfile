FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000


CMD python src/manage.py migrate && uwsgi deploy/app/uwsgi.ini
