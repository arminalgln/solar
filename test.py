from solarforecast import FileInf
import os
main_data_directory=os.path.join(os.getcwd(),"solarforecast\data")
resource=FileInf(main_data_directory)
resource.directory()
resource.data_files()