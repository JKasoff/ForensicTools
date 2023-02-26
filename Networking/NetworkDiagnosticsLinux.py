# Author: Jordan Kasoff
# Version 2.0


# Requirements:
# Linux/Unix OS (commands listed require unix/linux commands to operate properly, will not operate correctly on windows)

import os  # used to run commands on Linux system
import sys

FileOutput = False


# prepares for the network connectivity tests
def init():
    if sys.argv[1] == "-o":
        global FileOutput
        FileOutput = True
    os.system('clear')  # clears terminal for a clean view of the test
    UserName = os.popen("whoami").read().rstrip()
    print("===========================================")
    print("          Networking  Script V1.2")
    print("          Created By Jordan Kasoff")
    print("===========================================\n")
    print("Welcome: " + UserName)
    print("Output Mode: ")
    exit()


# gets gateway ip address for the system
# returns gateway if properly configures
# ends test if interface is not properly configured
def get_gateway():
    try:
        temp = os.popen(
            "ip route|grep default")  # displays routes (ip route) that start with keyword "default" (grep default)
        # turns command printout into readable python data types
        str_tmp = temp.read()
        temp = str_tmp.rstrip()
        arr1 = temp.split(' ')
        gateway = arr1[2]  # if correctly configured, gateway address is the 3rd "word" in the printout
        for i in range(0, 5):  # more spacing
            print(" ")
        print("Your Default Gateway is " + gateway)
        return gateway

    # IF Configuration file is not proper structured, will return an index error,
    # this result requires looking at connection and configuration to DF Gateway
    except IndexError:
        print(" ")
        print("Interface Configuration Error")
        print("Gateway cannot be detected")
        print("Script Completed")
        exit()


# method variable (gateway): determined ip address of the computer's gateway from get_gateway, used for pinging
# Tests ping to the gateway, reports if ping was successful or not
def ping_gateway(gateway):
    temp = os.popen("ping " + gateway + " -c4")  # pings gateway 4 times
    # turns command printout into readable python data types
    str_tmp = temp.read()
    temp = str_tmp.rstrip()
    arr1 = temp.split(' ')
    # sees if there is a 0% error rate in the ping result
    if "0%" in arr1:
        print("Ping to Gateway: Successful")
        return 1
    # if not, there is an error, and the test has failed
    else:
        print("Ping to Gateway: Unsuccessful")
        return 0


# Tests ping to a remote computer, reports if ping was successful or not
def ping_remote():
    temp = os.popen("ping 50.116.1.225 -c4")  # pings remote computer IP's address (netcat) 4 times
    # turns command printout into readable python data types
    str_tmp = temp.read()
    temp = str_tmp.rstrip()
    arr1 = temp.split(' ')
    # sees if there is a 0% error rate in the ping result
    if "0%" in arr1:
        print("Ping to Remote: Successful")
        return 1
    # if not, there is an error, and the test has failed
    else:
        print("Ping to Remote: Unsuccessful")
        return 0


# Tests ping to a remote gateway using a host name to test dns revolution , reports if ping was successful or not
def ping_remoteDNS():
    temp = os.popen("ping google.com -c4")  # pings remote computer IP's address (google.com) 4 times using a host name
    # turns command printout into readable python data types

    str_tmp = temp.read()
    temp = str_tmp.rstrip()
    arr1 = temp.split(' ')
    # sees if there is a 0% error rate in the ping result
    if "0%" in arr1:
        print("DNS Resolution: Successful")
        return 1
    # if not, there is an error, and the test has failed
    else:
        print("DNS Resolution: Unsuccessful")
        return 0


def main():
    score = 0  # counter for succulence connectivity tests
    init()
    gateway = get_gateway()
    score += ping_gateway(gateway)
    score += ping_remote()
    score += ping_remoteDNS()
    final = int(float(score) / float(3) * 100)  # calculates successful networking percentage
    print("Your Network Connectivity is at %" + str(final))
    print("Script Completed")


main()
