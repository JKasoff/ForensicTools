# Author: Jordan Kasoff
# Version 2.0


# Requirements:
# Windows

# To Do: Multi Interfaced Boxes

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
    os.system('cls')  # clears terminal for a clean view of the test
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
        tempGateway = os.popen("ipconfig /all | find \"Default Gateway\"").read().rstrip()
        # turns command printout into readable python data types
        tempGateway = tempGateway.split('Default Gateway . . . . . . . . . :')
        #tempGateway = tempGateway.split('  b\n')
        gateway = []
        for i in tempGateway:
            #expand to usage with multiple gateways
            if len(i) > 7:
                gateway.append(i)
        gateway = gateway[0].rstrip()

        printer(" Default Gateway: " + gateway)
        return gateway

    # IF Configuration file is not proper structured, will return an index error,
    # this result requires looking at connection and configuration to DF Gateway
    except IndexError:
        print(" ")
        print("Interface Configuration Error")
        print("Gateway cannot be detected")


def get_dns():
    try:
        command = "ipconfig /all | find \"DNS Server\""
        tempDNS = os.popen(command).read().rstrip()
        # turns command printout into readable python data types
        tempDNS = tempDNS.split('DNS Servers . . . . . . . . . . . :')
        # tempGateway = tempGateway.split('  b\n')
        DNS = []
        for i in tempDNS:
            # expand to usage with multiple gateways
            if len(i) > 7:
                DNS.append(i)
        DNS = DNS[0].rstrip()
        return DNS

    # IF Configuration file is not proper structured, will return an index error,
    # this result requires looking at connection and configuration to DF Gateway
    except IndexError:
        print(" ")
        print("DNS Configuration Error")
        print("DNS cannot be detected")


# Tests ping to the remote device, reports if ping was successful or not
def ping_device(deviceAddress):
    command = "ping " + deviceAddress + " -n 3"
    result = os.popen(command).read().rstrip()  # pings gateway 4 times
    # turns command printout into readable python data types
    # sees if there is a 0% error rate in the ping result
    if "0% loss" in result:
        printer("\nPing to " + deviceAddress + " : Successful\n")
        return 1
    # if not, there is an error, and the test has failed
    elif "100% loss" in result:
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
