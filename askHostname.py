#!/usr/bin/env python3

from tkinter import simpledialog
from tkinter import messagebox
import tkinter as tk
import socket
import pickle
import os
import re
import time

######################################
############ config ##################
######################################

## only debian and derivates

TITLE = "Hostname prompt"
ENTRY = "enter new hostname [current: {}]"
HOST_CHANGE_COMMAND_SESSION = "hostname -b "
HOST_CHANGE_COMMAND_PERMANENT = "echo "
HOST_CHANGE_COMMAND_PERMANENT_END = " > /etc/hostname"
REPEAT_ON_ERROR = True
RESET_NETWORK = "service networking restart"
NET_IFACES_DIRECTORY = "/sys/class/net/"
NET_RESET_LAYOUT_IN_SECONDS = 4.5

# this folder SHOULD exist...
DATA_FILE = '/home/pi/RadioniceConfig/delete_this_to_change_hostname_at_startup'

######################################
#### DO NOT EDIT BELOW THIS LINE #####
######################################


prompt = True

try:
    with open(DATA_FILE, 'rb') as f:
        prompt = pickle.load(f)
except:
    pass

def get_all_interfaces(path):
    return os.listdir(path)

def bring_ifaces_down(iface_list):
    for ifc in iface_list:
        os.system("ifconfig " + ifc + " down")

def bring_ifaces_up(iface_list):
    for ifc in iface_list:
        os.system("ifconfig " + ifc + " up")

def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

if prompt:

    CURR_HOSTNAME = socket.gethostname()

    app = tk.Tk()
    app.withdraw()
    result = simpledialog.askstring(TITLE, ENTRY.format(CURR_HOSTNAME), parent=app)

    if result != None:

        if not is_valid_hostname(result):
            messagebox.showerror("Error", "Invalid hostname")

            if REPEAT_ON_ERROR:
               exit(-1)

            with open(DATA_FILE, 'wb') as f:
               prompt = pickle.dump(False, f)
            exit(0)

        ret_val1 = os.system(HOST_CHANGE_COMMAND_SESSION + " " + result) # change the current session hostname
        ret_val2 = os.system(HOST_CHANGE_COMMAND_PERMANENT + " " + result + " " + HOST_CHANGE_COMMAND_PERMANENT_END)
        ret_val3 = os.system(RESET_NETWORK)

        if_list = get_all_interfaces(path = NET_IFACES_DIRECTORY)
        bring_ifaces_down(iface_list)
        time.sleep(NET_RESET_LAYOUT_IN_SECONDS)
        bring_ifaces_up(iface_list)

        ret_val4 = os.system(RESET_NETWORK)

        if ret_val1 != 0 or ret_val2 != 0 or ret_val3 != 0 or ret_val4 != 0:
            messagebox.showerror("Error", "Unable to change hostname (do you have sufficient privilegies?!)")
            if REPEAT_ON_ERROR:
                exit(-1)

    with open(DATA_FILE, 'wb') as f:
        prompt = pickle.dump(False, f)


