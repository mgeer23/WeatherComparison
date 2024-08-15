FROM ubuntu:latest

WORKDIR /WeatherComparison

COPY get_funcs.py daily_get.py requirements.txt .env /WeatherComparison/

RUN apt update
RUN apt install -y python3-pip python3-venv

RUN python3 -m venv /WeatherComparison/myvenv
RUN . /WeatherComparison/myvenv/bin/activate && pip install -r requirements.txt






