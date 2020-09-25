import json
import time
import urllib.request
import solcast
from opencage.geocoder import OpenCageGeocode
from solarforecast import FileInf
from solarforecast import SolcastDataForecast
from solarforecast import SolcastHistorical
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
        address = input('where is your site address?  ')
    location_api_key='23e6edd3ccc7437b90c589fd7c9c6213'
    solcast_API_key='osmO54Z_7TKYMgJFi3vrQenczYLbErBk'

    SDF = SolcastDataForecast(location_api_key, solcast_API_key, address)
    act, pred = SDF.get_solcast_forecast()
    day = pred['local_time'][1].strftime("%Y-%m-%d")
    f_dst = 'data/solcast/Irvine/forecast-' + day + '.pkl'
    a_dst = 'data/solcast/Irvine/actual-' + day + '.pkl'

    pred.to_pickle(f_dst)
    act.to_pickle(a_dst)
    print('the files for %s has been saved!' % day)
    
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

#%%
address = '17 goodyear, Irvine'
if not address:
    address = input('where is your site address?  ')
location_api_key = '23e6edd3ccc7437b90c589fd7c9c6213'
solcast_API_key = 'osmO54Z_7TKYMgJFi3vrQenczYLbErBk'


SDF = SolcastDataForecast(location_api_key, solcast_API_key, address)
act, pred = SDF.get_solcast_forecast()
# #%%
# temp_data = SolacastData(location_api_key, solcast_API_key, address)
# # temp_data.get_address_lat_lng()
# temp_data.get_solcast_forecast()
day = pred['local_time'][1].strftime("%Y-%m-%d")
f_dst = 'data/solcast/Irvine/forecast-' + day + '.pkl'
a_dst = 'data/solcast/Irvine/actual-' + day + '.pkl'

pred.to_pickle(f_dst)
act.to_pickle(a_dst)
print('the files for %s has been saved!' % day)
#%%
#7 days data for different sites with 6 kWh capacity

lats = [17.63506, 17.73534, 10.19835, 22.86274, 19.72728]
lngs = [94.58346, 96.22166, 98.60683, 93.62167, 97.07478]
caps = [6, 6, 6, 5.2, 6]






for i in range(len(lats)):
    lat = lats[i]
    lng = lngs[i]
    capacity = caps[i]
    hours = 168
    solcast_API_key = 'Cy_svKl2MNHobcsBWczeH-6MQ6cp2N6N'
    base_url_estimated = 'https://api.solcast.com.au//world_pv_power/estimated_actuals?' \
                         'latitude=%s&longitude=%s&capacity=%s&format=json&api_key=%s&hours=%s' % (
                         lat, lng, capacity, solcast_API_key, hours)

    weburl = urllib.request.urlopen(base_url_estimated)

    data = weburl.read()
    data = json.loads(data)
    data = pd.DataFrame(data['estimated_actuals'])

    data.to_csv('data/new_site/' + str(lat) + '-' + str(lng) + '-' + str(capacity) + 'past' +'.csv')

    plt.plot(data['pv_estimate'])
    plt.show()


    base_url_estimated = 'https://api.solcast.com.au//world_pv_power/forecasts?' \
                         'latitude=%s&longitude=%s&capacity=%s&format=json&api_key=%s&hours=%s' % (
                         lat, lng, capacity, solcast_API_key, hours)

    weburl = urllib.request.urlopen(base_url_estimated)

    data = weburl.read()
    data = json.loads(data)
    data = pd.DataFrame(data['forecasts'])

    data.to_csv('data/new_site/' + str(lat) + '-' + str(lng) + '-' + str(capacity) + 'forecasts' +'.csv')

    # plt.plot(data['pv_estimate'])
    # plt.show()

#%%
url = 'https://api.weather.com/v1/geocode/33.4/-117/forecast/hourly/24hour.json?units=m&language=en-US&apiKey=5424e9662cbf4bc3a4e9662cbf4bc3fe'

api_key = '5424e9662cbf4bc3a4e9662cbf4bc3fe'
url = 'https://api.weather.com/v1/geocode/33.4/117/forecast/hourly/6hour.json?units=m&language=en-US&apiKey=%s' %(api_key)

weburl = urllib.request.urlopen(url)
data = weburl.read()
data = json.loads(data)
#%%
data = pd.DataFrame(data['forecasts'])
data.to_csv('data/weatherCOM6dayshourly.csv')





























