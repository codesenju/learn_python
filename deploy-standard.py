import os
import paramiko
import sys
import datetime
import time

hostname = ''
username = ''
password = ''
ssh = paramiko.SSHClient()


def run_local_cmd(your_command):
    print(your_command)
    try:
        os.system(your_command)
    except Exception as err:
        print("Unable to execute local cmd: " + your_command  + " {} " + format(err))
        sys.exit(1)


def execRemoteCommand(cmd, client):
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stderr.readlines()
    for index, item in enumerate(output):
        print(item)
    output = stdout.readlines()
    for index, item in enumerate(output):
        print(item)


def get_arguments():
    try:
        # get arguments hostname username password
        cred = [sys.argv[1], sys.argv[2], sys.argv[3]]
        global hostname
        global username
        global password
        hostname = cred[0]
        username = cred[1]
        password = cred[2]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)


def automateDeployment(changes, sftp, client):
    for index, item in enumerate(changes):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # now
        print(item)
        #   Backup
        print('\n###############-BACKUP-###############')
        cmd = "/" + backupDir
        sftp.chdir(cmd)
        print('Working Directory: ' + sftp.getcwd())
        print('Local Working Dir: ' + os.getcwd())
        print(' Original File: ' + basePath + item.strip(
            '\n') + '\n Backup File: ' + backupDir + item.strip('\n') + '.rollback_' + now_time)
        # print(basePath + item.strip('\n'), ' \n' + backupDir + item.strip('\n') + '.rollback')
        try:
            sftp.stat("/" + basePath + item.strip('\n'))
        except Exception as err:
            print(basePath + item.strip('\n') + " Not Found! \n{}".format(err))
        finally:
            try:
                cmd = 'C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe Move-Item -Force -Path ' + basePath + item.strip(
                    '\n') + ' -Destination ' + backupDir + item.strip('\n') + '.rollback_' + now_time
                execRemoteCommand(cmd, client)
            except Exception as err:
                print("Unable to backup " + basePath + item.strip('\n') + ": {}".format(err))
                sys.exit(1)
        print('###############-END-###############\n')

        # Copy new file
        print('\n###############-COPY FILE-###############')
        sftp.chdir("/" + basePath)
        print('Working Directory: ' + sftp_client.getcwd())
        print('Copying file: ' + item.strip('\n') + '\n HOST: ' + hostname + '\n PATH: ' + basePath + item.strip('\n'))
        sftp.put(item.strip('\n'), "/" + basePath + item.strip('\n'))
        print('###############-END-###############\n')


get_arguments()

os.system('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe Expand-Archive -Path changes.zip -DestinationPath ./changes')
command = 'md changes'
print(command)
os.system(command)
command = 'C:\\7z2107\\x64\\7za.exe x changes.zip -o.\changes -aoa'
print(command)
os.system(command)

time.sleep(2)
os.chdir('changes')
print('Local Working directory: ' + os.getcwd())

print('reading file...')
with open("output.txt") as f:
    lines_ = f.readlines()
    print(type(lines_))
    print(lines_)

basePath = "D:/Destination/"
backupDir = "D:/Backup/"

print('Local Working Dir: ' + os.getcwd())
os.system('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe pwd')
os.system('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe ls')
print("Files to be copied: ")
os.system('C:\Windows\System32\WindowsPowerShell\\v1.0\powershell.exe cat output.txt')
print(lines_)

try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)
    sftp_client = ssh_client.open_sftp()
    automateDeployment(lines_, sftp_client, ssh_client)
finally:
    sftp_client.close()
    ssh_client.close()

# Clean Up
os.chdir('../')
os.system("rd /s/q changes")
# os.system("del /q changes.zip")