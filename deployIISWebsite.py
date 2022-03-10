import paramiko
import sys
import datetime
import time
import os

ssh = ''
hostname = ''
username = ''
password = ''
command = ''
env = 'dev'
site = 'WEB01'


def applyWebConfig(env_):
    global command
    if env_ == 'qa':
        print('Apply qa web config')
        command = 'powershell.exe Copy-Item ' + basePath + 'web_qa.config -Destination ' + basePath + 'web.config'
        print(command)
        execRemoteCommand(command)

    elif env_ == 'prod':
        print('Apply prod web config')
        command = 'powershell.exe Copy-Item ' + basePath + 'web_prod.config -Destination ' + basePath + 'web.config'
        print(command)
        execRemoteCommand(command)
    elif env_ == 'dev':
        print('Apply dev web config')
        command = 'powershell.exe Copy-Item ' + basePath + 'web_dev.config -Destination ' + basePath + 'web.config'
        print(command)
        execRemoteCommand(command)
    else:
        print('Unable to apply Web config ' + env)


def execRemoteCommand(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
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
        global env
        hostname = cred[0]
        username = cred[1]
        password = cred[2]
        env = sys.argv[4]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)
        if env == 'dev':
            print("script will apply dev web config {}".format(err))
        elif env == 'qa':
            print("script will apply qa web config {}".format(err))
        elif env == 'prod':
            print("script will apply prod web config {}".format(err))
        else:
            print("Unable to read Web config " + env + " {}".format(err))


def establish_connection(host, user, passwd):
    try:
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd)
    except Exception as err:
        print("Unable to connect to host: {}".format(err))
        sys.exit(1)


def automateDeployment(lines_):
    global command
    for index, item in enumerate(lines_):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # now
        print(item)
        #   Backup
        sftp_client = ssh.open_sftp()
        print('\n###############-BACKUP-###############')
        sftp_client.chdir(backupDir)
        print('Working Directory: ' + sftp_client.getcwd())
        print('Local Working Dir: ' + os.getcwd())
        print(' Original File: ' + basePath + item.strip(
            '\n') + '\n Backup File: ' + backupDir + item.strip('\n') + '.rollback_' + now_time)
        # print(basePath + item.strip('\n'), ' \n' + backupDir + item.strip('\n') + '.rollback')

        try:
            sftp_client.stat("/" + basePath + item.strip('\n'))
        except Exception as err:
            print(basePath + item.strip('\n') + " Not Found! \n{}".format(err))
        finally:
            try:
                command = "powershell.exe Move-Item -Force -Path '" + basePath + item.strip(
                    '\n') + "' -Destination '" + backupDir + item.strip('\n') + ".rollback_" + now_time + "'"
                execRemoteCommand(command)
            except Exception as err:
                print("Unable to backup " + basePath + item.strip('\n') + ": {}".format(err))
                sys.exit(1)
        print('###############-END-###############\n')
        sftp_client.close()

        # Copy new file
        sftp_client = ssh.open_sftp()
        print('\n###############-COPY FILE-###############')
        sftp_client.chdir(basePath)
        print('Working Directory: ' + sftp_client.getcwd())
        print('Copying file: ' + item.strip('\n') + '\n HOST: ' + hostname + '\n PATH: ' + basePath + item.strip('\n'))
        sftp_client.put(item.strip('\n'), "/" + basePath + item.strip('\n'))

        print('###############-END-###############\n')
        sftp_client.close()


get_arguments()
establish_connection(hostname, username, password)

basePath = 'D:/Websites/' + site + '/'
backupDir = 'D:/Websites/Backup/' + site + '/'

os.system('powershell.exe Expand-Archive -Force -Path changes.zip -DestinationPath ./changes')
time.sleep(2)
os.chdir('changes')
print('Local Working directory: ' + os.getcwd())

print('reading file...')
with open("output.txt") as f:
    lines = f.readlines()
    print(type(lines))
    print(lines)

automateDeployment(lines)
applyWebConfig(env)
ssh.close()
