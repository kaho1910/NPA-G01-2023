from netmiko import ConnectHandler

def get_data_from_device(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command(command)
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params, "sh ip int br")
    result = data.strip().split("\n")
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[1:]:
            return words[1]

def get_subnet(device_params, intf):
    data = get_data_from_device(device_params, "sh run int {}".format(intf))
    result = data.strip().split("\n")
    for line in result[5:]:
        line = line.strip()
        if "ip address" in line:
            ans = line.split()[-1]
            if ans == "dhcp":
                return "dhcp"
            if line == "no ip address":
                return "no ip address"
            return line.split()[-1]

def get_desc_n_stat(device_params, intf):
    '''
        return description and status in tuple
        ex. ("This is Desc", ("Status1", "Status2"))
    '''
    data = get_data_from_device(device_params, "sh int des")
    result = data.strip().split("\n")
    for line in result[1:]:
        words = [i.strip() for i in line.split()]
        if words[0][0] == intf[0] and words[0][-len(intf) + 1:] == intf[1:]:
            if words[2] == "down":
                ans1 = " ".join(words[4:])
                ans2 = " ".join(words[1:3]), words[3]
            else:
                ans1 = " ".join(words[3:])
                ans2 = words[1], words[2]
            return ans1, ans2

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
            "description Not Use"
        ],
        "R2":[
            "int G0/0",
            "description Connect to G0/3 of S0",
            "int G0/1",
            "description Connect to G0/2 of R1",
            "int G0/2",
            "description Connect to G0/1 of R3",
            "int G0/3",
            "description Not Use"
        ],
        "R3":[
            "int G0/0",
            "description Connect to G1/0 of S0",
            "int G0/1",
            "description Connect to G0/2 of R2",
            "int G0/2",
            "description Connect to WAN",
            "int G0/3",
            "description Not Use"
        ]}

    for device in ["R1", "R2", "R3"]:
        device_params["ip"] = devices_ip[device]
        with ConnectHandler(**device_params) as ssh:
            result = ssh.send_config_set(commands[device])
            print(result)


        # for i in range(4):
        #     print(get_subnet(device_params, "G0/%d" %i))
        #     print(get_ip(device_params, "G0/%d" %i))
        #     print(get_desc_n_stat(device_params, "G0/%d" %i))