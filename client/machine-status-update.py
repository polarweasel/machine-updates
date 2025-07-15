#!/usr/bin/env python3

# machine-status updater
#
# When this is deployed, it should be named /usr/local/bin/machine-status-update.py
# (Remember to make it executable!)

import socket
from time import localtime, strftime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import json
import os
import sys
import toml
from datetime import datetime

load_flag = False      # True if load averages are too high
diskfree_flag = False  # True if disk free space is too low

hostname = socket.gethostname() # This machine's hostname

CONFIG_FILENAME = "/etc/machine-status-update/config.toml"

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
    # Get system load averages. If any are higher than the warning threshold, raise the flag.
    # (load_flag corresponds to machineStatus.loadAverages.problemFlag in the JSON payload)
    try:
        loads = os.getloadavg()
        load_one = round(loads[0], 2)
        load_five = round(loads[1], 2)
        load_fifteen = round(loads[2], 2)
        # loads = f"Load average: {load_one:.2f}, {load_five:.2f}, {load_fifteen:.2f}"

        if load_one > max_load_avg or load_five > max_load_avg or load_fifteen > max_load_avg:
            load_flag = True
        elif load_one < 0 or load_five < 0 or load_fifteen < 0:
            load_flag = True
        else:
            load_flag = False

    except Exception as e:
        output_error = f"Load averages went wrong: {str(e)}"
        sys.exit(output_error)

    return load_one, load_five, load_fifteen, load_flag

# Get disk usage
def get_disk_used():
    # Get disk usage for the mount we care about. If free space is lower than the
    # warning threshold, raise the flag.
    # (diskfree_flag corresponds to machineStatus.diskFree.freeSpace in the JSON payload)

    diskfree_cmd = f"df -h {mountpoint} | awk 'NR==2 {{print $5}}'"

    try:
        disk_used = int(os.popen(diskfree_cmd).read().strip().strip("%"))

        if (100 - disk_used) < min_free_space or (100 - disk_used) < 0:
            diskfree_flag = True
        else:
            diskfree_flag = False

    except Exception as e:
        output_error = f"Disk free command went wrong: {str(e)}"
        sys.exit(output_error)

    return disk_used, diskfree_flag

# Make the JSON payload
def make_payload():
    # Get all the data
    load_one, load_five, load_fifteen, load_flag = get_load_avgs()
    disk_used, diskfree_flag = get_disk_used()

    # Make the data structure
    status_update = {
        "name": hostname,
        "machineStatus": {
            "loadAverages": {
                "load-1": load_one,
                "load-5": load_five,
                "load-15": load_fifteen,
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
    except Exception as e:
        output_error = f"Error creating status update JSON: {str(e)}"
        sys.exit(output_error)

    # Uncomment this print statement to send the JSON object to stdout
    # print(f"{status_update_json}")
    return status_update_json

# Send the update to the server
def make_request():
    # Set up the request, and add the content-type header
    this_machine_address = base_address + "/machines/" + hostname
    req = Request(url = this_machine_address, data = bytes(payload.encode("utf-8")), method = "PUT")
    req.add_header("Content-type", "application/json; charset=UTF-8")

    # Send the update to the server
    try:
        with urlopen(req) as resp:
            #response_data = json.loads(resp.read().decode("utf-8"))
            if resp.status == 201:
                logtime = datetime.now().strftime("%Y-%m-%d %X")
                print( f"{logtime} Update successful")
    except HTTPError as error:
        output_error = f"Server error: {error.status} {error.reason}"
        sys.exit(output_error)
    except URLError as error:
        output_error = f"URL error: {error.reason}"
        sys.exit(output_error)
    except TimeoutError:
        output_error = "Request timed out"
        sys.exit(output_error)
    except Exception as e:
        output_error = f"Uncaught error: {str(e)}"
        sys.exit(output_error)

base_address, mountpoint, min_free_space, max_load_avg = read_config()

# Useful for API testing. Not used in production.
# status_address = base_address + "/"
# vibe_address = base_address + "/vibe"
# all_machines_address = base_address + "/machines"

payload = make_payload()

make_request()
