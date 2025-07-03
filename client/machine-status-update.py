#!/usr/bin/env python3

# machine-status updater

#import subprocess
import socket
from time import localtime, strftime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import json
import os
import sys
import toml
from datetime import datetime
# import hashlib
# import netifaces as ni
# from PIL import Image, ImageFont, ImageDraw

load_flag = False      # True if load averages are too high
diskfree_flag = False  # True if disk free space is too low

# base_address = "http://localhost:4010"
hostname = socket.gethostname() # This machine's hostname

CONFIG_FILENAME = "config.toml"

# Read config file
def read_config():
    try:
        CONFIG = toml.load(CONFIG_FILENAME, _dict=dict)
        base_address = "http://" + CONFIG["machine_status_ip"] + ":" + CONFIG["machine_status_port"] + "/machine-status"
        # print(f"base_address is {base_address}")
        mountpoint = CONFIG["mountpoint"]
        min_free_space = CONFIG["min_free_space"]
        max_load_avg = CONFIG["max_load_avg"]
    except Exception as e:
        output_error = f"Config can't be parsed! Please check config file. Error: {str(e)}"
        sys.exit(output_error)

    return base_address, mountpoint, min_free_space, max_load_avg

# Get load averages
def get_load_avgs():
    try:
        loads = os.getloadavg()
        load_one = loads[0]
        load_five = loads[1]
        load_fifteen = loads[2]
        loads = f"Load average: {load_one:.2f}, {load_five:.2f}, {load_fifteen:.2f}"

        if load_one > max_load_avg or load_five > max_load_avg or load_fifteen > max_load_avg:
            load_flag = True
        else:
            load_flag = False

    except Exception as e:
        output_error = f"Load averages went wrong: {str(e)}"
        sys.exit(output_error)

    return load_one, load_five, load_fifteen, load_flag

# Get disk free space
def get_disk_used():
    try:
        disk_used = int(os.popen(diskfree_cmd).read().strip().strip("%"))

        if (100 - disk_used) < min_free_space:
            diskfree_flag = True
        else:
            diskfree_flag = False

    except Exception as e:
        output_error = f"Disk free command went wrong: {str(e)}"
        sys.exit(output_error)

    return disk_used, diskfree_flag

# Make the JSON payload
def make_payload():
    status_update = {
        "name": hostname,
        "machineStatus": {
            "loadAverages": {
                "load-1": round(load_one, 2),
                "load-5": round(load_five, 2),
                "load-15": round(load_fifteen, 2),
                "problemFlag": load_flag
            },
            "diskFree": {
                "mountPoint": mountpoint,
                "freeSpace": {
                    "freeSpacePercentage": 100 - disk_used,
                    "problemFlag": diskfree_flag
                },
            }
        }
    }

    # Make the JSON payload
    try:
        status_update_json = json.dumps(status_update)
        # print(f"{status_update_json}")
    except Exception as e:
        output_error = f"Error creating status update JSON: {str(e)}"
        sys.exit(output_error)

    return status_update_json

# Let's connect to a server!
def make_request():

    # Set up the request, and add the content-type header
    req = Request(url = one_machine_address, data = bytes(payload.encode("utf-8")), method = "PUT")

    req.add_header("Content-type", "application/json; charset=UTF-8")

    # Send the update to the server

    try:
        with urlopen(req) as resp:
            #response_data = json.loads(resp.read().decode("utf-8"))
            if resp.status == 201:
                logtime = datetime.now().strftime("%Y-%m-%d %X")
                print( f"{logtime} Update successful")
    except HTTPError as error:
        print( f"Server error: {error.status} {error.reason}" )
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")
    except Exception as e:
        output_error = f"Error in PUT attempt: {str(e)}"
        sys.exit(output_error)

base_address, mountpoint, min_free_space, max_load_avg = read_config()

status_address = base_address + "/"
vibe_address = base_address + "/vibe"
all_machines_address = base_address + "/machines"
one_machine_address = base_address + "/machines/" + hostname

load_one, load_five, load_fifteen, load_flag = get_load_avgs()

diskfree_cmd = f"df -h {mountpoint} | awk 'NR==2 {{print $5}}'"

disk_used, diskfree_flag = get_disk_used()

payload = make_payload()

make_request()
