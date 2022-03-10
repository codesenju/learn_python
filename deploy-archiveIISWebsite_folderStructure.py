import os
import sys
import subprocess
import time

ssh = ''
build = ''


def get_arguments():
    try:
        # get arguments hostname username password
        global build
        build = sys.argv[1]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))


def deploy_archive(changes):
    # Create Folder Structure
    for index, folder in enumerate(changes):
        dir = folder.split('/')
        del dir[-1]  # remove last index
        folderStructure = '/'.join(dir)
        # print(folderStructure)
        command = "powershell.exe New-Item -Force -Path ./changes/" + folderStructure + " -ItemType dir"
        print(command)
        os.system(command)
    # Copy Files
    for index, change in enumerate(changes):
        command = "powershell.exe Copy-Item -Path '" + change.strip('\n') + "' -Destination './changes/" + change.strip(
            '\n') + "'"
        print(command)
        os.system(command)
        time.sleep(2)
    # prepare build.zip
    command = "powershell.exe echo " + build + " > ./changes/build.txt"
    print(command)
    os.system(command)
    time.sleep(2)
    command = "powershell.exe Copy-item -Force -Path output.txt ./changes/output.txt"
    print(command)
    os.system(command)
    time.sleep(2)
    command = "powershell.exe Compress-Archive -Force -Path ./changes/* -destinationPath changes.zip"
    print(command)
    os.system(command)
    time.sleep(2)


get_arguments()
# Prep
try:
    os.system("del /q changes.zip")
except Exception as err:
    print("{}".format(err))

file_ = open("output.txt", "w")
subprocess.Popen("C:/PortableGit/mingw64/bin/git.exe diff --name-only HEAD^", stdout=file_)
file_.close()
time.sleep(2)

print('reading file...')
with open("output.txt") as f:
    lines_ = f.readlines()
    print(type(lines_))
    print(lines_)

deploy_archive(lines_)

time.sleep(4)
# Clean Up
os.system("powershell.exe Remove-Item output.txt")
os.system("rd /s/q changes")
