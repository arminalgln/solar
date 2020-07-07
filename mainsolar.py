from solarforecast import FileInf
import os  #access files and so on
import matplotlib
import matplotlib.pyplot as plt
from solarforecast import SolarF
import pandas as pd


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
                            ,train=0.8,dev=0.1,test=0.1)
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
pred=solar_forecaster.solar_predict(x_test)
for i,k in enumerate(pred):
    # print(i[30])
    # plt.plot(x_train[i])
    plt.plot(y_test[i])
    plt.plot(pred[i])
    plt.show()
# selected_data.head()