# =============================================================================
# Liberaries
# =============================================================================
import pandas as pd
import os  #access files and so on
import sys #for handleing exceptions
import re #for checking letter in a string
import numpy as np
import random


class FileInf():
    
    def __init__(self,directory):
        self.dir=directory
        self.files=os.listdir(self.dir)

    def load_data(self,file):
        """

        Parameters
        ----------
        file : string
            selected dataset file.

        Returns
        -------
        df : pd.Datafframe
            dataset for the selected file.

        """
        print(file)
        self.file=file
        filepath=os.path.join(self.dir, file)
        try:
            #with regard to website file format
            if file.split('_')[0]=='JRC':
                with open(filepath) as fd:
                    headers = [ next(fd) for i in range(10) ]
                    df = pd.read_csv(fd)
                  
                  #remove descriptions of the file located at the end of the file
                while re.search('[a-zA-Z]', df.iloc[-1][0]):
                    df.drop(df.tail(1).index,inplace=True)
            
            elif file.split('_')[0]=='NREL':
                with open(filepath) as fd:
                    headers = [ next(fd) for i in range(2) ]
                    df = pd.read_csv(fd)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
        
        return df
    
    def train_dev_test(self,file,**kwarg):
        """
        

        Parameters
        ----------
        file : string
            selected data set .
        **kwarg : 0 - 1
            train, dedv and test percentage.

        Returns
        -------
        new_data : three array each of the are dataframe
            train, dedv and test sets.

        """
        train_chunk,dev_chunk,test_chunk=kwarg['train'],kwarg['dev'],kwarg['test']
        
        data=self.load_data(self.file)
            
        #irrediaction features for today
        feature_irradiations=data[['Clearsky DHI','Clearsky DNI','Clearsky GHI',
                      'DHI','DNI','GHI']].iloc[0:(data.shape[0]-48)]

        #features are for tomorrow 
        feature_weather=data[[ 'Temperature','Cloud Type', 'Dew Point',
               'Fill Flag', 'Relative Humidity', 'Solar Zenith Angle',
               'Surface Albedo', 'Pressure', 'Precipitable Water', 'Wind Direction',
           'Wind Speed']].iloc[48:(data.shape[0])]
        
        same_index=np.array(range(0,data.shape[0]-48))
        
        feature_irradiations.index=same_index
        feature_weather.index=same_index
        
        whole_features=pd.concat([feature_irradiations,feature_weather],axis=1)
        
        #should be forecasted
        output_irradiations=data[['Clearsky DHI','Clearsky DNI','Clearsky GHI',
                      'DHI','DNI','GHI']].iloc[48:(data.shape[0])]
        old_columns=[]
        new_columns=[]
        for i in output_irradiations:
            old_columns.append(i)
            new_columns.append(i+' tmrw')
        for i,k in enumerate(old_columns):
            output_irradiations.rename(columns={k:new_columns[i]},inplace=True)
        
        output_irradiations.index=same_index
        
        new_data=pd.concat([whole_features,output_irradiations],axis=1)
        new_data=np.array_split(new_data,np.floor(data.shape[0]/48-1))
        
        #shuffle data with seed
        random.seed(4)
        random.shuffle(new_data)
        
        size_data=len(new_data)
        trian_pointer=int(np.floor(train_chunk*size_data))
        dev_pointer=int(trian_pointer+np.floor(dev_chunk*size_data))
        
        train=new_data[0:trian_pointer]
        dev=new_data[trian_pointer:dev_pointer]
        test=new_data[dev_pointer:]
        
        x_train=[]
        y_train=[]
        for i in train:
            x_train.append(i.iloc[:,0:17].values)
            y_train.append(i.iloc[:,17].values)
        x_train=np.array(x_train)
        y_train=np.array(y_train)
        
        
        x_dev=[]
        y_dev=[]
        for i in dev:
            x_dev.append(i.iloc[:,0:17].values)
            y_dev.append(i.iloc[:,17:].values)
        x_dev=np.array(x_dev)
        y_dev=np.array(y_dev)
            
        x_test=[]
        y_test=[]
        for i in test:
            x_test.append(i.iloc[:,0:17].values)
            y_test.append(i.iloc[:,17:].values)
        x_test=np.array(x_test)
        y_test=np.array(y_test)
        
        tdt_output=[x_train,y_train,x_dev,y_dev,x_test,y_test]

        return tdt_output
    
    
    
    
    
    
    
# =============================================================================
# =============================================================================
# =============================================================================
# # # Detail for data      
# =============================================================================
# =============================================================================
# =============================================================================

#JRC
# =============================================================================
# =============================================================================
# # P: PV system power (W)
# Gb(i): Beam (direct) irradiance on the inclined plane (plane of the array) (W/m2)
# Gd(i): Diffuse irradiance on the inclined plane (plane of the array) (W/m2)
# Gr(i): Reflected irradiance on the inclined plane (plane of the array) (W/m2)
# H_sun: Sun height (degree)
# T2m: 2-m air temperature (degree Celsius)
# WS10m: 10-m total wind speed (m/s)
# Int: 1 means solar radiation values are reconstructed
# =============================================================================
# =============================================================================
