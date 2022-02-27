import sys
import paramiko
# Funcions:
def run_remote_commad(cmd):
# Execute commands remotely
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stderr.readlines())
        return stdout.readlines()
    except Exception as err:
        print("Error happened: {}".format(err))

dest_path=""
source_path=""

# get arguments hostname username password
cred = [sys.argv[1],sys.argv[2],sys.argv[3]]
hostname = cred[0]
username = cred[1]
password = cred[2]

# setup ssh connection
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname,username=username,password=password,)
except Exception as err:
    print("Unable to connect to host: {}".format(err))

sftp_client=ssh.open_sftp()
#Download from remote server
#sftp_client.get('D:/DevOps/python/remote_file.txt','downloaded_file.txt')
sftp_client.chdir("D:/DevOps/Deployments/tests") # Change directory
#print(sftp_client.getcwd()) # Get current directory
#print(sftp_client.listdir()) 

# remove a file
#sftp_client.remove('transfared_file.txt')

#Transfer to remote server
#sftp_client.put('./local_file.txt','transfared_file.txt')
#print(sftp_client.listdir())
#stdin, stdout, stderr = ssh.exec_command("C:\Python310\python.exe --version")
#print(stdout.readlines())
#print(stderr.readlines())

try:
    cmd = sys.argv[4] # get command from 4th args
#    cmd = "powershell.exe ls D:/DevOps/Deployments"
except Exception as err:
    print("Unable to assign arguments to cmd: {}".format(err))


try:
    print('\n'.join(run_remote_commad(cmd)))
except Exception as err:
    print("Unable to run remote command: {}".format(err))
 
# Rename folder
#sftp_client.rename('build','new-build')

#print(sftp_client.listdir())

#closing sessions
sftp_client.close()
ssh.close()
