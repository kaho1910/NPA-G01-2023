import time
import paramiko

USERNAME = "admin"
PASSWORD = "cisco"

routers = [1, 2, 3]
devices_ip = "172.31.101.%s"

command = {
    "r1": ["conf t", "int g0/2", "ip add 172.31.101.34 255.255.255.240", "no shut", "ex", "router ospf 1 vrf Control-DataVRF", "router-id 1.1.1.1", "network 172.31.101.16 0.0.0.15 area 0", "network 172.31.101.32 0.0.0.15 area 0", "network 1.1.1.1 0.0.0.0 area 0", "do wr"],
    "r2": ["conf t", "int g0/1", "ip add 172.31.101.33 255.255.255.240", "no shut", "int g0/2", "ip add 172.31.101.50 255.255.255.240", "no shut", "ex", "router ospf 1 vrf Control-DataVRF", "router-id 2.2.2.2", "network 172.31.101.32 0.0.0.15 area 0", "network 172.31.101.48 0.0.0.15 area 0", "network 2.2.2.2 0.0.0.0 area 0", "ex", "do wr"],
    "r3": ["conf t", "ip access-list extended Block-telnet/SSH", "deny tcp any any eq 22", "deny tcp any any eq 23", "permit ip any any", "int g0/1", "ip add 172.31.101.49 255.255.255.240", "no shut", "int g0/2", "ip add dhcp", "ip access-group Block-telnet/SSH in", "ip route vrf Control-DataVRF 0.0.0.0 0.0.0.0 192.168.122.1", "no shut", "ex", "router ospf 1 vrf Control-DataVRF", "router-id 3.3.3.3", "default-information originate", "network 172.31.101.48 0.0.0.15 area 0", "network 3.3.3.3 0.0.0.0 area 0", "ex", "access-list 1 permit any", "ip nat inside source list 1 int g0/2 vrf Control-DataVRF overload", "int g0/2", "ip nat outside", "int g0/1", "ip nat inside", "do wr"]
}

for r in routers:
    ip = devices_ip %(r + 3)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, key_filename="/Users/kaho/Documents/KMITL/NPA/npa_rsa", look_for_keys=True)

    with client.invoke_shell() as ssh:
        print("Connecting to {} ...".format(ip))
        for i in command["r%s" %r]:
            ssh.send(i+ "\n")
            time.sleep(1)
            result = ssh.recv(1000).decode("ascii")
            print(result)
    client.close()