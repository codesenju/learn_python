import sys
import os

env = "default"


def get_arguments():
    global env
    try:
        # get arguments hostname username password
        env = sys.argv[1]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))


get_arguments()

os.chdir('./app')
print('Working Directory: ' + os.getcwd())
os.system("npm install")
os.system("npm run build:" + env)
os.system("powershell.exe Compress-Archive -Path build/* -destinationPath ROOT.zip")
os.system("powershell.exe ls")
