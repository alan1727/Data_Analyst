import pandas as pd
import pandasql
import numpy as np
import csv
import math


# 2.1
# Run a SQL query on a dataframe to get the number of rainy days 
def num_rainy_days(filename):
    weather_data = pd.read_csv(filename)
    
    q = """
    SELECT
    COUNT(rain)
    FROM
    weather_data
    WHERE
    rain = 1
    """
    
    # Execute the SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days


# 2.2
# Run a SQl query on a dataframe to get the maximum max temperature for both foggy and non-foggy days
def max_temp_aggregate_by_fog(filename):
    weather_data = pd.read_csv(filename)
    
    q = """
    SELECT 
    fog, MAX(maxtempi)
    FROM
    weather_data
    GROUP BY
    fog
    """
    
    # Execute the SQL command against the pandas frame
    foggy_days = pandasql.sqldf(q.lower(), locals())
    return foggy_days


# 2.3
# Run a SQL query on a dataframe to get the average mean temperature on weekends
def avg_weekend_temperature(filename):
    weather_data = pd.read_csv(filename)
    
    q = """
    SELECT 
    AVG(meantempi)
    FROM 
    weather_data
    WHERE
    CAST(STRFTIME('%w',date) as INTEGER) = 0 
    OR
    CAST(STRFTIME('%w',date) as INTEGER) = 6
    """
    
    #Execute the SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends


# 2.4
# Run a SQL query on a dataframe to get the average minimum temperature on rainy days 
# where the minimum temperature is greater than 55 degrees
def avg_min_temperature(filename):
    weather_data = pd.read_csv(filename)
    
    q = """
    SELECT 
    AVG(mintempi)
    FROM
    weather_data
    WHERE
    rain = 1
    AND
    mintempi > 55
    """
    
    #Execute the SQL command against the pandas frame
    avg_min_temp_rainy = pandasql.sqldf(q.lower(), locals())
    return avg_min_temp_rainy


# 2.5
# Update each row in the text files so there is only one entry per row.
def fix_turnstile_data(filenames):
    for name in filenames:
        updated_file = "updated_" + name
        # Open one file from the file list
        f_in = open(name, 'r')
        # Create a new file
        f_out = open(updated_file, 'w')
        
        # Read the old file
        read_in = csv.reader(f_in, delimiter=',')
        # Ready to write new file
        write_out = csv.writer(f_out, delimiter=',')
        
        # Read the old file line by line, every line is a list
        for line in read_in:
                id0 = line[0]
                id1 = line[1]
                id2 = line[2]
                i = 3 
                while i < len(line):
                    # The first 3 elements of new lines are same like the old line.
                    line_new = [id0,id1,id2,line[i],line[i+1],line[i+2],line[i+3],line[i+4]]
                    # Write the new line.
                    write_out.writerow(line_new)
                    i = i + 5
        
        #Close the old and new files
        f_in.close()
        f_out.close()



# 2.6
# Combining Turnstile Data
def create_master_turnstile_file(filenames, output_file):
    f_out = open(output_file, 'w')
    writer_out = csv.writer(f_out, delimiter=',')
    row1 = ["C/A", "UNIT", "SCP", "DATEn", "TIMEn", "DESCn", "ENTRIESn", "EXITSn"]
    writer_out.writerow(row1)
    
    for name in filenames:
        f_in = open(name, 'r')
        read_in = csv.reader(f_in, delimiter=',')
        for line in read_in:
            writer_out.writerow(line)
        f_in.close()
    
    f_out.close()


# 2.7
# Filtering Irregular Data
def filter_by_regular(filename):
    turnstile_data = pd.read_csv(filename)
    q = """
    SELECT
    * 
    FROM
    turnstile_data
    WHERE
    DESCn = 'REGULAR'
    """
    turnstile_data = pandasql.sqldf(q.lower(), locals())
    return turnstile_data


# 2.8
# Get hourly entries
def get_hourly_entries(df):
    df['ENTRIESn_hourly'] = 1
    i = 1
    while i < len(df.index):
        val1 = df.iat[i,7]
        val2 = df.iat[i-1,7]
        # The difference between ENTRIESn of the current row 
        # and the previous row
        diff = int(val1) - int(val2)
        if math.isnan(diff):
            df.iat[i,9] = 1
        else:
            df.iat[i,9] = diff
        i = i + 1
    return df


# 2.9
# Get hourly exits
def get_hourly_exits(df):
    df['EXITSn_hourly'] = 0
    i = 1
    while i < len(df.index):
        val1 = df.iat[i,8]
        val2 = df.iat[i-1,8]
        # The difference between EXITSn of the current row 
        # and the previous row
        diff = int(val1) - int(val2)
        if math.isnan(diff):
            df.iat[i,10] = 0
        else:
            df.iat[i,10] = diff
        i = i + 1
    return df


# 2.10
# Extract the hour part from the input variable time
# and return it as an integer
def time_to_hour(t):
    string_to_time = time.strptime(t, "%H:%M:%S")
    hour = int(time.strftime("%H",string_to_time))
    return hour


# 2.11
# Reformat Subway Dates
def reformat_subway_dates(date):
    string_to_time = time.strptime(date, "%m-%d-%y")
    date_formatted = time.strftime("%Y-%m-%d",string_to_time)
    return date_formatted

