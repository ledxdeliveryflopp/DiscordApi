FROM python:3.12-slim-bullseye
LABEL maintainer="LedxDeliveryFlopp"

WORKDIR /user_microservice

COPY . /user_microservice

RUN pip install --no-cache-dir poetry==1.8.4 && poetry config virtualenvs.create false && poetry install

ENTRYPOINT ["python", "main.py"]
