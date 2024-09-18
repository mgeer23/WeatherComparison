FROM python:latest

WORKDIR /WeatherComparison

COPY get_funcs.py pipeline_funcs.py daily_supabase.py requirements.txt .env /WeatherComparison/

RUN pip install -r requirements.txt

CMD ["python3", "./daily_supabase.py"]
