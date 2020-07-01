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
main_data_directory=os.path.join(os.getcwd(),"solarforecast\data")
resource=FileInf(main_data_directory)
data_files=resource.files
#NREL data
selected_file=data_files[1]
selected_data=resource.load_data(selected_file)
#%%
x_train,y_train,x_dev,y_dev,x_test,y_test=resource.train_dev_test(selected_file,train=0.9,dev=0.1,test=0.1)
#%%

# =============================================================================
# solar forecaster instance
# =============================================================================
# solar forcaster object
solar_forecaster=SolarF()
#define compile parameters
solar_forecaster.opt_ls_mtr(optimizer='adam',
                            loss='mse',
                            metric='mse')
# #train
#%%
# y_train=y_train.reshape(327,48,1)
solar_forecaster.train(x_train, y_train, batch=1, epoch=1) 
#evaluation on train set
solar_forecaster.solar_eval(x_train, y_train)
# #evaluation on dev set
# solar_forecaster.solar_eval(x_dev, y_train)


#%%
#prediction
# solar_forecaster.solar_predict(x_pred)
selected_data.head()