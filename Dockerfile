FROM ubuntu:latest

WORKDIR /WeatherComparison

COPY get_funcs.py daily_get.py requirements.txt .env /WeatherComparison/

RUN apt update
# RUN apt install wget 
RUN apt install -y python3-pip python3-venv libmariadb3 libmariadb-dev
# ADD wget https://r.mariadb.com/downloads/mariadb_repo_setup
# RUN chmod +x mariadb_repo_setup 
# RUN apt install libmariadb3 libmariadb-dev

RUN python3 -m venv /WeatherComparison/myvenv
RUN . /WeatherComparison/myvenv/bin/activate && pip install -r requirements.txt






