import time
import paramiko

USERNAME = "admin"
PASSWORD = "cisco"

devices_ip = ["172.31.101.4", "172.31.101.5", "172.31.101.6"]

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, pkey="/Users/kaho/.ssh/id_rsa", look_for_keys=True)

    commands = ["sh ip int br"]
    for command in commands:
        print("Executing {}".format(command))
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print("Errors")
        print(stderr.read().decode())
        time.sleep(1)
    client.close()