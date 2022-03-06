import paramiko
import sys
import datetime
import time
cred = ''
hostname = ''
username = ''
password = ''
liquibaseCommand = ''
ssh = ''
command = ''


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
        global liquibaseCommand
        cred = [sys.argv[1], sys.argv[2], sys.argv[3]]
        global hostname
        global username
        global password
        hostname = cred[0]
        username = cred[1]
        password = cred[2]
        liquibaseCommand = sys.argv[4]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)


def establish_connection(host, user, passwd):
    try:
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=passwd)
    except Exception as err:
        print("Unable to connect to host: {}".format(err))
        sys.exit(1)


def automateDeployment():
    global command
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # now
    command = 'md ' + removeDir
    print(command)
    execRemoteCommand(command)

    # COPY SQL SCRIPTS
    sftp_client = ssh.open_sftp()
    sftp_client.chdir(rootPath + basePath)
    print('Working Directory: ' + sftp_client.getcwd())
    sftp_client.put('sql.zip', 'sql.zip')
    # COPY PROPERTIES FILE
    sftp_client.put('liquibase.properties', 'liquibase.properties')
    # COPY ROOT CHANGELOG
    sftp_client.put('db.changelog-root.xml', 'db.changelog-root.xml')
    sftp_client.close()

    # Extract Archive
    command = 'powershell.exe Expand-Archive -Force -LiteralPath ' + rootPath + basePath + '/sql.zip -DestinationPath ' + rootPath + basePath
    print(command)
    execRemoteCommand(command)
    time.sleep(4)
    # Liquibase Status
    command = 'powershell.exe C:/liquibase-4.7.1/liquibase.bat --defaultsFile=' + rootPath + basePath + 'liquibase.properties status'
    print(command)
    execRemoteCommand(command)

    # Liquibase Command
    command = 'powershell.exe C:/liquibase-4.7.1/liquibase.bat --defaultsFile=' + rootPath + basePath + 'liquibase.properties ' + liquibaseCommand
    print(command)
    execRemoteCommand(command)


get_arguments()
establish_connection(hostname, username, password)

rootPath = 'C:/DevOps/Deployments/mssql_version_ctrl/'
basePath = 'dev/'
removeDir = 'C:\\DevOps\\Deployments\\mssql_version_ctrl\\dev'
# backupDir='react_project_BACKUPS/'

automateDeployment()

# Clean Up
command = 'rd /s/q ' + removeDir
print(command)
execRemoteCommand(command)

ssh.close()
