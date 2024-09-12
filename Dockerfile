FROM ubuntu:latest

WORKDIR /WeatherComparison

COPY get_funcs.py pipeline_funcs.py daily_supabase.py requirements.txt .env /WeatherComparison/

RUN apt update
RUN apt install -y python3-pip python3-venv

RUN python3 -m venv /WeatherComparison/myvenv
ENV PATH="/WeatherComparison/myvenv/bin:$PATH"
# RUN . /WeatherComparison/myvenv/bin/activate && pip install -r requirements.txt
RUN pip install -r requirements.txt
CMD ["python3", "daily_supabase.py"]
