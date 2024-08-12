FROM ubuntu:latest

WORKDIR /WeatherComparison

COPY Pipfile Pipfile.lock /WeatherComparison/
COPY get_funcs.py daily_get.py /WeatherComparison/

RUN apt-get update
RUN apt-get install -y python3-pip pipenv
# installing dependencies below does not complete successfully when building image
RUN cd /WeatherComparison/ && pipenv install --system
# RUN pipenv --rm




