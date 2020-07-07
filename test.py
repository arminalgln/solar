from solarforecast import FileInf
import os
main_data_directory=os.path.join(os.getcwd(),"data")
resource=FileInf(main_data_directory)
print(resource.dir)
print(resource.files)

