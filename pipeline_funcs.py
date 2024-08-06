import os, json, datetime

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
    
def met_past_24h_extract(json_line):
    """
    Takes a json line of the met past 24 hour data and generates
    individual lists for each hour of the previous day.
    The output lists contain the location, date, hour, temperature (C),
    weather code and boolean for if there was precipitation.
    """
    location = json_line['SiteRep']['DV']['Location']['name']
    days = json_line['SiteRep']['DV']['Location']['Period']
    for day in days:
        date = day['value'][:-1]
        split_date = str.split(date, '-')
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(int(weather_code) > 8)
            hour = int(h['$']) / 60
            dt = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), hour)
            data_row = [location, dt, temp, weather_code, precip_bool]
            yield data_row

def met_past_24h_extract_list(json_line):
    """
    Takes a json line of the met past 24 hour data and generates
    individual lists for each hour of the previous day.
    The output lists contain the location, date, hour, temperature (C),
    weather code and boolean for if there was precipitation.
    """
    return_list = []
    location = json_line['SiteRep']['DV']['Location']['name']
    days = json_line['SiteRep']['DV']['Location']['Period']
    for day in days:
        date = day['value'][:-1]
        split_date = str.split(date, '-')
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(int(weather_code) > 8)
            hour = int(h['$']) / 60
            dt = datetime.datetime(int(split_date[0]), \
                                   int(split_date[1]), \
                                    int(split_date[2]), hour)
            return_list.append([location, dt, temp, weather_code, precip_bool])
    return return_list



line = read_last_line('data/met_past_24h.jsonl')
print(line)
print(type(line))

print(met_past_24h_extract(line))

for h in met_past_24h_extract(line):
    print(h)