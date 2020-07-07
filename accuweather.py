import json
import time
import urllib.request



#%%
API='f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7'
country_code='US'
# city=input('City Name')
city='Riverside'
def get_location(country_code,city):
    
    search_address="http://dataservice.accuweather.com/locations/v1/cities/US/search?apikey=f7p6tZSmiDE0F4xF0nLMH44qGJYSJhY7&q=Riverside"
    print(search_address)
    with urllib.request.urlopen(search_address) as search_address:
        print(search_address)
        data=json.loads(search_address.read().decode())
    print(data)
    
get_location(country_code, city)