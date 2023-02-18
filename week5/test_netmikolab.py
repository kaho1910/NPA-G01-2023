from netmikolab import *

device_ip = "172.31.101.4"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password
}

def test_ip():
    assert get_ip(device_params, "G0/0") == "172.31.101.4"