from pipeline_funcs import read_every_line, sql_add_data
import os

file_path = os.getenv('PI_PATH') + '/data/met_past_24h.jsonl'

for l in read_every_line(file_path):
    sql_add_data('met_past_24h', l)