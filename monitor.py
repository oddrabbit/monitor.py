#!/usr/bin/env python3

'''

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import subprocess
import os
import time
import sys
import time
import argparse
import icmplib

parser = argparse.ArgumentParser(prog = sys.argv[0], usage = sys.argv[0] + " --configuration-file <Configuration file> --log-file <Log file> --ip-address <IP address>\n       " + sys.argv[0] + " -c <Configuration file> -l <Log file> -i <IP address>")

parser.add_argument("-c", help = "Configuration file -> This will be the file that contains all of the hosts to scan seperated by a newline")
parser.add_argument("-l", help = "Log file -> This will be the file where hosts that are down will be logged")
parser.add_argument("-i", help = "IP address -> This will be the usual IP address of the network")
parser.add_argument("--configuration-file", help = "Configuration file -> Same as -c")
parser.add_argument("--log-file", help = "Log file -> Same as -l")
parser.add_argument("--ip-address", help = "IP address -> same as -i")

args = parser.parse_args()

if args.c:
    configuration_file = args.c
elif args.configuration_file:
    configuration_file = args.configuration_file
else:
    parser.print_help(sys.stderr)
    quit()

if args.l:
    log_file = args.l
elif args.log_file:
    log_file = args.log_file
else:
    parser.print_help(sys.stderr)
    quit()

if args.i:
    usual_ip_address = args.i
elif args.ip_address:
    usual_ip_address = args.ip_address
else:
    parser.print_help(sys.stderr)
    quit()
     

null_file_handler = open(os.devnull, "w")
no_pingback_count = {}
hosts_to_scan = []

try:
    file_handler = open(configuration_file, "r")
except NameError:
    parser.print_help(sys.stderr)
    exit()

contents = file_handler.readlines()

for i in contents:
    hosts_to_scan.append(i.strip())

for i in hosts_to_scan:
    no_pingback_count[i] = 0

def scan_hosts():
    current_time = time.asctime(time.localtime(time.time())).split()

    print("Scan started: " + current_time[4] + "-", end = "")
    if current_time[1] == "Jan":
        print("01", end = "")
    elif current_time[1] == "Feb":
        print("02", end = "")
    elif current_time[1] == "Mar":
        print("03", end = "")
    elif current_time[1] == "Apr":
        print("04", end = "")
    elif current_time[1] == "May":
        print("05", end = "")
    elif current_time[1] == "Jun":
        print("06", end = "")
    elif current_time[1] == "Jul":
        print("07", end = "")
    elif current_time[1] == "Aug":
        print("08", end = "")
    elif current_time[1] == "Sep":
        print("09", end = "")
    elif current_time[1] == "Oct":
        print("10", end = "")
    elif current_time[1] == "Nov":
        print("11", end = "")
    elif current_time[1] == "Dec":
        print("12", end = "")

    print("-" + current_time[2] + ", " + current_time[3])

    for i in hosts_to_scan:
        if i == "":
            break
        try:
            host_pinged = icmplib.ping(i, count = 1, interval = 1, timeout = 2)
        except icmplib.exceptions.NameLookupError:
            no_pingback_count[i] += 1
            if no_pingback_count[i] == 3:
                no_pingback_count[i] = 1
            print("\t[-] " + i.upper() + " IS DOWN")
            with open(log_file, "a") as file_handler:
                file_handler.write("[-] " + i.upper() + " IS DOWN (" + time.asctime(time.localtime(time.time())) + ")\n")
                no_pingback_count[i] = 0
                continue
        if host_pinged.is_alive:
            print("\t[+] " + i + " is up")
            no_pingback_count[i] = 0
        else:
            no_pingback_count[i] += 1
            if no_pingback_count[i] == 3:
                no_pingback_count[i] = 1
                print("\t[-] " + i.upper() + " IS DOWN")
                with open(log_file, "a") as file_handler:
                    file_handler.write("[-] " + i.upper() + " IS DOWN (" + time.asctime(time.localtime(time.time())) + ")\n")
                    no_pingback_count[i] = 0

def scan_ip():
       
    actual_ip_address = subprocess.check_output(["curl -s https://get-site-ip.com | grep 'Your ip is' | cut -d ' ' -f 22 | tail -n 1"], shell = True).decode("utf-8")[:-1]
    if actual_ip_address == usual_ip_address:
        print("IP address: " + actual_ip_address)
    else:
        print("CHANGED IP ADDRESS: " + actual_ip_address)

def main():
    while True:
        subprocess.run(["reset"])
        scan_ip()
        scan_hosts()
        time.sleep(5)

if __name__ == "__main__":
    main()
