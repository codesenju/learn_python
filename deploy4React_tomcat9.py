from re import I
from tokenize import String
import paramiko
import sys
import datetime
import time

def execRemoteCommand(command):   
    stdin, stdout, stderr = ssh.exec_command(command)  
    output = stdout.readlines() 
    for index, item in enumerate(output):
        print(item)
    output = stdout.readlines() 
    for index, item in enumerate(output):
        print(item)
def get_arguments():
    try: 
        # get arguments hostname username password
        global cred
        cred = [sys.argv[1],sys.argv[2],sys.argv[3]]
        global hostname
        global username
        global password 
        hostname = cred[0]
        username = cred[1]
        password = cred[2]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)
def establich_connection(host,user,passwd):
    try:
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,username=user,password=passwd,)
    except Exception as err:
        print("Unable to connect to host: {}".format(err))
        sys.exit(1)
def automateDeployment():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') #  now
        #   Backup
        sftp_client=ssh.open_sftp()
        sftp_client.chdir(rootPath + basePath)
        print('Working Directory: ' + sftp_client.getcwd())
        sftp_client.put('ROOT.zip','ROOT.zip')
        sftp_client.close()

        # Execute command on SSH terminal STOP & START SERVICE
        # using exec_command
        command = 'powershell.exe Get-Service SERVICE_NAME'
        print(command)
        execRemoteCommand(command)
        command = 'powershell.exe Stop-Service SERVICE_NAME'
        print('STOP SERVICE: '+command)
        execRemoteCommand(command)
        command = 'powershell.exe Get-Service SERVICE_NAME'
        print(command)
        execRemoteCommand(command)

        #Service is stopped
        time.sleep(4)
        # Execute command on SSH terminal  RENAME & BACKUP
        # using exec_command
        
        command = 'powershell.exe Compress-Archive -FORCE -Path ' +  rootPath + basePath + 'apache-tomcat-9.0.59/webapps/ROOT/* -destinationPath ' +  rootPath + backupDir + '/ROOT_ROLLBACK_' + nowTime + '.zip'
        print(command)
        execRemoteCommand(command)
        

        # Execute command on SSH terminal EXTRACT ARCHIVE
        # using exec_command
        command = 'powershell.exe Expand-Archive -FORCE -Path ' +  rootPath + basePath + 'ROOT.zip -destinationPath ' +  rootPath + basePath + 'apache-tomcat-9.0.59/webapps/ROOT'
        print(command)
        execRemoteCommand(command)
        

        command = 'powershell.exe Start-Service SERVICE_NAME'
        print('START SERVICE: ' + command)
        execRemoteCommand(command)
        

        command = 'powershell.exe Get-Service SERVICE_NAME'
        print(command)
        execRemoteCommand(command)
        
get_arguments()
establich_connection(hostname,username,password)

rootPath='D:/DevOps/Deployments/'
basePath='react_project/'
backupDir='react_project_BACKUPS/'

automateDeployment()

#Clean Up
ssh.close()