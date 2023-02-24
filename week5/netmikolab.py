import re
from netmiko import ConnectHandler
# from pprint import pprint
import struct
import socket
from jinja2 import Template

def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_command(command, use_textfsm=True)
        return result

def get_ip(device_params, intf):
    data = get_data_from_device(device_params, "sh ip int br")
    for i in data:
        result = re.search(r"(\w)\w+(\d+/\d+)", i["intf"])
        if result is not None:
            intf_type, intf_num = result.groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return i["ipaddr"]

def get_subnet(device_params, intf):
    data = get_data_from_device(device_params, "sh ip int {}".format(intf))
    if data[0]["ipaddr"] == []:
        return "no ip address"
    ans = cidr_to_netmask(data[0]["mask"][0])
    return ans

def get_desc_n_stat(device_params, intf):
    '''
        return description and status in tuple
        ex. ("This is Desc", ("Status1", "Status2"))
    '''
    data = get_data_from_device(device_params, "sh int des")
    for i in data:
        result = re.search(r"(\w)\w+(\d+/\d+)", i["port"])
        if result is not None:
            intf_type, intf_num = result.groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return (i["descrip"], (i["status"], i["protocol"]))

def cidr_to_netmask(net_bits):
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask

if __name__ == "__main__":
    devices_ip = {
        "R1": "172.31.101.4",
        "R2": "172.31.101.5",
        "R3": "172.31.101.6",
    }
    username = "admin"
    password = "cisco"

    device_params = {
        "device_type": "cisco_ios",
        "ip": "127.0.0.1",
        "username": username,
        "password": password
    }

    commands = {
        "R1": {
            "int_desc":[
                {
                    "interface": "g0/0",
                    "desc": "Connect to G0/2 of S0"
                }, {
                    "interface": "g0/1",
                    "desc": "Connect to G0/2 of S1"
                }, {
                    "interface": "g0/2",
                    "desc": "Connect to G0/1 of R2"
                }, {
                    "interface": "g0/3",
                    "desc": "Not Use"
                }
            ]
        }, "R2": {
            "int_desc":[
                {
                    "interface": "g0/0",
                    "desc": "Connect to G0/3 of S0"
                }, {
                    "interface": "g0/1",
                    "desc": "Connect to G0/2 of R1"
                }, {
                    "interface": "g0/2",
                    "desc": "Connect to G0/1 of R3"
                }, {
                    "interface": "g0/3",
                    "desc": "Not Use"
                }
            ]
        }, "R3": {
            "int_desc":[
                {
                    "interface": "g0/0",
                    "desc": "Connect to G1/0 of S0"
                }, {
                    "interface": "g0/1",
                    "desc": "Connect to G0/2 of R2"
                }, {
                    "interface": "g0/2",
                    "desc": "Connect to WAN"
                }, {
                    "interface": "g0/3",
                    "desc": "Not Use"
                }
            ]
        }
    }

    for device in ["R1", "R2", "R3"]:
        device_params["ip"] = devices_ip[device]
        with ConnectHandler(**device_params) as ssh:
            with open("week5/jinja2/int_desc.jinja2") as file_:
                template = Template(file_.read())
                command = template.render(commands[device]).split("\n")
                result = ssh.send_config_set(command)
                print(result)
        # pprint(get_data_from_device(device_params, "sh ip int br"))

        # for i in range(4):
            # print(get_ip(device_params, "G0/%d" %i))
            # print(get_subnet(device_params, "G0/%d" %i))
            # print(get_desc_n_stat(device_params, "G0/%d" %i))