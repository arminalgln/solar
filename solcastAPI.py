import json
import time
import urllib.request
import solcast
from opencage.geocoder import OpenCageGeocode
from solarforecast import FileInf
from solarforecast import SolcastData
import os  #access files and so on
import matplotlib
import matplotlib.pyplot as plt
from solarforecast import SolarF
import pandas as pd
import datetime
from time import sleep
import schedule
#%%


def saving_task():      
    address='17 goodyear, Irvine'
    if not address:
        address=input('where is your site address?  ')
    location_api_key='23e6edd3ccc7437b90c589fd7c9c6213'
    solcast_API_key='osmO54Z_7TKYMgJFi3vrQenczYLbErBk'
    
    temp_data=SolacastData(location_api_key,solcast_API_key,address)
    # temp_data.get_address_lat_lng()
    temp_data.get_solcast_forecast()
    day=temp_data.forecasts_data['local_time'][1].strftime("%Y-%m-%d")
    f_dst='data/solcast/Irvine/forecast-'+day+'.pkl'
    a_dst='data/solcast/Irvine/actual-'+day+'.pkl'
    
    
    temp_data.forecasts_data.to_pickle(f_dst)
    temp_data.actuals_data.to_pickle(a_dst)
    print('the files for %s has been saved!'%day)
    
#%%
def show_sth():
    print('I am still working!!!')
    print(datetime.datetime.now())
#%%
schedule.clear()
schedule.every().day.at('00:00').do(saving_task)
schedule.every().hour.do(show_sth)

#%%
while True:
    schedule.run_pending()
    # time.sleep(60*60)

