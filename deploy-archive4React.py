from re import I
import sys
import time
import os
def get_arguments():
    try: 
        # get arguments environment name
        global env 
        env =sys.argv[1]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
get_arguments()
#os.chdir('.') # change to directory locally of React Project ROOT
print('Working Directory: ' + os.getcwd())
os.system('powershell.exe npm install ')
os.system('powershell.exe npm run build:' + env)
os.system('powershell.exe Compress-Archive -Path build/* -destinationPath ROOT.zip')
time.sleep(2)