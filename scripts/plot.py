#!/home/nikita/anaconda3/bin/python3.5

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import json
import os
from datetime import date
from time import sleep
from urllib.request import urlopen

counter = 0
while True:
    try:
        conn = psycopg2.connect("dbname='nikita_srv' host='10.100.82.141' user='nikita_srv'")
        break
    except:
        counter += 1
        sleep(10)
    if counter == 5:
        print("Can\'t connect to database!")
        sys.exit()

query = 'SELECT * FROM temperature WHERE date >= now()::date;'
#Loading csv and converting date to timestamp entries:
df = pd.read_sql(query, conn)
df['date'] = pd.to_datetime(df['date'])
#Creating variables for dates:
today = date.today().strftime('%Y-%m-%d')
#Uploading weather data
hostname = "google.com"
response = os.system("ping -c 1 -w2 "+hostname+" > /dev/null 2>&1")
if response == 0:
    data = urlopen('https://api.forecast.io/forecast/f4b2b876511f01f53ff2c7c29d10f43e/48.4753,35.1578,'+str(today)+'T08:00:00?units=si&exclude=minute,today,currently,daily,flags')
    raw_json = json.loads(data.read().decode('UTF-8'))
    df_weather = pd.DataFrame.from_dict(raw_json['hourly']['data'])
    df_weather['time'] = pd.to_datetime(df_weather['time'],unit='s')
    df_weather['time'] = df_weather['time'] + pd.Timedelta('03:00:00')
    plt.plot_date(df_weather['time'].iloc[8:23], df_weather['apparentTemperature'].iloc[8:23], xdate=True, ydate=False, color='red')
#Creating plot:
plt.plot_date(df['date'], df['temp'], xdate=True, ydate=False, color='green')
plt.ylim(0,60)
plt.xlim(['07:00:00','23:00:00'])
plt.xticks(rotation=60)
plt.grid(True)
#Saving plot to file:
plt.savefig('/home/nikita/shared/server_temperature/temperature_' + str(today) + '.png', bbox_inches='tight')

