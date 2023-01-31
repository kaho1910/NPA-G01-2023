import pexpect

PROMPT = "#"
ROUTER_IP = ["172.31.101.4", "172.31.101.5", "172.31.101.6"]
USERNAME = "admin"
PASSWORD = "cisco"
LOOPBACK = ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
SUBNET_MASK = "255.255.255.255"
COMMAND = ["conf t", "int lo0", "ip add %s %s", "do wr"]
CHECK_COMMAND = "do sh ip int br"

for i in range(len(ROUTER_IP)):
    child = pexpect.spawn("telnet " + ROUTER_IP[i])
    child.expect("Username")
    child.sendline(USERNAME)
    child.expect("Password")
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    for j in range(len(COMMAND)):
        if j == 2:
            child.sendline(COMMAND[j] %(LOOPBACK[i], SUBNET_MASK))
        else:
            child.sendline(COMMAND[j])
        child.expect(PROMPT)
    child.sendline(CHECK_COMMAND)
    child.expect(PROMPT)
    result = child.before
    print("Router IP: %s" %ROUTER_IP[i])
    print(result.decode('UTF-8'), end="\n\n")
child.sendline("exit")
