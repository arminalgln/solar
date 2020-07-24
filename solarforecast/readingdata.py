# =============================================================================
# Liberaries
# =============================================================================
import pandas as pd
import os  # access files and so on
import sys  # for handling exceptions
import re  # for checking letter in a string
import numpy as np
import random
import time
import xlrd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import solcast
from opencage.geocoder import OpenCageGeocode
import datetime
import math


class EtapData:

    def __init__(self, training_percentage):
        self.features = ['Avg', 't']
        self.train_chunk = training_percentage
        self.train_data, self.test_data = self.__train_test_data()

    def __get_data(self):

        etap_power = {}
        with pd.ExcelFile(r'data/etap_power.xls') as reader:
            for i, k in enumerate(reader.sheet_names):
                etap_power[i] = pd.read_excel(reader, sheet_name=k, header=1)

        # timestamp
        selected_output = pd.DataFrame(columns=self.features)
        for i in etap_power:
            new_time = []
            if 'Time' in etap_power[i]:
                for ind, j in enumerate(etap_power[i]['Time']):
                    date = datetime.datetime.strptime(j, '%m/%d/%Y %I:%M:%S %p')
                    ts = datetime.datetime.timestamp(date)
                    new_time.append(ts)
            etap_power[i]['t'] = new_time
            if not i == 0:
                # print(i)
                selected_output = selected_output.append(etap_power[i][self.features], ignore_index=True)
        return selected_output

    def __clean_data(self):
        data = self.__get_data()
        data = data.sort_values('t')
        data = data.reset_index()
        del data['index']
        t_index=[]
        for i, t in enumerate(data['t']):
            # if datetime.datetime.utcfromtimestamp(t).hour == 7:
            #     t_index.append(t)
            if time.localtime(t).tm_hour == 0:
                t_index.append(t)

        sectionized_data = {}
        count = 0
        for i, t in enumerate(t_index):
            if i < len(t_index)-1:
                start = t
                end = t_index[i+1]
                part = data.loc[(data['t'] >= start) & (data['t'] < end)]
                if part.shape[0] == 24:
                    sectionized_data[t] = part
                    count += 1
        return sectionized_data

    def __train_test_data(self):
        clean_data = self.__clean_data()
        data_indexes = list(clean_data.keys())
        train_sample_numbers = math.floor(self.train_chunk * len(data_indexes))
        random.seed(4)
        randomized_index = random.sample(data_indexes, train_sample_numbers)
        train_data = {i:clean_data.get(i) for i in randomized_index}
        test_index = [item for item in data_indexes if item not in randomized_index]
        test_data = {i:clean_data.get(i) for i in test_index}

        return train_data, test_data

class SolcastHistorical:
    def __init__(self, dst, train_index, test_index):
        self.train_index = train_index
        self.test_index = test_index
        self.dst = dst
        self.train,  self.test = self.__train_test_historical()

    def __time_add(self):
        historical = pd.read_csv(self.dst)
        ts = []
        for i in historical['PeriodEnd']:
            date = datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ')
            t = datetime.datetime.timestamp(date) - 7 * 3600  # Irvine to UTC difference
            ts.append(int(t))
        historical['t'] = ts
        return historical

    def __train_test_historical(self):

        historical = self.__time_add()

        train = {}
        count = 0
        for i, t in enumerate(self.train_index):
            start = t
            end = start + 24 * 3600
            part = historical.loc[(historical['t'] >= start) & (historical['t'] < end)]
            if part.shape[0] == 24:
                train[t] = part
                count += 1
        test = {}
        count = 0
        for i, t in enumerate(self.test_index):
            start = t
            end = start + 24 * 3600
            part = historical.loc[(historical['t'] >= start) & (historical['t'] < end)]
            if part.shape[0] == 24:
                test[t] = part
                count += 1

        return train, test




class SolcastDataForecast:
    
    def __init__(self, location_api_key, solcast_api_key, address):
        self.location_api_key = location_api_key
        self.solcast_api_key = solcast_api_key
        self.address = address

    def __get_address_lat_lng(self):
        geocoder = OpenCageGeocode(self.location_api_key)
        self.whole_location_info = geocoder.geocode(self.address)[0]
        geo = self.whole_location_info['geometry']
        lat,  lng = geo['lat'], geo['lng']
        self.lat = lat
        self.lng = lng
# location_api_key='23e6edd3ccc7437b90c589fd7c9c6213'

    def get_solcast_forecast(self):
        # solcast_API_key='osmO54Z_7TKYMgJFi3vrQenczYLbErBk'
        self.__get_address_lat_lng()
        radiation_forecasts = solcast.RadiationForecasts(self.lat, self.lng, self.solcast_api_key)
        self.forecasts_data=pd.DataFrame(radiation_forecasts.forecasts)
        radiation_actuals = solcast.RadiationEstimatedActuals(self.lat, self.lng, self.solcast_api_key)
        self.actuals_data=pd.DataFrame(radiation_actuals.estimated_actuals)
        self.__local_time()

    def __local_time(self):
        #timezonefinder and get append UNIX time as well
        temp_time=[]
        desired_tz=self.whole_location_info['annotations']['timezone']['name']
        def utc_to_local(utc_dt,desired_tz):
            return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=desired_tz)
        for t in self.actuals_data['period_end']:
            temp_time.append(utc_to_local(t,desired_tz))
        
        self.actuals_data['local_time']=temp_time
        
        temp_time=[]
        desired_tz=self.whole_location_info['annotations']['timezone']['name']
        for t in self.forecasts_data['period_end']:
            temp_time.append(utc_to_local(t,desired_tz))
        
        self.forecasts_data['local_time'] = temp_time



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
                    self.data=df
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
        
        return df
    
    
    def train_dev_test(self,file,features,output_f,resolution,**kwarg):
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
        k=data.keys()
        
        # data[k] = StandardScaler().fit_transform(data[k])            
        scaler = MinMaxScaler() 
        scaled_values = scaler.fit_transform(data) 
        data.loc[:,:] = scaled_values
        #irrediaction features for today
        
        
        
        feature_irradiations=data[['Clearsky DHI','Clearsky DNI','Clearsky GHI',
                      'DHI','DNI','GHI']].iloc[0:(data.shape[0]-resolution)]

        #features are for tomorrow 
        feature_weather=data[[ 'Temperature','Cloud Type', 'Dew Point',
               'Fill Flag', 'Relative Humidity', 'Solar Zenith Angle',
               'Surface Albedo', 'Pressure', 'Precipitable Water', 'Wind Direction',
           'Wind Speed']].iloc[resolution:(data.shape[0])]
        
        same_index=np.array(range(0,data.shape[0]-resolution))
        
        feature_irradiations.index=same_index
        feature_weather.index=same_index
        
        whole_features=pd.concat([feature_irradiations,feature_weather],axis=1)
        
        #should be forecasted
        output_irradiations=data[['Clearsky DHI','Clearsky DNI','Clearsky GHI',
                      'DHI','DNI','GHI']].iloc[resolution:(data.shape[0])]
        old_columns=[]
        new_columns=[]
        for i in output_irradiations:
            old_columns.append(i)
            new_columns.append(i+' tmrw')
        for i,k in enumerate(old_columns):
            output_irradiations.rename(columns={k:new_columns[i]},inplace=True)
        
        output_irradiations.index=same_index
        
        new_data=pd.concat([whole_features,output_irradiations],axis=1)
        new_data=np.array_split(new_data,np.floor(data.shape[0]/resolution-1))#one day shift for prediciton 
        
        
        
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
            x_train.append(i.loc[:,features].values)
            y_train.append(i.loc[:,output_f].values)
        x_train=np.array(x_train)
        y_train=np.array(y_train)
        
        
        x_dev=[]
        y_dev=[]
        for i in dev:
            x_dev.append(i.loc[:,features].values)
            y_dev.append(i.loc[:,output_f].values)
        x_dev=np.array(x_dev)
        y_dev=np.array(y_dev)
            
        x_test=[]
        y_test=[]
        for i in test:
            x_test.append(i.loc[:,features].values)
            y_test.append(i.loc[:,output_f].values)
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
