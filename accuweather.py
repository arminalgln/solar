import json
import time
import urllib.request



#%%
API='f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7'
country_code='US'
city=input('City Name')
# city='Riverside'
def get_location(country_code,city):
    
    search_address="http://dataservice.accuweather.com/locations/v1/cities/"+country_code+"/search?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&q="+city+""
    # print(search_address)
    with urllib.request.urlopen(search_address) as search_address:
        # print(search_address)
        data=json.loads(search_address.read().decode())
    # print(data)
    return data[0]['Key']
    # print(location_key)
    
    
# def get_forecast(location_key):
#     12_daily_forecast="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"+location_key+"?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&details=true"
#     with urllib.request.urlopen(12_daily_forecast) as 12_daily_forecast:
#         data=json.loads(12_daily_forecast.read().decode())
#     return data

def get_historical(location_key):
    historical="http://dataservice.accuweather.com/currentconditions/v1/"+location_key+"/historical/24?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&details=true"
    with urllib.request.urlopen(historical) as historical:
        data=json.loads(historical.read().decode())
    return data
location_key=get_location(country_code, city)
# data=get_forecast(location_key)
historical=get_historical(location_key)
#%%
for i in historical:
    print(i['CloudCover'])