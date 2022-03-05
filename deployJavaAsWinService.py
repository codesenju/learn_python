import paramiko
import sys
import time

hostname = ''
username = ''
password = ''
service_name = 'app'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def execRemoteCommand(command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stderr.readlines()
    for index, item in enumerate(output):
        print(item)
    output = stdout.readlines()
    for index, item in enumerate(output):
        print(item)


def get_arguments():
    global hostname
    global username
    global password
    try:
        # get arguments hostname username password
        cred = [sys.argv[1], sys.argv[2], sys.argv[3]]
        hostname = cred[0]
        username = cred[1]
        password = cred[2]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)


def establish_connection(host, user, passwd):
    try:
        ssh.connect(hostname=host, username=user, password=passwd)
    except Exception as err:
        print("Unable to connect to host: {}".format(err))
        sys.exit(1)


def automateDeployment():
    # Execute command on SSH terminal STOP & START SERVICE
    # using exec_command
    command = 'powershell.exe Get-Service ' + service_name
    print(command)
    execRemoteCommand(command)
    command = 'powershell.exe Stop-Service ' + service_name
    print('STOP SERVICE: ' + command)
    execRemoteCommand(command)
    command = 'powershell.exe Get-Service ' + service_name
    print(command)
    execRemoteCommand(command)

    # Service is stopped
    time.sleep(2)
    # Execute command on SSH terminal  RENAME & BACKUP
    # using exec_command
    command = "powershell.exe Move-Item -Force -Path '" + appPath + service_name + ".jar' -Destination '" + appPath + service_name + ".jar.rollback'"
    print(command)
    execRemoteCommand(command)

    # Execute command on SSH terminal COPY NEW JAR FILE
    sftp_client = ssh.open_sftp()
    sftp_client.chdir(appPath)
    print('Working Directory: ' + sftp_client.getcwd())
    sftp_client.put(service_name + '.jar', service_name + '.jar')
    sftp_client.close()

    command = 'powershell.exe Start-Service ' + service_name
    print('START SERVICE: ' + command)
    execRemoteCommand(command)

    command = 'powershell.exe Get-Service ' + service_name
    print(command)
    execRemoteCommand(command)


get_arguments()
establish_connection(hostname, username, password)

appPath = 'D:/Deployments/' + service_name

automateDeployment()

# Clean Up
ssh.close()
