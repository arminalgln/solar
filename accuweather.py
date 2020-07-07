import json
import time
import urllib.request



#%%
API='f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7'
country_code='US'
# city=input('City Name')
city='Riverside'
def get_location(country_code,city):
    
    search_address="http://www.accuweather.com/en/us/riverside-ca/92506/hourly-weather-forecast/327146?day=1&hbhhour=20&lang=en-us"
    print(search_address)
    with urllib.request.urlopen(search_address) as search_address:
        print(search_address)
    #     data=json.loads(search_address.read().decode())
    # print(data)
    
get_location(country_code, city)