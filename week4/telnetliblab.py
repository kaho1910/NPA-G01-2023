import getpass
import telnetlib
import time

host = "172.31.101.4"
user = input("Enter username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host, 23, 5)

tn.read_until(b"Username:")
tn.write(user.encode("ascii") + b"\n")
time.sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode("ascii") + b"\n")
time.sleep(1)

tn.write(b"conf t\nint g0/1\n ip add 172.31.101.17 255.255.255.240\nno shut\n")
time.sleep(1)
tn.write(b"do sh ip int br\n")
time.sleep(2)
tn.write(b"do wr\nend\n")
time.sleep(1)

output = tn.read_very_eager()
print(output.decode("ascii"))

tn.close()