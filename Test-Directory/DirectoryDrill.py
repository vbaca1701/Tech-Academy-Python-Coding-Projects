import os
from datetime import datetime


fPath = 'C:\\Test-Directory\\'
directoryList = os.listdir(fPath) #Creates list of files in the specified directory.
print("These are the files in the path, {} :\n\n{}\n\n".format(fPath,directoryList))

for file in directoryList:
    if file.endswith('.txt'):
        abPath = os.path.join(fPath, file) #Concatinates the path directory with a txt file found through each iteration. 
        fModTime = os.path.getmtime(abPath) #Retrieves last modified time
        formattedTime = datetime.fromtimestamp(fModTime).strftime('%m-%d-%Y %H:%M:%S') #formats the time in an easily read format
        print("File {} : Last-Modified Time {}\n".format(abPath,formattedTime))
