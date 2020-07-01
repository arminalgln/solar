# =============================================================================
# =============================================================================
# # Change whole py extentions to txt and vise versa
# =============================================================================
# =============================================================================
import os
class FileExtentionChange():
    def __init__(self,dir):
        self.FileDirection=dir
        
    def PyToTxt(self):
        for file in os.listdir(self.FileDirection):
            Base = os.path.splitext(file)[0]
            # print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1]=='.py':
                os.rename(os.path.join(self.FileDirection, file), os.path.join(self.FileDirection, Base) + '.txt')
                print(file)
                
    def TxtToPy(self):
        for file in os.listdir(self.FileDirection):
            Base = os.path.splitext(file)[0]
            if os.path.splitext(file)[1]=='.txt':
                os.rename(os.path.join(self.FileDirection, file), os.path.join(self.FileDirection, Base) + '.py')
                print(file)

def office_py_txt():
    FileDirection=r'C:\Users\Armin.Aligholian\OneDrive - etap.com\ETAP research\forecasting\code\solarforecast'
    FileExtentionChange(FileDirection).PyToTxt()
    FileDirection=r'C:\Users\Armin.Aligholian\OneDrive - etap.com\ETAP research\forecasting\code'
    FileExtentionChange(FileDirection).PyToTxt()

def office_txt_py():
    FileDirection=r'C:\Users\Armin.Aligholian\OneDrive - etap.com\ETAP research\forecasting\code\solarforecast'
    FileExtentionChange(FileDirection).TxtToPy()
    FileDirection=r'C:\Users\Armin.Aligholian\OneDrive - etap.com\ETAP research\forecasting\code'
    FileExtentionChange(FileDirection).TxtToPy()

def home_py_txt():
    FileDirection=r'C:\Users\hamed\OneDrive - etap.com\ETAP research\forecasting\code\solarforecast'
    FileExtentionChange(FileDirection).PyToTxt()
    FileDirection=r'C:\Users\hamed\OneDrive - etap.com\ETAP research\forecasting\code'
    FileExtentionChange(FileDirection).PyToTxt()

def home_txt_py():
    FileDirection=r'C:\Users\hamed\OneDrive - etap.com\ETAP research\forecasting\code\solarforecast'
    FileExtentionChange(FileDirection).TxtToPy()
    FileDirection=r'C:\Users\hamed\OneDrive - etap.com\ETAP research\forecasting\code'
    FileExtentionChange(FileDirection).TxtToPy()

#%%
office_py_txt()
#%%
office_txt_py()
#%%
home_py_txt()
#%%
home_txt_py()
