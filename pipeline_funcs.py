import os, json, mariadb

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

# ===============================================================
# ===================   MARIADB FUNCTIONS   =====================

col_name_dict = {'met_past_24h' : ['(location, date_time, temp, weather_code, precip_bool)', 
                                   '(?, ?, ?, ?, ?)']}

extract_dict = {'met_past_24h' : met_past_24h_extract_list}

def sql_add_data(table_name, json_line):
    col_names = col_name_dict[table_name]
    insert_query = f"""
                    INSERT INTO {table_name} {col_names[0]}
                    VALUES {col_names[1]}
                    """
    new_values = extract_dict['met_past_24h'](json_line)

    try:
        with mariadb.connect(host = 'localhost',
                    user = os.getenv('MYSQL_USER'),
                    password = os.getenv('MYSQL_PASS'),
                    database = 'weather_comp') as connection:
            cur = connection.cursor()
            cur.executemany(insert_query, new_values)
            connection.commit()
    except mariadb.Error as e:
        print(e)

# for line in read_every_line('data/met_past_24h.jsonl'):
#     print(line)

# line = read_last_line('data/met_past_24h.jsonl')
# sql_add_data('met_past_24h', line)

# print(met_past_24h_extract(line))

# for h in met_past_24h_extract(line):
#     print(h)