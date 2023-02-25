import time
import paramiko
from jinja2 import Template

USERNAME = "admin"
PASSWORD = "cisco"

routers = [1, 2, 3]
devices_ip = "172.31.101.%s"

commands = {
    "r1": {
        "hostname": "R1",
        "interfaces": [
            {
                "int": "g0/1"
            }, {
                "int": "g0/2",
                "ip": "172.31.101.34",
                "netmask": "255.255.255.240"
            }, {
                "int": "g0/3",
                "ip": "172.31.101.34",
                "netmask": "255.255.255.240"
            }
        ],
        "routerID": "1.1.1.1",
        "routerOSPF": [
            {
                "network": "172.31.101.16",
                "wildcard": "0.0.0.15",
                "area": "0"
            }, {
                "network": "172.31.101.32",
                "wildcard": "0.0.0.15",
                "area": "0"
            }, {
                "network": "1.1.1.1",
                "wildcard": "0.0.0.0",
                "area": "0"
            }
        ]
    }, "r2": {
        "hostname": "R2",
        "interfaces": [
            {
                "int": "g0/1",
                "ip": "172.31.101.33",
                "netmask": "255.255.255.240"
            }, {
                "int": "g0/2",
                "ip": "172.31.101.50",
                "netmask": "255.255.255.240"
            }
        ],
        "routerID": "2.2.2.2",
        "routerOSPF": [
            {
                "network": "172.31.101.32",
                "wildcard": "0.0.0.15",
                "area": "0"
            }, {
                "network": "172.31.101.48",
                "wildcard": "0.0.0.15",
                "area": "0"
            }, {
                "network": "2.2.2.2",
                "wildcard": "0.0.0.0",
                "area": "0"
            }
        ]
    }, "r3": {
        "hostname": "R3",
        "interfaces": [
            {
                "int": "g0/1",
                "ip": "172.31.101.49",
                "netmask": "255.255.255.240"
            }, {
                "int": "g0/2",
                "ip": "dhcp",
                "netmask": ""
            }
        ],
        "routerID": "3.3.3.3",
        "routerOSPF": [
            {
                "network": "172.31.101.48",
                "wildcard": "0.0.0.15",
                "area": "0"
            }, {
                "network": "3.3.3.3",
                "wildcard": "0.0.0.0",
                "area": "0"
            }
        ],
        "intNATOutside": "g0/2",
        "intNATInside": "g0/1",
    }
}

for r in routers:
    ip = devices_ip %(r + 3)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=USERNAME, key_filename="/Users/kaho/Documents/KMITL/NPA/npa_rsa", look_for_keys=True)

    with open("week4/jinja2/paramikolab02.jinja2") as file_:
        template = Template(file_.read())
        command = template.render(commands["r%s" %r]).split("\n")
        with client.invoke_shell() as ssh:
            print("Connecting to {} ...".format(ip))
            for i in command:
                ssh.send(i + "\n")
                time.sleep(1)
                result = ssh.recv(1000).decode("ascii")
                print(result)
    client.close()