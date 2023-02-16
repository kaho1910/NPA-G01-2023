import time
import paramiko

USERNAME = "admin"
PASSWORD = "cisco"

routers = [1, 2, 3]
devices_ip = "172.31.101.%s"

command = {
    "r1": "conf t\nint g0/2\nip add 172.31.101.34 255.255.255.240\nno shut\nex\nrouter ospf 1\nrouter-id 1.1.1.1\nnetwork 172.31.101.0 0.0.0.31 area 0\nnetwork 1.1.1.1 0.0.0.0 area 0\ndo wr",
    "r2": "conf t\nint g0/1\nip add 172.31.101.33 255.255.255.240\nint g0/2\nip add 172.31.101.50 255.255.255.240\nno shut\nex\nrouter ospf 1\nrouter-id 2.2.2.2\nnetwork 172.31.101.32 0.0.0.15 area 0\nnetwork 172.31.101.48 0.0.0.15 area 0\nnetwork 2.2.2.2 0.0.0.0 area 0\nex\ndo wr",
    "r3": "conf t\nint g0/1\nip add 172.31.101.49 255.255.255.240\nno shut\nint g0/2\nip add dchp\nno shut\nex\nrouter ospf 1\nrouter-id 3.3.3.3\nnetwork 172.31.101.48 0.0.0.15 area 0\nnetwork 3.3.3.3 0.0.0.0 area 0\nex\ndo wr"
}

for r in routers:
    ip = devices_ip %(r + 3)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, key_filename="/Users/kaho/Documents/KMITL/NPA/npa_rsa", look_for_keys=True)

    with client.invoke_shell() as ssh:
        print("Connecting to {} ...".format(ip))
        
        ssh.send(command["r%s" %r] + "\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)
    client.close()