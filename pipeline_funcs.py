import os, json

def read_last_line(file_path):
    """
    Returns the last line of a file, or the first if only one line exists
    Parameters:
        file_path: str
            Pathway to the file to be read
    """
    with open(file_path, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        return json.loads(f.readline().decode())
    
def met_past_24h_extract(json_str):
    """
    Takes a json line of the met past 24 hour data and generates
    individual lists for each hour of the previous day.
    The output lists contain the location, date, hour, temperature (C),
    weather code and boolean for if there was precipitation.
    """
    location = json_str['SiteRep']['DV']['Location']['name']
    days = json_str['SiteRep']['DV']['Location']['Period']
    for day in days:
        date = day['value'][:-1]
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(weather_code) > 8
            hour = int(h['$']) / 60
            data_row = [location, date, hour, temp, weather_code, precip_bool]
            yield data_row



line = read_last_line('data/met_past_24h.jsonl')
print(line)
print(type(line))

print(met_past_24h_extract(line))

for h in met_past_24h_extract(line):
    print(h)