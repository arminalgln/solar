from solarforecast import FileInf
import os  #access files and so on
import matplotlib
import matplotlib.pyplot as plt
from solarforecast import Solar

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
tt=resource.train_dev_test(selected_file)
#%%

print(selected_data.keys())
print(selected_data.head())
#%%

# =============================================================================
# solar forecaster instance
# =============================================================================
# solar forcaster object
solar_forecaster=Solar()
#define compile parameters
solar_forecaster.opt_ls_mtr(optimizer='adam',
                            loss='sparse_categorical_crossentropy',
                            metric='sparse_categorical_accuracy')
# #train
solar_forecaster.train(x_train, y_train, batch=12, epoch=5) 
#evaluation on train set
solar_forecaster.solar_eval(x_train, y_train)
#evaluation on dev set
solar_forecaster.solar_eval(x_dev, y_train)


#%%
#prediction
# solar_forecaster.solar_predict(x_pred)
sele