from netmikolab import *

devices_ip = {
    "R1": "172.31.101.4",
    "R2": "172.31.101.5",
    "R3": "172.31.101.6"
    }
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": "127.0.0.1",
    "username": username,
    "password": password
}

def test_ip_R1():
    device_params["ip"] = devices_ip["R1"]
    assert get_ip(device_params, "G0/0") == "172.31.101.4"
    assert get_ip(device_params, "G0/1") == "172.31.101.17"
    assert get_ip(device_params, "G0/2") == "172.31.101.34"
    assert get_ip(device_params, "G0/3") == "unassigned"

def test_ip_R2():
    device_params["ip"] = devices_ip["R2"]
    assert get_ip(device_params, "G0/0") == "172.31.101.5"
    assert get_ip(device_params, "G0/1") == "172.31.101.33"
    assert get_ip(device_params, "G0/2") == "172.31.101.50"
    assert get_ip(device_params, "G0/3") == "unassigned"

def test_ip_R3():
    device_params["ip"] = devices_ip["R3"]
    assert get_ip(device_params, "G0/0") == "172.31.101.6"
    assert get_ip(device_params, "G0/1") == "172.31.101.49"
    assert get_ip(device_params, "G0/3") == "unassigned"

def test_subnet_R1():
    device_params["ip"] = devices_ip["R1"]
    assert get_subnet(device_params, "G0/0") == "255.255.255.240"
    assert get_subnet(device_params, "G0/1") == "255.255.255.240"
    assert get_subnet(device_params, "G0/2") == "255.255.255.240"
    assert get_subnet(device_params, "G0/3") == "no ip address"

def test_subnet_R2():
    device_params["ip"] = devices_ip["R2"]
    assert get_subnet(device_params, "G0/0") == "255.255.255.240"
    assert get_subnet(device_params, "G0/1") == "255.255.255.240"
    assert get_subnet(device_params, "G0/2") == "255.255.255.240"
    assert get_subnet(device_params, "G0/3") == "no ip address"

def test_subnet_R3():
    device_params["ip"] = devices_ip["R3"]
    assert get_subnet(device_params, "G0/0") == "255.255.255.240"
    assert get_subnet(device_params, "G0/1") == "255.255.255.240"
    assert get_subnet(device_params, "G0/3") == "no ip address"

def test_desc_n_stat_R1():
    device_params["ip"] = devices_ip["R1"]
    assert get_desc_n_stat(device_params, "G0/0") == ("Connect to G0/2 of S0", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/1") == ("Connect to G0/2 of S1", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/2") == ("Connect to G0/1 of R2", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/3") == ("Not Use", ("admin down", "down"))

def test_desc_n_stat_R2():
    device_params["ip"] = devices_ip["R2"]
    assert get_desc_n_stat(device_params, "G0/0") == ("Connect to G0/3 of S0", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/1") == ("Connect to G0/2 of R1", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/2") == ("Connect to G0/1 of R3", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/3") == ("Not Use", ("admin down", "down"))

def test_desc_n_stat_R3():
    device_params["ip"] = devices_ip["R3"]
    assert get_desc_n_stat(device_params, "G0/0") == ("Connect to G1/0 of S0", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/1") == ("Connect to G0/2 of R2", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/2") == ("Connect to WAN", ("up", "up"))
    assert get_desc_n_stat(device_params, "G0/3") == ("Not Use", ("admin down", "down"))