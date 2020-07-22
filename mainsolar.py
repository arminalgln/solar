import importlib
import solarforecast
solarforecast = importlib.reload(solarforecast)
from solarforecast import FileInf
from solarforecast import SolcastHistorical
from solarforecast import SolcastDataForecast
from solarforecast import EtapData
import os  #access files and so on
import matplotlib
import matplotlib.pyplot as plt
from solarforecast import SolarF
import numpy as np
import pandas as pd
import datetime
import time
from time import sleep
import schedule
#%%
%reload_ext solarforecast

etap_power=EtapData(0.9)
train_times = etap_power.train_data.keys()
test_times = etap_power.test_data.keys()
#historical data from solcast
dst='data/solcast_etap_historical.csv'
hist = SolcastHistorical(dst, train_times, test_times)

#%%
forecasted_features = ['Ghi', 'Ghi90', 'Ghi10', 'Ebh', 'Dni', 'Dni10', 'Dni90', 'Dhi',
       'air_temp', 'Zenith', 'Azimuth', 'cloud_opacity', 'period_end',
       'Period']
historical_features = ['PeriodEnd', 'PeriodStart', 'Period', 'AirTemp', 'AlbedoDaily',
       'Azimuth', 'CloudOpacity', 'DewpointTemp', 'Dhi', 'Dni', 'Ebh', 'Ghi',
       'PrecipitableWater', 'RelativeHumidity', 'SnowDepth', 'SurfacePressure',
       'WindDirection10m', 'WindSpeed10m', 'Zenith']

whole_training_features = ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity'] #for today which will predict tomorrow
output_feature = ['PV_power']#for the next day power generation

# select features for training
selected_features = ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity']
feature_numbers=len(selected_features)
resolution=24

train_features = []
train_label = []
for i in hist.train.keys():
    selected_data = hist.train[i][selected_features]
    train_features.append(selected_data.values)
    train_label.append(etap_power.train_data[i]['Avg'].values)

train_features = np.array(train_features)
train_label = np.array(train_label)

test_features = []
test_label = []
for i in hist.test.keys():
    selected_data = hist.test[i][selected_features]
    test_features.append(selected_data.values)
    test_label.append(etap_power.test_data[i]['Avg'].values)

test_features = np.array(test_features)
test_label = np.array(test_label)
#%%
#max min normalization
powermax = np.max(train_label)
powermin = np.min(train_label)

feature_max = train_features.max(axis=(1,0))
feature_min = train_features.min(axis=(1,0))

##normalize
x_train = (train_features-feature_min)/(feature_max-feature_min)
x_test = (test_features-feature_min)/(feature_max-feature_min)

y_train = (train_label-powermin)/(powermax-powermin)
y_test = (test_label-powermin)/(powermax-powermin)

#%%
def normaly(x):
    return [(i-min(x))/(max(x)-min(x)) for i in x]

#%%
samples=range(2)
for sample in samples:
    plt.plot((x_train[sample][:,0]))
    plt.plot((y_train[sample]))
    plt.legend(['f','p'])
    plt.show(block=True)
    plt.interactive(False)

#%%

solar_forecaster = SolarF(feature_numbers,resolution)

solar_forecaster.opt_ls_mtr(optimizer='adam',
                            loss='mse',
                            metric='mse')
# #train
#%%
# y_train=y_train.reshape(327,48,1)
solar_forecaster.train(x_train, y_train, batch=1, epoch=100)
#evaluation on train set
solar_forecaster.solar_eval(x_train, y_train)
# #evaluation on dev set

solar_forecaster.solar_eval(x_train, y_train)
# solar_forecaster.solar_eval(x_dev, y_dev)
solar_forecaster.solar_eval(x_test, y_test)


#prediction
pred = solar_forecaster.solar_predict(x_test)
for i, k in enumerate(pred):
    # print(i[30])
    # plt.plot(x_train[i])
    plt.plot(y_test[i])
    plt.plot(pred[i])
    plt.legend(['real','pred'])
    plt.show()
# selected_data.head()




#%%
# =============================================================================
# =============================================================================
# # select the data file needed
# =============================================================================
# =============================================================================



main_data_directory=os.path.join(os.getcwd(),"data")
resource=FileInf(main_data_directory)
data_files=resource.files
#NREL data
selected_file='NREL_etap_2015.csv'
selected_data=resource.load_data(selected_file)
#%%

# =============================================================================
# input and output selection
# =============================================================================
features=['Clearsky DHI','Clearsky DNI','Clearsky GHI',
          'DHI','DNI','GHI', 'Temperature','Cloud Type', 'Dew Point',
          'Fill Flag', 'Relative Humidity', 'Solar Zenith Angle',
          'Surface Albedo', 'Pressure', 'Precipitable Water', 'Wind Direction',
          'Wind Speed']

selected_features=['Clearsky DNI','DNI','Cloud Type','Temperature','Wind Speed']
selected_features=features
###############################################################################

outputs=['Clearsky DHI tmrw','Clearsky DNI tmrw','Clearsky GHI tmrw',
                      'DHI tmrw','DNI tmrw','GHI tmrw']
selected_output=['DNI tmrw']
###############################################################################
feature_numbers=len(selected_features)

# output_numbers=len(selected_output)

# sample_number=x_train.shape[0]
# sample_length=x_train.shape[1]
resolution=48



x_train,y_train,x_dev,y_dev,x_test,y_test=resource.train_dev_test(selected_file,
                            selected_features,selected_output, resolution
                            , train=0.8, dev=0.1, test=0.1)
#%%

# =============================================================================
# solar forecaster instance
# =============================================================================
# solar forcaster object

solar_forecaster=SolarF(feature_numbers,resolution)
#define compile parameters
solar_forecaster.opt_ls_mtr(optimizer='adam',
                            loss='mse',
                            metric='mse')
# #train
#%%
# y_train=y_train.reshape(327,48,1)
solar_forecaster.train(x_train, y_train, batch=10, epoch=5) 
#evaluation on train set
solar_forecaster.solar_eval(x_train, y_train)
# #evaluation on dev set
#%%
solar_forecaster.solar_eval(x_train, y_train)
solar_forecaster.solar_eval(x_dev, y_dev)
solar_forecaster.solar_eval(x_test, y_test)


#%%
#prediction
pred = solar_forecaster.solar_predict(x_test)
for i, k in enumerate(pred):
    # print(i[30])
    # plt.plot(x_train[i])
    plt.plot(y_test[i])
    plt.plot(pred[i])
    plt.show()
# selected_data.head()