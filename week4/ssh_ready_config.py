import getpass
import telnetlib
import time

def main():
    '''function to put PUB_KEY in R0-3'''
    host = "172.31.101.%d"
    user = input("Enter username: ")
    password = getpass.getpass()

    for i in range(1, 7):
        tn = telnetlib.Telnet(host %i, 23, 5)

        tn.read_until(b"Username:")
        tn.write(user.encode("ascii") + b"\n")
        time.sleep(1)

        tn.read_until(b"Password:")
        tn.write(password.encode("ascii") + b"\n")
        time.sleep(1)

        tn.write(b"conf t\nip ssh pubkey-chain\nusername admin\nkey-string\nAAAAB3NzaC1yc2EAAAADAQABAAABAQDQybBesoEEHrkVqjJn1m134hE6I7Scj25S\nukxhbZkARBQe/bqwYtspGpcFavu3+TVTUSYifpU0V7Pmu/ZNImMfb7MpKExbjTfGVQyr7YMk\nWwFeYv/Lw+ybk3zYIlDlWNHqCXlk+4IUePzKXD5r6DBXgNIFgFXSp9sGR2VNAbZTEustcp7R\nOSV+FBUDoDlCOByHCKIdrzdNH8dTA9SFeJmCJ1s0PDJnYgos9GisUTdsO+hkjbpPhGjEtYAa\nQnU5HwA7aNy31dRB6gbu2mRBn4fyUGtapSb7kP+HYqKB1zTT1MC7IvmbBa/MOkvcmhLWHvDt\nb+dP4tybocuMsbJviuV3\nexit\nexit\nexit\nno ip ssh server authenticate user password\nno ip ssh server authenticate user keyboard\ndo wr\n")
        time.sleep(1)
        tn.write(b"do sh ip int br\n")
        time.sleep(2)
        tn.write(b"do wr\nend\n")
        time.sleep(1)

        tn.close()
main()
