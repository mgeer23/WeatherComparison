from get_funcs import met_loc_id, met_5d_forecast, met_past_24h, accu_loc_id, accu_5d_forecast
from pipeline_funcs import supabase_add_data

met_credenhill_id = met_loc_id('Credenhill')

request = met_5d_forecast(met_credenhill_id)
if type(request) == str:
    pass
else:
    supabase_add_data('met_5d', request)


request = met_past_24h(met_credenhill_id)
if type(request) == str:
    pass
else:
    supabase_add_data('met_past_24h', request)

# =======================================================
# =================   AccuWeather   =====================

accu_credenhill_id = accu_loc_id('HR47DW')

request = accu_5d_forecast(accu_credenhill_id)
if type(request) == str:
    pass
else:
    supabase_add_data('accu_5d', request)