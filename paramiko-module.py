import sys
import paramiko

# get arguments hostname username password
cred = [sys.argv[1],sys.argv[2],sys.argv[3]]
hostname = cred[0]
username = cred[1]
password = cred[2]

# setup ssh connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname,username=username,password=password,)
sftp_client=ssh.open_sftp()
#Download from remote server
#sftp_client.get('D:/DevOps/python/remote_file.txt','downloaded_file.txt')
sftp_client.chdir("D:\\DevOps\\python\\")
print(sftp_client.getcwd()) #Get current directory
print(sftp_client.listdir()) 

# remove a file
#sftp_client.remove('transfared_file.txt')

#Transfer to remote server
#sftp_client.put('local_file.txt','transfared_file.txt')
#print(sftp_client.listdir())

# remote commands
#stdin, stdout, stderr = ssh.exec_command("python --version")
#output = stdout.read()
#print(output)

#closing sessions
sftp_client.close()
ssh.close()
