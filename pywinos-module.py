from pywinos import WinOSClient
import sys

# get arguments hostname username password
cred = [sys.argv[1],sys.argv[2],sys.argv[3]]
hostname = cred[0]
username = cred[1]
password = cred[2]
print(cred)
tool = WinOSClient(host=hostname, username=username, password=password, logger_enabled=True)
response = tool.run_ps(command='whoami')

#print(response)  
# ResponseParser(response=(0, 'Major  Minor  Build  Revision\r\n-----  -----  -----  --------\r\n5      1      17763  592', None, '$PSVersionTable.PSVersion'))
#print(response.exited)  # 0
print(response.stdout)
# Major  Minor  Build  Revision
# -----  -----  -----  --------
# 5      1      17763  592

# stderr in PowerShell contains some text by default    
print('errors: ', response.stderr)  # <Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04"><Ob...
#print(response.ok)  # True