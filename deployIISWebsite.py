import paramiko
import sys
import datetime
import time

cred = ''
hostname = ''
username = ''
password = ''
command = ''
ssh = ''


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
        global cred
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


def establish_connection(host, user, passwd):
    try:
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd, )
    except Exception as err:
        print("Unable to connect to host: {}".format(err))
        sys.exit(1)


def automateDeployment():
    global command
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # now
    #   Backup
    sftp_client = ssh.open_sftp()
    sftp_client.chdir(rootPath)
    print('Working Directory: ' + sftp_client.getcwd())
    sftp_client.put('Site.zip', 'Site.zip')
    sftp_client.close()

    # Execute command on SSH terminal  RENAME & BACKUP CURRENT SITE
    # using exec_command
    command = 'powershell.exe Compress-Archive -FORCE -Path ' + rootPath + basePath + '* -destinationPath ' + rootPath + backupDir + '/Site_Rollback_' + now_time + '.zip'
    print(command)
    execRemoteCommand(command)

    # Execute command on SSH terminal REMOVE CURRENT SITE
    # using exec_command
    command = 'rd /s/q C:\\Websites\\Site\\'
    print(command)
    execRemoteCommand(command)
    time.sleep(2)

    # Execute command on SSH terminal EXTRACT ARCHIVE NEW SITE
    # using exec_command
    command = 'powershell.exe Expand-Archive -FORCE -Path ' + rootPath + 'Site.zip -destinationPath ' + rootPath + basePath
    print(command)
    execRemoteCommand(command)


get_arguments()
establish_connection(hostname, username, password)

rootPath = 'C:/Websites/'
basePath = 'Site/'
backupDir = 'Site_Backup/'

automateDeployment()

# Clean Up
command = 'del /q C:\\Websites\\Site.zip'
print(command)
execRemoteCommand(command)
ssh.close()
