FROM python:3.10-alpine3.18 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml /tmp
COPY poetry.lock /tmp


RUN poetry export -f requirements.txt --only core --only test --output requirements.txt --without-hashes

FROM python:3.10-alpine3.18

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

WORKDIR /app

# set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

EXPOSE 8181

# Copy requirements from previous stage to docker container in /app 
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install mysqlclient

COPY ./config /app/config
COPY ./src /app/src
COPY ./utils /app/utils
COPY entrypoint.sh .
COPY main.py .

# Copy files for unit tests
COPY ./tests /app/tests
COPY .coveragerc .
COPY pytest.ini .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]

