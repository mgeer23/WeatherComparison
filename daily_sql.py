from pipeline_funcs import read_last_line, met_past_24h_extract_list, sql_add_data
import os

json_line = read_last_line('data/met_past_24h.jsonl')
json_line = read_last_line(os.getenv('PI_PATH') + '/data/met_past_24h.jsonl')
# sql_add_data('met_past_24h', json_line)