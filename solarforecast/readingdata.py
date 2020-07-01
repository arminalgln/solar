# =============================================================================
# Liberaries
# =============================================================================
import pandas as pd
import os  #access files and so on
import sys #for handleing exceptions
import re #for checking letter in a string

class FileInf():
    
    def __init__(self,directory):
        self.dir=directory
        self.files=os.listdir(self.dir)

    def directory(self):
        print('This is the directory yo are lpooking for data: ', self.dir)
        return self.dir
    def data_files(self):
        print('All the data files in resource: ',self.files)
        return self.files
    def load_data(self,file):
        print(file)
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
        
# =============================================================================
# =============================================================================
# =============================================================================
# # # Detal for data      
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
