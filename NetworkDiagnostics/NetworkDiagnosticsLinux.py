# Author: Jordan Kasoff
# Version 2.0


# Requirements:
# Linux/Unix OS (commands listed require unix/linux commands to operate properly, will not operate correctly on windows)

import os  # used to run commands on Linux system
import sys

FileOutput = False


def printer(message):
    if FileOutput:
        file1 = open('report.txt', 'a')
        file1.write(message)
    else:
        print(message)


# prepares for the network connectivity tests
def init():
    os.system('clear')  # clears terminal for a clean view of the test
    try:
        if sys.argv[1] == "-o":
            global FileOutput
            FileOutput = True
            if os.path.exists("report.txt"):
                os.remove("report.txt")
            else:
                os.popen("touch report.txt")
            UserName = os.popen("whoami").read().rstrip()
            printer("===========================================\n")
            printer("          NetworkDiagnostics  Script V1.2\n")
            printer("          Created By Jordan Kasoff\n")
            printer("===========================================\n")
            printer("Welcome: " + UserName)
    except IndexError:
        UserName = os.popen("whoami").read().rstrip()
        printer("===========================================\n")
        printer("          NetworkDiagnostics  Script V1.2\n")
        printer("          Created By Jordan Kasoff\n")
        printer("===========================================\n")
        printer("Welcome: " + UserName)


# gets gateway ip address for the system
# returns gateway if properly configures
# ends test if interface is not properly configured
def get_gateway():
    try:
        # displays routes (ip route) that start with keyword "default" (grep default)
        tempGateway = os.popen("ip route|grep default").read().rstrip()
        # turns command printout into readable python data types
        tempGateway = tempGateway.split(' ')
        gateway = tempGateway[2]  # if correctly configured, gateway address is the 3rd "word" in the printout
        printer("\n\n" + tempGateway[4] + " Default Gateway: " + gateway)
        return gateway

    # IF Configuration file is not proper structured, will return an index error,
    # this result requires looking at connection and configuration to DF Gateway
    except IndexError:
        print(" ")
        print("Interface Configuration Error")
        print("Gateway cannot be detected")


def get_dns():
    try:
        command = "resolvectl status |grep \"Current DNS Server\""
        tempDNS = os.popen(command).read().rstrip()
        # turns command printout into readable python data types
        tempDNS = tempDNS.split(' ')
        DNS = tempDNS[3]  # if correctly configured, gateway address is the 3rd "word" in the printout
        printer("\n\nCurrent DNS Server: " + DNS)
        return DNS

    # IF Configuration file is not proper structured, will return an index error,
    # this result requires looking at connection and configuration to DF Gateway
    except IndexError:
        print(" ")
        print("DNS Configuration Error")
        print("DNS cannot be detected")


# Tests ping to the remote device, reports if ping was successful or not
def ping_device(deviceAddress):
    result = os.popen("ping " + deviceAddress + " -c4").read().rstrip()  # pings gateway 4 times
    # turns command printout into readable python data types
    # sees if there is a 0% error rate in the ping result
    if "0% packet loss" in result:
        printer("\nPing to " + deviceAddress + " : Successful\n")
        return 1
    # if not, there is an error, and the test has failed
    elif "100% packet loss" in result:
        printer("\nPing to " + deviceAddress + " : Unsuccessful\n")
        return 0
    else:
        printer("\nPing to " + deviceAddress + " : Indeterminate \n")
        return 0.5


def main():
    init()
    printer("\n\nGateway Test")
    gateway = get_gateway()
    gateway_test = ping_device(gateway)
    if gateway_test < 1:
        printer("Warning: Possible Gateway Connectivity Issues")
        exit()
    printer("\n\nLocal DNS Test")
    Default_DNS = get_dns()
    dns_test = ping_device(Default_DNS)
    if dns_test < 1:
        printer("Warning: Possible DNS Connectivity Issues")
        exit()
    printer("\n\nRemote Connectivity Test")
    Remote_Device = ping_device("8.8.8.8")
    if Remote_Device < 1:
        printer("Warning: Possible Remote Device Connectivity Issues")
    Remote_DNS = ping_device("google.com")

    exit()


main()
