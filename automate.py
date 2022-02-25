import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='<server>',username='<user>',password='<passwd',)
sftp_client=ssh.open_sftp()
#Download from remote server
#sftp_client.get('D:/DevOps/python/remote_file.txt','downloaded_file.txt')
sftp_client.chdir("D:\\DevOps\\python\\")
print(sftp_client.getcwd()) #Get current directory
print(sftp_client.listdir()) 

#Transfer to remote server
#sftp_client.put('local_file.txt','transfared_file.txt')
print(sftp_client.listdir())
sftp_client.close()
ssh.close()