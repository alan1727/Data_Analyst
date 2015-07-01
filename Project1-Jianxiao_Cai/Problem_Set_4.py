from pandas import *
from ggplot import *
import time
import numpy as np
import datetime

# 4.1 Get the mean hourly entries of days. The first 10 station will be compared.

def plot_weather_data(df):
    # select 10 stations as sample
    selected_subway_station = ['R001','R002','R003','R004','R005','R006','R007','R008','R009','R010']
    
    # choose the data of 10 stations
    df = df[df['UNIT'].isin(selected_subway_station)][['Hour','ENTRIESn_hourly','UNIT']]
    
    # Get the total entries of each station at different times
    df = df.groupby(['UNIT','Hour']).mean()
    
    # Reset the index
    df.reset_index(inplace = True)
    
    # Get the mean hourly entries 
    # df['ENTRIESn_hourly_mean'] = df['ENTRIESn_hourly'] / number_of_days
    plot = ggplot(aes(x='Hour',y='ENTRIESn_hourly',color='UNIT'),data=df) + \
           geom_point() + \
           geom_line() + \
           ggtitle("The mean hourly entries in may") + \
           xlab("Hours") + ylab("Hourly Entries") + \
           xlim(0,24) + ylim(0,10000)
    return plot



# 4.2 Get the mean entries of 6 hours of weekdays

def plot_weather_data2(df):
    # Select 10 stations to compare
    selected_subway_station = ['R001','R002','R003','R004','R005','R006','R007','R008','R009','R010']
    
    # Choose the data of 10 stations
    df = df[df['UNIT'].isin(selected_subway_station)][['UNIT','DATEn','ENTRIESn_hourly']]
    
    # Get the sum entries of 6 hours of each day 
    df = df.groupby(['UNIT','DATEn']).sum()
    
    # Reset index of dataframe
    df.reset_index(inplace = True)
    
    # Add a new column of weekday 
    df['weekday'] = df['DATEn'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').weekday()+1)
    
    # Delete column of date
    del df['DATEn']
    
    # Get the mean entries of 6 hours of weekdays
    df = df.groupby(['UNIT','weekday']).mean()
    
    # Reset index of dataframe
    df.reset_index(inplace = True)
    
    plot = ggplot(aes(x='weekday',y='ENTRIESn_hourly',color='UNIT'), data=df) + \
           geom_point() + \
           geom_line() + \
           ggtitle('The mean entries of 6 hours of weekdays') + \
           xlab("Weekdays") + ylab("Daily Entries") + \
           scale_x_continuous(breaks=[1,2,3,4,5,6,7],labels=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]) +            xlim(1,7) + ylim(0, 9000)
    return plot


