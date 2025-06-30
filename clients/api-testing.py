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

#if os.geteuid() != 0:
#    sys.exit("You need root permissions to access E-Ink display, try running with sudo!")

INTERFACE = "wlan0"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 80
# IS_ROTATED = 0
# SCREEN_TYPE = "215g"

OUTPUT_STRING = ""
DISPHASH_FILENAME = "/tmp/api-testing-output"
CONFIG_FILENAME = "config.toml"
SESSION_CACHE_FILE = "/tmp/api-testing-session"

# Read config file
try:
    CONFIG = toml.load(CONFIG_FILENAME, _dict=dict)
    INTERFACE = CONFIG["interface"]
    SERVER_IP = CONFIG["machine_status_ip"]
    SERVER_PORT = CONFIG["machine_status_port"]
    # IS_ROTATED = CONFIG["is_rotated"]
    # SCREEN_TYPE = CONFIG["screen_type"]
except Exception as e:
    output_error = f"Config can't be parsed! Please check config file. Error: {str(e)}"
    sys.exit(output_error)

hostname = socket.gethostname()
font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
font_name = os.path.join(font_dir, "font.ttf")
font16 = ImageFont.truetype(font_name, 16)
font12 = ImageFont.truetype(font_name, 12)

# Global variable to store CSRF token if needed
csrf_token = None

def save_session(sid, csrf):
    """Save session ID and CSRF token to cache file for reuse"""
    try:
        with open(SESSION_CACHE_FILE, 'w') as f:
            cache_data = {
                'sid': sid,
                'csrf': csrf,
                'timestamp': strftime("%Y-%m-%d %H:%M:%S", localtime())
            }
            f.write(json.dumps(cache_data))
    except Exception:
        # If we can't save the session, just continue without caching
        pass

def load_session():
    """Load session ID and CSRF token from cache file if available"""
    try:
        if os.path.exists(SESSION_CACHE_FILE):
            with open(SESSION_CACHE_FILE, 'r') as f:
                cache_data = json.loads(f.read())

                # Set csrf_token global
                global csrf_token
                csrf_token = cache_data.get('csrf')

                return cache_data.get('sid')
    except Exception:
        # If we can't load the session, return None to request a new one
        pass
    return None

def validate_session(sid):
    """Test if the cached session is still valid"""
    if not sid:
        return False

    headers = {
        'sid': sid,
        'Cookie': f'sid={sid}'
    }

    # Add CSRF token if available
    if csrf_token:
        headers['X-CSRF-Token'] = csrf_token

    # Try to access the summary API as a test
    try:
        test_url = f"http://{PIHOLE_IP}:{PIHOLE_PORT}/api/stats/summary"
        request = urllib.request.Request(test_url, headers=headers)
        response = urllib.request.urlopen(request)
        # If we get here, the session is valid
        return True
    except Exception:
        # Session invalid, we'll need a new one
        return False

def get_session_id():
    """Get a session ID from the V6 API by authenticating, with caching"""
    # First try to load and validate a cached session
    cached_sid = load_session()
    if cached_sid and validate_session(cached_sid):
        return cached_sid

    # If no valid cached session, request a new one
    if not PIHOLE_PASSWORD:
        # Try to access without authentication (if local API auth is disabled)
        return None

    auth_url = f"http://{PIHOLE_IP}:{PIHOLE_PORT}/api/auth"
    auth_data = json.dumps({"password": PIHOLE_PASSWORD}).encode('utf-8')

    try:
        request = urllib.request.Request(
            auth_url,
            data=auth_data,
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(request)
        result = json.load(response)

        # Check for the nested session structure (Pi-hole v6)
        if 'session' in result and 'sid' in result['session']:
            # Store CSRF token if available for future requests
            global csrf_token
            if 'csrf' in result['session']:
                csrf_token = result['session']['csrf']

            # Save the session for future use
            sid = result['session']['sid']
            save_session(sid, csrf_token)
            return sid
        # Fallback for older API format
        elif 'sid' in result:
            sid = result['sid']
            save_session(sid, None)
            return sid

        # If we get here, no valid session ID was found
        sys.exit(f"Failed to find session ID in authentication response: {result}")
    except Exception as e:
        sys.exit(f"Failed to authenticate: {str(e)}")


session_id = get_session_id()

# With V6 API, we need to make separate requests
headers = {}
if session_id:
    # Pi-hole v6 accepts the session ID in various ways
    # Try setting it as both a header and in a cookie
    headers['sid'] = session_id
    headers['Cookie'] = f'sid={session_id}'

    # Add CSRF token if available
    if csrf_token:
        headers['X-CSRF-Token'] = csrf_token

# Get system info
system_url = f"http://{PIHOLE_IP}:{PIHOLE_PORT}/api/info/system"

try:
    request = urllib.request.Request(system_url, headers=headers)
    response = urllib.request.urlopen(request)
    system_info = json.load(response)
except Exception as e:
    output_string = "Error fetching system info.\nRun pihole-dashboard-draw\nfor details."
    # draw_dashboard(output_string)
    output_error = f"System Info API Response Error: {str(e)}"
    sys.exit(output_error)

# Grab the system load averages (1, 5, 15 minute)
try:
    load_one = system_info["system"]["cpu"]["load"]["raw"][0]
    load_five = system_info["system"]["cpu"]["load"]["raw"][1]
    load_fifteen = system_info["system"]["cpu"]["load"]["raw"][2]
except Exception as e:
    output_error = f"Load averages went wrong: {str(e)}"
    sys.exit(output_error)

# Unix convention includes trailing zeroes on rounded load averages
#if len(load_one) < 4:
#    load_one = load_one + "0"
#if len(load_five) < 4:
#    load_five = load_five + "0"
#if len(load_fifteen) < 4:
#    load_fifteen = load_fifteen + "0"

loads = f"[⏻] Load average: {load_one:.2f}, {load_five:.2f}, {load_fifteen:.2f}"

print(loads)

# Get diagnosis messages
system_url = f"http://{PIHOLE_IP}:{PIHOLE_PORT}/api/info/messages/count"

try:
    request = urllib.request.Request(system_url, headers=headers)
    response = urllib.request.urlopen(request)
    message_count = json.load(response)
except Exception as e:
    output_string = "Error fetching message count.\nRun pihole-dashboard-draw\nfor details."
    # draw_dashboard(output_string)
    output_error = f"Message Count API Response Error: {str(e)}"
    sys.exit(output_error)

if message_count["count"] > 0:
    diagnosis_messages = "[×] " + str(message_count["count"]) + " diagnosis messages"
else:
    diagnosis_messages = "[✓] No diagnosis messages"

print(diagnosis_messages)
