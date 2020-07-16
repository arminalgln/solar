import json
import time
import urllib.request
import solcast

from opencage.geocoder import OpenCageGeocode

#%%
# =============================================================================
# take address and return lat and lng
# =============================================================================
address=input('What is your address?  ')
location_api_key='23e6edd3ccc7437b90c589fd7c9c6213'
geocoder = OpenCageGeocode(location_api_key)

whole_location_info = geocoder.geocode(address)[0]
geo=whole_location_info['geometry']
lat,lng=geo['lat'],geo['lng']


#%%
# =============================================================================
# get lat and lng and return forecast irredication data
# =============================================================================
solcast_API_key='osmO54Z_7TKYMgJFi3vrQenczYLbErBk'

radiation_forecasts = solcast.get_radiation_forecasts(lat, lng, solcast_API_key)
radiation_forecasts_data=pd.DataFrame(radiation_forecasts.forecasts)


radiation_actuals = solcast.RadiationEstimatedActuals(lat, lng, solcast_API_key)
radiation_actuals_data=pd.DataFrame(radiation_forecasts_actuals.estimated_actuals)
#%%
# =============================================================================
# load historical data solcast
# =============================================================================
historical=pd.read_csv('data/solcast_etap_historical.csv')
historical .keys()




#%%
plt.plot(radiation_forecasts_data['cloud_opacity'])
# plt.plot(radiation_forecasts_data['ghi90'])
# plt.plot(radiation_forecasts_data['ghi10'])
plt.plot(radiation_actuals_data['cloud_opacity'])
plt.legend(['scenario','actual'])
plt.show()



#%%


# #%%
# country_code='US'
# city=input('City Name')
# # city='Riverside'
# def get_location(country_code,city):
    
#     search_address="http://dataservice.accuweather.com/locations/v1/cities/"+country_code+"/search?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&q="+city+""
#     # print(search_address)
#     with urllib.request.urlopen(search_address) as search_address:
#         # print(search_address)
#         data=json.loads(search_address.read().decode())
#     # print(data)
#     return data[0]['Key']
#     # print(location_key)
    
    
# # def get_forecast(location_key):
# #     12_daily_forecast="http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"+location_key+"?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&details=true"
# #     with urllib.request.urlopen(12_daily_forecast) as 12_daily_forecast:
# #         data=json.loads(12_daily_forecast.read().decode())
# #     return data

# def get_historical(location_key):
#     historical="http://dataservice.accuweather.com/currentconditions/v1/"+location_key+"/historical/24?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&details=true"
#     with urllib.request.urlopen(historical) as historical:
#         data=json.loads(historical.read().decode())
#     return data
# location_key=get_location(country_code, city)
# # data=get_forecast(location_key)
# historical=get_historical(location_key)
# #%%
# for i in historical:
#     print(i['CloudCover'])

