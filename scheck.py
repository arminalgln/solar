import pandas as pd
import numpy as np
#%%

# sheet1, sheet2 = None, None
main_data={}
with pd.ExcelFile(r'data/Solar-MW.xls') as reader:
    for i,k in enumerate(solar_etap_power.sheet_names):
        main_data[i]=pd.read_excel(reader, sheet_name=k,header=1)
    #%%
plt.plot(main_data[6]['Avg'])
#%%
forecast=pd.read_csv('data/GetWeatherSiteForecast.csv')

historical=pd.read_csv('data/hist.csv')
#%%
plt.plot(historical['Ghi'])
