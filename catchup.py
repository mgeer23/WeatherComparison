# run transform and load functions for data from pi

from pipeline_funcs import read_every_line, supabase_add_data

# MET past 24 hours data

for line in read_every_line('data/Pi_24Aug27/met_past_24h.jsonl'):
    supabase_add_data('met_past_24h', line)

# for line in read_every_line('data/Pi_24Aug27/met_5d.jsonl'):
#     supabase_add_data('met_5d', line)

# for line in read_every_line('data/Pi_24Aug27/accu_5d.jsonl'):
#     supabase_add_data('accu_5d', line)
