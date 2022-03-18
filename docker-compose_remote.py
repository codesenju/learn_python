import paramiko
import sys

command = ""
ssh_client = paramiko.SSHClient()
hostname = ''
username = ''
password = ''
env = ''


def execRemoteCommand(cmd, ssh):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stderr.readlines()
    for index, item in enumerate(output):
        print(item)
    output = stdout.readlines()
    for index, item in enumerate(output):
        print(item)


def get_env_username_password():
    try:
        global env
        global username
        global password
        env = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        sys.exit(1)
    finally:
        if env == "dv":
            print("env: " + env)
        elif env == "nt":
            print("env: " + env)
        elif env == "nt":
            print("env: " + env)
        else:
            print("Env has to be set to dv|nt|qa|pr")
            sys.exit(1)


def get_compose_cmd():
    global command
    try:
        command = sys.argv[4]
    except Exception as err:
        print("Unable to get arguments: {}".format(err))
        print("Will use 'ps' as dedault")
        command = "ps"


get_env_username_password()

applications = {}

get_compose_cmd()

docker_ps = 'docker ps --no-trunc --format "table {{.Names}}\\t{{.Status}}"'


def docker_compose(list_, docker_compose_cmd):
    # start containers
    for x, y in list_.items():
        # x = Key | host
        # y = list | directories
        # c = item in list
        print(x)
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=x, username=username, password=password)
            for c in y:
                cmd_ = "cd /tmp/docker_run/" + c + "/ && docker-compose " + docker_compose_cmd
                print(cmd_)
                execRemoteCommand(cmd_, ssh_client)
                sftp_client = ssh_client.open_sftp()
                # dir_ = "/tmp/docker_run/" + c + "/"
                # print(dir_)
                # sftp_client.chdir(dir_)
                # print(sftp_client.listdir())
                # print(sftp_client.getcwd())

            print("\n")
        finally:
            sftp_client.close()
            ssh_client.close()


docker_compose(applications, command)
