from netmiko import ConnectHandler

def get_data_from_device(device_params):
    with ConnectHandler(**device_params) as ssh:
        result_shipintbr = ssh.send_command("sh ip int br")
        return result_shipintbr

def get_ip(device_params, intf):
    data = get_data_from_device(device_params)
    result = data.strip().split("\n")
    for line in result[1:]:
        words = line.split()
        if words[0][0] == intf[0] and words[0][-3:] == intf[1:]:
            return words[1]

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
            "description Connect to WAN2",
            "int G0/3",
            "description Not Use"
        ]}

    for device in ["R1", "R2", "R3"]:
        device_params["ip"] = devices_ip[device]
        with ConnectHandler(**device_params) as ssh:
            command = commands[device]
            for i in command:
                result = ssh.send_config_set(i)
                print(result)

        print(get_ip(device_params, "G0/0"))