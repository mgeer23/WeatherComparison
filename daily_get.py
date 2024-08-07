import json, os
from get_funcs import met_loc_id, met_5d_forecast, met_past_24h, accu_loc_id, accu_5d_forecast
from dotenv import load_dotenv

load_dotenv()
PI_PATH = os.getenv('PI_PATH')

met_credenhill_id = met_loc_id('Credenhill')
print(met_credenhill_id)

request = met_5d_forecast(met_credenhill_id)
if type(request) == str:
    with open('data/met_5d.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/met_5d.jsonl', 'a') as f:

        f.write(request + '\n')
else:
    with open('data/met_5d.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/met_5d.jsonl', 'a') as f:
        f.write(json.dumps(request) + '\n')

request = met_past_24h(met_credenhill_id)
if type(request) == str:
    with open('data/met_past_24h.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/met_past_24h.jsonl', 'a') as f:
        f.write(request + '\n')
else:
    with open('data/met_past_24h.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/met_past_24h.jsonl', 'a') as f:
        f.write(json.dumps(met_past_24h(met_credenhill_id)) + '\n')

accu_credenhill_id = accu_loc_id('HR47DW')
print(accu_credenhill_id)

request = accu_5d_forecast(accu_credenhill_id)
if type(request) == str:
    with open('data/accu_5d.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/accu_5d.jsonl', 'a') as f:
        f.write(request + '\n')
else:
    with open('data/accu_5d.jsonl', 'a') as f:
    # with open(PI_PATH + 'data/accu_5d.jsonl', 'a') as f:
        f.write(json.dumps(accu_5d_forecast(accu_credenhill_id)) + '\n')