import os
import paramiko
import sys
import json
import datetime
import time
ssh_client = paramiko.SSHClient()
hostname = ''
username = 'SVC_KafkaIGX_poc_dev'
password = ''
dev_hosts = ['fas-rbglidv01', 'fas-rbglidv02', 'fas-rbglidv03', 'fas-rbglidv04', 'fas-rbglidv05']
int_hosts = ['fas-rbglint01', 'fas-rbglint02', 'fas-rbglint03', 'fas-rbglint04', 'fas-rbglint05']
# int_hosts = ['fas-rbglint02']
hosts = list("")
myDict = {}


def execRemoteDockerCommand(cmd, client, n):
    containers = list("")
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stderr.readlines()
    for index, item in enumerate(output):
        print(item)
    output = stdout.readlines()
    for index, item in enumerate(output):
        # print(item)
        # containers.append(item.split(" ")[0])
        # print(item.split(" ")[0])
        containers.append(item.split(" ")[0])
    del containers[0]
    # print(containers)
    myDict.update({n: containers})
    del containers


def execRemoteCommand(cmd, ssh):
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
        # cred = [sys.argv[1], sys.argv[2], sys.argv[3]]
        # global hostname
        # global username
        global password
        # hostname = cred[0]
        # username = cred[1]
        password = sys.argv[1]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)


get_arguments()
docker_ps = 'docker ps --no-trunc --format "table {{.Names}}\\t{{.Status}}"'


def dockerGod(docker_ps_):
    for h in int_hosts:
        try:
            global ssh_client
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=h, username=username, password=password)
            # sftp_client = ssh_client.open_sftp()
            # print("####################" + x + "####################")
            execRemoteDockerCommand(docker_ps_, ssh_client, h)
            # myDict.update({x: containers})
        finally:
            # sftp_client.close()
            ssh_client.close()

print("####-CONTAINERS-####")

# print(containers)
# print(myDict)

dockerGod(docker_ps)

# start containers
for x, y in myDict.items():
    # x = host
    # y = list of containers in x
    # c = container
    print(x)
    try:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=x, username=username, password=password)
        for c in y:
            cmd_ = 'docker restart ' + c
            print(cmd_)
            execRemoteCommand(cmd_, ssh_client)
        print("\n")
    finally:
        # sftp_client.close()
        ssh_client.close()

