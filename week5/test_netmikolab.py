from netmikolab import *
from multiprocessing import Process

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

r1_params = device_params.copy()
r1_params.update({"ip": devices_ip["R1"]})

r2_params = device_params.copy()
r2_params.update({"ip": devices_ip["R2"]})

r3_params = device_params.copy()
r3_params.update({"ip": devices_ip["R3"]})

def check_ip_R1():
    assert get_ip(r1_params, "G0/0") == "172.31.101.4"
    assert get_ip(r1_params, "G0/1") == "172.31.101.17"
    assert get_ip(r1_params, "G0/2") == "172.31.101.34"
    assert get_ip(r1_params, "G0/3") == "unassigned"

def check_ip_R2():
    assert get_ip(r2_params, "G0/0") == "172.31.101.5"
    assert get_ip(r2_params, "G0/1") == "172.31.101.33"
    assert get_ip(r2_params, "G0/2") == "172.31.101.50"
    assert get_ip(r2_params, "G0/3") == "unassigned"

def check_ip_R3():
    assert get_ip(r3_params, "G0/0") == "172.31.101.6"
    assert get_ip(r3_params, "G0/1") == "172.31.101.49"
    assert get_ip(r3_params, "G0/3") == "unassigned"

def check_subnet_R1():
    assert get_subnet(r1_params, "G0/0") == "255.255.255.240"
    assert get_subnet(r1_params, "G0/1") == "255.255.255.240"
    assert get_subnet(r1_params, "G0/2") == "255.255.255.240"
    assert get_subnet(r1_params, "G0/3") == "no ip address"

def check_subnet_R2():
    assert get_subnet(r2_params, "G0/0") == "255.255.255.240"
    assert get_subnet(r2_params, "G0/1") == "255.255.255.240"
    assert get_subnet(r2_params, "G0/2") == "255.255.255.240"
    assert get_subnet(r2_params, "G0/3") == "no ip address"

def check_subnet_R3():
    assert get_subnet(r3_params, "G0/0") == "255.255.255.240"
    assert get_subnet(r3_params, "G0/1") == "255.255.255.240"
    assert get_subnet(r3_params, "G0/3") == "no ip address"

def check_desc_n_stat_R1():
    assert get_desc_n_stat(r1_params, "G0/0") == ("Connect to G0/2 of S0", ("up", "up"))
    assert get_desc_n_stat(r1_params, "G0/1") == ("Connect to G0/2 of S1", ("up", "up"))
    assert get_desc_n_stat(r1_params, "G0/2") == ("Connect to G0/1 of R2", ("up", "up"))
    assert get_desc_n_stat(r1_params, "G0/3") == ("Not Use", ("admin down", "down"))

def check_desc_n_stat_R2():
    assert get_desc_n_stat(r2_params, "G0/0") == ("Connect to G0/3 of S0", ("up", "up"))
    assert get_desc_n_stat(r2_params, "G0/1") == ("Connect to G0/2 of R1", ("up", "up"))
    assert get_desc_n_stat(r2_params, "G0/2") == ("Connect to G0/1 of R3", ("up", "up"))
    assert get_desc_n_stat(r2_params, "G0/3") == ("Not Use", ("admin down", "down"))

def check_desc_n_stat_R3():
    assert get_desc_n_stat(r3_params, "G0/0") == ("Connect to G1/0 of S0", ("up", "up"))
    assert get_desc_n_stat(r3_params, "G0/1") == ("Connect to G0/2 of R2", ("up", "up"))
    assert get_desc_n_stat(r3_params, "G0/2") == ("Connect to WAN", ("up", "up"))
    assert get_desc_n_stat(r3_params, "G0/3") == ("Not Use", ("admin down", "down"))

def test_r1():
    p1 = Process(target=check_ip_R1)
    p1.start()
    p2 = Process(target=check_subnet_R1)
    p2.start()
    p3 = Process(target=check_desc_n_stat_R1)
    p3.start()
    p1.join()
    p2.join()
    p3.join()

def test_r2():
    p1 = Process(target=check_ip_R2)
    p1.start()
    p2 = Process(target=check_subnet_R2)
    p2.start()
    p3 = Process(target=check_desc_n_stat_R2)
    p3.start()
    p1.join()
    p2.join()
    p3.join()

def test_r3():
    p1 = Process(target=check_ip_R3)
    p1.start()
    p2 = Process(target=check_subnet_R3)
    p2.start()
    p3 = Process(target=check_desc_n_stat_R3)
    p3.start()
    p1.join()
    p2.join()
    p3.join()

