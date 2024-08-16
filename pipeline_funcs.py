import os, json, datetime
# import mariadb
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# ===============================================================
# ================   READ SAVED JSONL FILES   ===================

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

def read_every_line(file_path):
    with open(file_path, 'rb') as f:
        jsons = f.readlines()
        for j in jsons:
            yield json.loads(j)

# ===============================================================
# ===============   DATA EXTRACTION FROM JSON   =================

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
        # split_date = str.split(date, '-')
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(int(weather_code) > 8)
            hour = int(int(h['$']) / 60)
            # dt = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), hour)
            stringtime = f"{date} {hour}:00:00"
            data_row = [location, stringtime, temp, weather_code, precip_bool]
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
        # split_date = str.split(date, '-')
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(int(weather_code) > 8)
            hour = int(int(h['$']) / 60)
            # dt = datetime.datetime(int(split_date[0]), \
            #                        int(split_date[1]), \
            #                         int(split_date[2]), hour)
            stringtime = f"{date} {hour}:00:00"
            return_list.append([location, stringtime, temp, weather_code, precip_bool])
    return return_list

def met_past_24h_extract_dict(json_line):
    """
    Takes a json line of the met past 24 hour data and generates 
    a list of dictionaries for each hour of the previous day.
    The output lists contain the location, date, hour, temperature (C),
    weather code and boolean for if there was precipitation.
    """
    return_list = []
    location = json_line['SiteRep']['DV']['Location']['name']
    days = json_line['SiteRep']['DV']['Location']['Period']
    for day in days:
        date = day['value'][:-1]
        # split_date = str.split(date, '-')
        for h in day['Rep']:
            temp = h['T']
            weather_code = h['W']
            precip_bool = int(int(weather_code) > 8)
            hour = int(int(h['$']) / 60)
            # dt = datetime.datetime(int(split_date[0]), \
            #                        int(split_date[1]), \
            #                         int(split_date[2]), hour)
            stringtime = f"{date} {hour}:00:00"
            return_list.append({'location' : location, 'date_time' : stringtime, 'temp' : temp, 
                                'weather_code' : weather_code, 'precip_bool' : precip_bool})
    return return_list

def met_5d_extract_dict(json_line):
    """
    Takes a json line of the met 5 day forecast data and generates 
    a list of dictionaries for each day.
    The output dictionaries contain the location, date being forecast, 
    the number of days in advance the forecast was collected, the 
    predicted maximum temperature (C), weather code and probability (%) 
    of precipitation.
    """
    return_list = [] # empty list to collect the data dictionaries
    json_data = json_line['SiteRep']['DV']

    # get the date that the forecast was collected
    datetime0 = json_line['SiteRep']['DV']['dataDate']
    date0_split = str.split(datetime0[:10], '-') # split date into ['year', 'month', 'day']
    date0 = datetime.date(int(date0_split[0]), int(date0_split[1]), int(date0_split[2]))
    location = json_data['Location']['name']

    json_forecasts = json_line['SiteRep']['DV']['Location']['Period']
    for d in json_forecasts: # loop over each day of the 5 day forecast
        forecast_date_split = str.split(d['value'][:10], '-')
        forecast_date = datetime.date(int(forecast_date_split[0]), 
                            int(forecast_date_split[1]), 
                            int(forecast_date_split[2]))
        forecast_date_str = d['value'][:10]
        # calculate the number of days difference between the date the forecast 
        # was made and the date that the forecast is predicting
        days_delta = str(forecast_date - date0)[:1]
        for period in d['Rep']: # loop over night and day forecasts
            if period['$'] == 'Day':
                temp_max = period['Dm']
                weather_code = period['W']
                precip_prob = period['PPd']
                return_list.append({'location' : location, 'date' : forecast_date_str, 'forecast_delta' : days_delta, 
                                    'temp_max' : temp_max, 'weather_code' : weather_code, 'precip_prob' : precip_prob})
    return return_list

def accu_5d_extract_dict(json_line):
    location = 'CREDENHILL'
    date0_split = str.split(json_line['DailyForecasts'][0]['Date'][:10], '-')
    date0_split = [int(x) for x in date0_split]
    date0 = datetime.date(date0_split[0], date0_split[1], date0_split[2])

    return_list = []
    for d in json_line['DailyForecasts']:
        forecast_date_str = d['Date'][:10]
        forecast_date_split = str.split(d['Date'][:10], '-')
        forecast_date_split = [int(x) for x in forecast_date_split]
        forecast_date = datetime.date(forecast_date_split[0], forecast_date_split[1], forecast_date_split[2])
        days_delta = str(forecast_date - date0)[:1]

        temp_max = (d['Temperature']['Maximum']['Value'] -25) * 5 / 9
        temp_min = (d['Temperature']['Minimum']['Value'] -25) * 5 / 9
        precip_bool = d['Day']['HasPrecipitation']
        return_list.append({'location' : location, 'date' : forecast_date_str, 'forecast_delta' : days_delta,
                            'temp_max' : temp_max, 'temp_min' : temp_min, 'precip_bool' : precip_bool})
    return return_list
    


# ===============================================================
# ===================   MARIADB FUNCTIONS   =====================

# col_name_dict = {'met_past_24h' : ['(location, date_time, temp, weather_code, precip_bool)', 
#                                    '(?, ?, ?, ?, ?)']}

# extract_dict = {'met_past_24h' : met_past_24h_extract_list}

# def sql_add_data(table_name, json_line):
#     col_names = col_name_dict[table_name]
#     insert_query = f"""
#                     INSERT INTO {table_name} {col_names[0]}
#                     VALUES {col_names[1]}
#                     """
#     new_values = extract_dict[table_name](json_line)

#     try:
#         with mariadb.connect(host = 'localhost',
#                     user = os.getenv('MYSQL_USER'),
#                     password = os.getenv('MYSQL_PASS'),
#                     database = 'weather_comp') as connection:
#             cur = connection.cursor()
#             cur.executemany(insert_query, new_values)
#             connection.commit()
#     except mariadb.Error as e:
#         print(e)

# ===============================================================
# ===================   SUPABASE FUNCTIONS   ====================

url = os.getenv('SUPABASE_URL')
key = os.getenv("SUPABASE_SECRET_KEY")

extract_dict = {'met_past_24h' : met_past_24h_extract_dict,
                'met_5d' : met_5d_extract_dict,
                'accu_5d' : accu_5d_extract_dict}

def supabase_add_data(table_name, json_line):
    new_values = extract_dict[table_name](json_line)

    supabase = create_client(url, key)
    try:
        response = supabase.table(table_name).upsert(new_values, ignore_duplicates=True).execute()
    except:
        print(f'Error inserting values into {table_name}')
        return response

