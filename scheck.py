import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
#%%

# sheet1, sheet2 = None, None
main_data={}
with pd.ExcelFile(r'data/Solar-MW.xls') as reader:
    for i,k in enumerate(reader.sheet_names):
        main_data[i]=pd.read_excel(reader, sheet_name=k,header=1)
        

etap_weather={}
with pd.ExcelFile(r'data/Solar-Weather.xls') as reader:
    for i,k in enumerate(reader.sheet_names):
        etap_weather[i]=pd.read_excel(reader, sheet_name=k, header=[0,1])

#%%
#timestamp
for i in main_data:
    new_time=[]
    if 'Time' in main_data[i]:
        for ind,j in enumerate(main_data[i]['Time']):
            date = datetime.datetime.strptime(j, '%m/%d/%Y %I:%M:%S %p')
            ts = datetime.datetime.timestamp(date)
            new_time.append(ts)
    main_data[i]['t']=new_time
    
#%%
for i in etap_weather:
    new_time=[]
    if '381 (WeatherStation - WeatherStation - SolarRadiation)' in etap_weather[i]:
        if 'Time' in etap_weather[i]['381 (WeatherStation - WeatherStation - SolarRadiation)']:
            times=etap_weather[i]['381 (WeatherStation - WeatherStation - SolarRadiation)']['Time']
            for ind,j in enumerate(times):
                date = datetime.datetime.strptime(j, '%m/%d/%Y %I:%M:%S %p')
                ts = datetime.datetime.timestamp(date)
                new_time.append(ts)
            for key in etap_weather[i].keys().get_level_values(0).unique():
                etap_weather[i][key,'t']=new_time

#%%
forecast=pd.read_csv('data/GetWeatherSiteForecast.csv')

historical=pd.read_csv('data/hist.csv')

ts=[]
for i in historical['PeriodEnd']:
    date = datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ')
    t=datetime.datetime.timestamp(date)-7*3600
    ts.append(t)

historical['t']=ts


#%%
start='2020-05-11'
end='2020-05-22'

start_date=datetime.datetime.strptime(start, '%Y-%m-%d')
end_date=datetime.datetime.strptime(end, '%Y-%m-%d')


start_date=datetime.datetime.timestamp(start_date)
end_date=datetime.datetime.timestamp(end_date)

#%%

july=historical.loc[(historical['t']>start_date) & (historical['t']<end_date)]
etap_jul=main_data[5].loc[(main_data[5]['t']>start_date) & (main_data[5]['t']<end_date)]



plt.plot(list((etap_solar_jul['Avg']-etap_solar_jul['Avg'].mean())/(etap_solar_jul['Avg'].max()-etap_solar_jul['Avg'].min())))
# plt.show()
plt.plot(list((july['Ghi']-july['Ghi'].mean())/(july['Ghi'].max()-july['Ghi'].min())))

#%%

july=historical.loc[(historical['t']>start_date) & (historical['t']<end_date)]
etap_solar=etap_weather[5]['381 (WeatherStation - WeatherStation - SolarRadiation)']
etap_solar_jul=etap_solar.loc[(etap_solar['t']>start_date) & (etap_solar['t']<end_date)]

plt.plot(list(etap_solar_jul['Avg']))
plt.plot(list(july['Ghi']))
# plt.plot(list(july['Dni']))
# plt.plot(list(july['Dhi']))
# plt.plot(list(july['Ebh']))

# plt.legend(['etap','Ghi','Dni', 'Dhi', 'Ebh'])

#%%
def C2F(Celsius):
    Fahrenheit = [((i*9/5)+32) for i in Celsius]
    return Fahrenheit
#%%
july=historical.loc[(historical['t']>start_date) & (historical['t']<end_date)]
etap_temp=etap_weather[5]['384 (WeatherStation - WeatherStation - TempOutside)']
etap_temp_jul=etap_temp.loc[(etap_temp['t']>start_date) & (etap_temp['t']<end_date)]

plt.plot(list(etap_temp_jul['Avg']))
plt.plot(list(C2F(july['AirTemp'])))
# plt.plot(list(july['Dni']))
# plt.plot(list(july['Dhi']))
# plt.plot(list(july['Ebh']))

# plt.legend(['etap','Ghi','Dni', 'Dhi', 'Ebh'])











