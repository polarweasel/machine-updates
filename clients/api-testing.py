#!/usr/bin/env python3

# machine-status testing

#import subprocess
import socket
from time import localtime, strftime
import urllib.request
import json
import os
import sys
import toml
# import hashlib
# import netifaces as ni
# from PIL import Image, ImageFont, ImageDraw

load_flag = False      # True if load averages are too high
diskfree_flag = False  # True if disk free space is too low

# Get the machine's DNS hostname
hostname = socket.gethostname()

CONFIG_FILENAME = "config.toml"

# Read config file
try:
    CONFIG = toml.load(CONFIG_FILENAME, _dict=dict)
    MOUNTPOINT = CONFIG["mountpoint"]
    MIN_FREE_SPACE = CONFIG["min_free_space"]
    MAX_LOAD_AVG = CONFIG["max_load_avg"]
except Exception as e:
    output_error = f"Config can't be parsed! Please check config file. Error: {str(e)}"
    sys.exit(output_error)

# Get load averages
try:
    loads = os.getloadavg()
    load_one = loads[0]
    load_five = loads[1]
    load_fifteen = loads[2]
    loads = f"Load average: {load_one:.2f}, {load_five:.2f}, {load_fifteen:.2f}"

    if load_one > MAX_LOAD_AVG or load_five > MAX_LOAD_AVG or load_fifteen > MAX_LOAD_AVG:
        load_flag = True

except Exception as e:
    output_error = f"Load averages went wrong: {str(e)}"
    sys.exit(output_error)


diskfree_cmd = f"df -h {MOUNTPOINT} | awk 'NR==2 {{print $5}}'"

try:
    disk_used = int(os.popen(diskfree_cmd).read().strip().strip("%"))

    if (100 - disk_used) < MIN_FREE_SPACE:
        diskfree_flag = True

except Exception as e:
    output_error = f"Disk free command went wrong: {str(e)}"
    sys.exit(output_error)

# Make the data structure that we'll turn into the JSON payload
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
            "mountPoint": MOUNTPOINT,
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
    print(f"{status_update_json}")
except Exception as e:
    output_error = f"Error creating status update JSON: {str(e)}"
    sys.exit(output_error)
