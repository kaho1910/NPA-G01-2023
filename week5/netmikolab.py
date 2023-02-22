import re
from netmiko import ConnectHandler
# from pprint import pprint
import struct
import socket

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
    data = get_data_from_device(device_params, "sh run int {}".format(intf))
    result = data.strip().split("\n")
    for line in result[5:]:
        intf_subnet = re.search(r"(no ip address|\d+\.\d+\.\d+\.\d+$|dhcp)", line)
        if intf_subnet is not None:
            intf_subnet = intf_subnet.group(0)
            return intf_subnet

def get_desc_n_stat(device_params, intf):
    '''
        return description and status in tuple
        ex. ("This is Desc", ("Status1", "Status2"))
    '''
    data = get_data_from_device(device_params, "sh int des")
    result = data.strip().split("\n")
    for line in result[1:]:
        intf_data = re.search(r"(\w)\w+(\d/\d)\s+(up|admin down)\s+(up|down)\s+(.+)", line)
        if intf_data is not None:
            intf_type, intf_num, intf_stat, intf_prot, intf_desc = intf_data.groups()
            if intf_type == intf[0] and intf_num == intf[1:]:
                return (intf_desc, (intf_stat, intf_prot))

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
        "R1": [
            "int G0/0",
            "description Connect to G0/2 of S0",
            "int G0/1",
            "description Connect to G0/2 of S1",
            "int G0/2",
            "description Connect to G0/1 of R2",
            "int G0/3",
            "description Not Use",
            "do wr"
        ],
        "R2":[
            "int G0/0",
            "description Connect to G0/3 of S0",
            "int G0/1",
            "description Connect to G0/2 of R1",
            "int G0/2",
            "description Connect to G0/1 of R3",
            "int G0/3",
            "description Not Use",
            "do wr"
        ],
        "R3":[
            "int G0/0",
            "description Connect to G1/0 of S0",
            "int G0/1",
            "description Connect to G0/2 of R2",
            "int G0/2",
            "description Connect to WAN",
            "int G0/3",
            "description Not Use",
            "do wr"
        ]}

    for device in ["R1", "R2", "R3"]:
        device_params["ip"] = devices_ip[device]
        with ConnectHandler(**device_params) as ssh:
            result = ssh.send_config_set(commands[device])
            print(result)
        # pprint(get_data_from_device(device_params, "sh ip int br"))

        # for i in range(4):
            # print(get_ip(device_params, "G0/%d" %i))
            # print(get_subnet(device_params, "G0/%d" %i))
            # print(get_desc_n_stat(device_params, "G0/%d" %i))