# syntax=docker/dockerfile:1

# Fastapi application
FROM python:3.10-alpine3.15
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt

# Add environment
COPY ./.docker.env /app/.env

# Add manage bash scripts
COPY ./run-project.sh /app/run-project.sh
RUN chmod u+x ./run-project.sh

COPY ./run-tests.sh /app/run-tests.sh
RUN chmod u+x ./run-tests.sh

# Add source sode
COPY ./src /app/src

CMD [ "/bin/sh", "./run-project.sh" ]
