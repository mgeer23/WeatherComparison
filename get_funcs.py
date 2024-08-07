import requests, os

from dotenv import load_dotenv

load_dotenv()
ACCU_KEY = os.getenv('ACCU_KEY')
MET_KEY = os.getenv('MET_KEY')

met_url = 'http://datapoint.metoffice.gov.uk/public/data/'


def accu_loc_id(postcode):
    postcode_url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search'
    payload = {'apikey': ACCU_KEY, 'q': postcode}

    r = requests.get(postcode_url, params=payload)
    if r.status_code == 200:
        return r.json()[0]['Key']
    else:
        print("accu_loc_id error code: " + str(r.status_code))
        return f'Error code: {r.status_code}'

def accu_5d_forecast(accu_loc_id):
    accu_5d_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
    accu_5d_request = accu_5d_url + accu_loc_id
    payload = {'apikey': ACCU_KEY}

    r = requests.get(accu_5d_request, params = payload)
    if r.status_code == 200:
        return r.json()
    else:
        print("accu_5d_forecast error code: " + str(r.status_code))
        return f'Error code: {r.status_code}'
    

def met_loc_id(location):
    site_list_resource = 'val/wxfcs/all/json/sitelist'
    site_list_request = met_url + site_list_resource
    payload = {'key': MET_KEY}

    r = requests.get(site_list_request, params = payload)
    if r.status_code == 200:
        met_locations = r.json()['Locations']['Location']
        for l in met_locations:
            if l['name'] == location:
                met_loc_id = l['id']
        return met_loc_id
    else:
        print("met_loc_id error code: " + str(r.status_code))
        return f'Error code: {r.status_code}'

def met_5d_forecast(met_loc_id):
    met_5d_resource = 'val/wxfcs/all/json/'
    met_5d_request = met_url +met_5d_resource + met_loc_id
    payload = {'res': 'daily', 'key': MET_KEY}

    r = requests.get(met_5d_request, params=payload)
    if r.status_code == 200:
        return r.json()
    else:
        print("met_5d_forecast error code: " + str(r.status_code))
        return f'Error code: {r.status_code}'

def met_past_24h(met_loc_id):
    met_obs_resource = 'val/wxobs/all/json/'
    met_obs_request = met_url + met_obs_resource + met_loc_id
    payload = {'res': 'hourly', 'key': MET_KEY}

    r = requests.get(met_obs_request, params = payload)
    if r.status_code == 200:
        return r.json()
    else:
        print("met_past_24h error code: " + str(r.status_code))
        return f'Error code: {r.status_code}'






