import time
import paramiko

USERNAME = "admin"
PASSWORD = "cisco"

devices_ip = ["172.31.101.4", "172.31.101.5", "172.31.101.6"]

commands = ["terminal length 0", "sh ip int br"]

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, key_filename="/Users/kaho/Documents/KMITL/NPA/npa_rsa", look_for_keys=True)

    print("Connecting to {} ...".format(ip))
    with client.invoke_shell() as ssh:
        print("Connecting to {} ...".format(ip))

        for j in commands:
            ssh.send(j + "\n")
            time.sleep(1)
            result = ssh.recv(1000).decode("ascii")
            print(result)
    client.close()