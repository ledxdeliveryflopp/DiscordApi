FROM python:3.12-slim-bullseye
LABEL maintainer="LedxDeliveryFlopp"

WORKDIR /event_gateway

COPY . /event_gateway

RUN pip install --no-cache-dir poetry==1.8.4 && poetry config virtualenvs.create false && poetry install

ENTRYPOINT ["python", "main.py"]
