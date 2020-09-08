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
import keras
import pandas as pd
import datetime
import time
from time import sleep
import schedule
import scipy.stats

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

    common_features=[feature_max,feature_min,powermax,powermin]
    return x_train, x_test, y_train, y_test,common_features


#%%
# select features for training
scenarios = {
    'whole': ['Ghi', 'Ebh', 'Dni', 'Dhi', 'AirTemp', 'CloudOpacity'],
    'radiations':['Ghi', 'Ebh', 'Dni', 'Dhi'],
    'normal':['Ghi', 'AirTemp', 'CloudOpacity'],
    'minimal':['Ghi', 'CloudOpacity'],
    'Ghi':['Ghi']
}
#%%
mses={}
for sc in scenarios:
    if sc == 'normal':
        print(sc)
        selected_features = scenarios[sc]

        feature_numbers = len(selected_features)
        resolution = 24
        x_train, x_test, y_train, y_test, common_features = train_test_by_features(selected_features, hist, etap_power)
        feature_max, feature_min, powermax, powermin = common_features
        loaded_model = keras.models.load_model('models/'+sc)
        print(loaded_model)
        predicted = loaded_model.predict(x_train)
        mse_error = loaded_model.evaluate(x_train, y_train)
        print(mse_error)
        mses[sc] = mse_error[0]

#%%
## prediciton error normal pdf
error = predicted - y_train
error = error.ravel()
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

data = error

# Fit a normal distribution to the data:
mu, std = norm.fit(data)

# Plot the histogram.
plt.hist(data,bins=30, density=True,  color='blue')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'r', linewidth=2)
title = "Error fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)
plt.legend(['normal pdf fitted for error','normalized error histogram'])
plt.savefig('figs/errorhist.png')
plt.show()
#%%
#prediciton plot
for i, k in enumerate(predicted):
    plt.plot((y_train[i] * (powermax - powermin) + powermin)*1000)
    plt.plot((predicted[i] * (powermax - powermin) + powermin)*1000)
    plt.ylabel('Power(kW)')
    plt.xlabel('Hour of the day')
    plt.legend(['ETAP real solar generation','Predicted solar generation'])
    plt.savefig('figs/realpred/' + str(i) + '.png')
    plt.show()
#%%







    #%%
from keras.models import Model, Sequential
from keras import backend as K


def create_dropout_predict_function(model, dropout):
    """
    Create a keras function to predict with dropout
    model : keras model
    dropout : fraction dropout to apply to all layers

    Returns
    predict_with_dropout : keras function for predicting with dropout
    """

    # Load the config of the original model
    conf = model.get_config()
    # Add the specified dropout to all layers
    for layer in conf['layers']:
        # Dropout layers
        if layer["class_name"] == "Dropout":
            layer["config"]["rate"] = dropout
            print('config-rate')
        # Recurrent layers with dropout
        elif "dropout" in layer["config"].keys():
            layer["config"]["dropout"] = dropout
            print(layer["config"]["dropout"],'config-droupout')
    # Create a new model with specified dropout
    if type(model) == Sequential:
        # Sequential
        newmodel = keras.models.clone_model(model)
        # newmodel.compile(optimizer='adam',
        #                     loss='mse',
        #                     metric='mse')
        # newmodel.set_weights(model.get_weights())

        model_dropout = Sequential.from_config(conf)
        # print('model1')
    else:
        # Functional
        model_dropout = Model.from_config(conf)
        # print('model2')

    model_dropout.set_weights(model.get_weights())
    # model_dropout.compile(optimizer='adam',
    #                       loss='mse')

    # final_conv_layer = get_output_layer(model, "conv5_3")
    # get_output = K.function([model.layers[0].input],
    #                         [final_conv_layer.output, model.layers[-1].output])
    # [conv_outputs, predictions] = get_output([img])
    # Create a function to predict with the dropout on
    predict_with_dropout = K.function([model_dropout.layers[0].input,K.learning_phase()],
                                      [model_dropout.layers[-1].output])

    return predict_with_dropout

#%%
def mc(x_train, iternum, drop):
    mcpred = {}
    prediction_with_dropout = create_dropout_predict_function(loaded_model, drop)
    for i in range(x_train.shape[0]):
        mcpred[i] = []

    for i in range(iternum):
        y = prediction_with_dropout([x_train, 1])
        for j in range(y[0].shape[0]):
            mcpred[j].append((y[0][j] * (powermax - powermin) + powermin)*1000)
    return mcpred
#%%
def ReLU(x):
    a=[]
    for i in x:
        a.append(max(i,0))
    return a
def mean_confidence_interval(data, zp):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a,axis=0), np.std(a,axis=0)
    h = se* zp/2
    return m, ReLU(m-h), m+h

def confidence_intervals(mcpred, zp):
    CItrain = {}
    for i in range(len(mcpred)):
        mn, lower, upper = mean_confidence_interval(mcpred[i],zp)
        CItrain[i] = [lower, upper ]
    return CItrain

#%%
dropout_levels = [0.1, 0.2, 0.3, 0.4]
CI_level = [0.8, 0.9, 0.95]
zp =[1.28, 1.64, 1.96]
iternum=50

results = {}
for drop in dropout_levels:
    print(drop)
    results[drop] = {}
    mcpred = mc(x_train, iternum,drop)
    for level in zp:
        print(level)
        ci = confidence_intervals(mcpred, level)
        results[drop][level] = ci


#%%
for j in zp:
    os.mkdir('figs/confidence/' + str(j))
    for i in range(16):
        temp = results[0.1][j]
        plt.plot(temp[i][0])
        plt.plot(temp[i][1])
        plt.plot((predicted[i]* (powermax - powermin) + powermin)*1000)
        plt.plot((y_train[i]* (powermax - powermin) + powermin)*1000)
        plt.legend(['lower bound', 'higher bound', 'prediction', 'real'])
        plt.ylabel('Power(kW)')
        plt.xlabel('Hour of the day')
        plt.savefig('figs/confidence/' + str(j) + '/' + str(i) + '.png')
        plt.show()

