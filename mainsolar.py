import importlib
import solarforecast
import tensorflow as tf
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
# import keras
import pandas as pd
import datetime
import time
from time import sleep
import schedule
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#%%

#%%
####################################################
####################################################
####################################################
"""

Solar forecasting

"""
####################################################
####################################################
####################################################
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

%reload_ext solarforecast

etap_power=EtapData(0.8)
train_times = etap_power.train_data.keys()
test_times = etap_power.test_data.keys()
#historical data from solcast
dst='data/solcast_etap_historical.csv'
hist = SolcastHistorical(dst, train_times, test_times)

#%%
def train_test_by_features(selected_features, hist, etap_power):

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

    return x_train, x_test, y_train, y_test

# def normaly(x):
#     return [(i-min(x))/(max(x)-min(x)) for i in x]
#
# #%%
# samples=range(2)
# for sample in samples:
#     plt.plot((x_train[sample][:,0]))
#     plt.plot((y_train[sample]))
#     plt.legend(['f','p'])
#     plt.show(block=True)
#     plt.interactive(False)
# MSE_of_scenarios = {
#     'whole': 0.0012270294828340411,
#     'radiations': 0.018972916528582573,
#     'normal': 0.0009280733065679669,
#     'minimal': 0.0010660196421667933,
#     'Ghi': 0.0014592972584068775
#     }
#%%
# select features for training
scenarios = {
    'whole': ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity'],
    'radiations':['Ghi', 'Ebh', 'Dni', 'Dhi'],
    'normal':['Ghi', 'AirTemp', 'CloudOpacity'],
    'minimal':['Ghi', 'CloudOpacity'],
    'Ghi':['Ghi']
}

for sc in scenarios:
    print(sc)
    selected_features = scenarios[sc]

    feature_numbers=len(selected_features)
    resolution=24
    x_train, x_test, y_train, y_test = train_test_by_features(selected_features, hist, etap_power)
    solar_forecaster = SolarF(feature_numbers,resolution)

    solar_forecaster.opt_ls_mtr(optimizer='adam',
                                loss='mse',
                                metric='mse')
# #train

    # y_train=y_train.reshape(327,48,1)
    solar_forecaster.train(x_train, y_train, batch=1, epoch=100)
    #evaluation on train set
    solar_forecaster.solar_eval(x_train, y_train)
    # #evaluation on dev set

    solar_forecaster.solar_eval(x_train, y_train)
    # solar_forecaster.solar_eval(x_dev, y_dev)
    solar_forecaster.solar_eval(x_test, y_test)

    # solar_forecaster.model.save('models/'+sc)


#%%
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)
#%%
feature_numbers=3
resolution=24
scenarios = {
    'whole': ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity'],
    'radiations':['Ghi', 'Ebh', 'Dni', 'Dhi'],
    'normal':['Ghi', 'AirTemp', 'CloudOpacity'],
    'minimal':['Ghi', 'CloudOpacity'],
    'Ghi':['Ghi']
}
selected_features = scenarios['normal']
x_train, x_test, y_train, y_test = train_test_by_features(selected_features, hist, etap_power)
solar_forecaster = SolarF(feature_numbers,resolution)


solar_forecaster.opt_ls_mtr(optimizer='adam',
                            loss='mse',
                            metric='mse')
# #train

# y_train=y_train.reshape(327,48,1)
solar_forecaster.train(x_train, y_train, batch=1, epoch=100)
#evaluation on train set
solar_forecaster.solar_eval(x_train, y_train)
# #evaluation on dev set

solar_forecaster.solar_eval(x_train, y_train)
# solar_forecaster.solar_eval(x_dev, y_dev)
solar_forecaster.solar_eval(x_test, y_test)

# solar_forecaster.model.save('models/whole_features')

#%%
scenarios = {
    'whole': ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity'],
    'radiations':['Ghi', 'Ebh', 'Dni', 'Dhi'],
    'normal':['Ghi', 'AirTemp', 'CloudOpacity'],
    'minimal':['Ghi', 'CloudOpacity'],
    'Ghi':['Ghi']
}

## loading model and compare their performance
mses={}
for sc in scenarios:
    if sc == 'normal':
        print(sc)
        selected_features = scenarios[sc]

        feature_numbers = len(selected_features)
        resolution = 24
        x_train, x_test, y_train, y_test = train_test_by_features(selected_features, hist, etap_power)

        loaded_model = keras.models.load_model('models/'+sc)
        print(loaded_model)
        predicted = loaded_model.predict(x_test)
        mse_error = loaded_model.evaluate(x_test, y_test)
        print(mse_error)
        mses[sc] = mse_error[0]
        # os.mkdir('models/figs/'+sc)
        # for i, k in enumerate(predicted):
        #     print(i)
        #     plt.plot(y_test[i])
        #     plt.plot(predicted[i])
        #     plt.legend(['real', 'pred'])
        #     plt.savefig('models/figs/' + sc + '/' + str(i) + '.png')
        #     plt.show()





#%%
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
#saving keras model
solar_forecaster.model.save('models/whole_features')
#%%
loaded=keras.models.load_model('models/normal')
#%%
a=2




