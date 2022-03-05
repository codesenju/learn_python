import sys
import time
import os
env = ''


def get_arguments():
    try:
        # get arguments environment name
        global env
        env = sys.argv[1]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))


# os.chdir('.')  # change to directory locally
print('Working Directory: ' + os.getcwd())
os.system('powershell.exe Compress-Archive -Path ./* -destinationPath Access.zip')
time.sleep(2)
