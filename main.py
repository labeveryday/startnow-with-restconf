#!/usr/bin/env python
"""
    Copyright 2016 Cisco Systems All rights reserved.
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are
 met:
     * Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.
 The contents of this file are licensed under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with the
 License. You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations under
 the License.
"""
import json
from datetime import datetime
import requests

# Disables unverified HTTPS requests warning
requests.urllib3.disable_warnings()

# Headers that tell the server that we are sending/receiving YANG data in json format
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def get_date() -> str:
    "Return Today's date in Month-Day-Year"
    return datetime.today().strftime('%m-%d-%Y')

def get_run_config(host: str, username: str, password: str, port: str='443') -> dict:
    """GET RESTCONF request to gather current running config

    Args:
        host (str): hostname or ip of device
        username (str): API username for authentication
        password (str): API user password for authentication
        port (str): port for API uri

    return: dict
    """
    url = f"https://{host}:{port}/restconf/data/native"
    response = requests.get(url=url, headers=HEADERS, auth=(username, password), verify=False)
    response.raise_for_status()
    if response.ok:
        return response
    return None

def backup_config(config: dict) -> str:
    """Store running config as json

    Args:
        config (str): running-config in dictionary format

    return: None
    """
    hostname = config['Cisco-IOS-XE-native:native']['hostname']
    today = get_date()
    with open(f"./backups/{hostname}_{today}.json", "w") as file:
        json.dump(config, file, indent=2)


if __name__ == "__main__":
    creds = {
        "host": "sandbox-iosxe-latest-1.cisco.com",
        "username": "developer",
        "password": "C1sco12345"
    }
    print("-" * 20)
    print("Please wait while gathering device running config....")
    running_config = get_run_config(**creds)
    backup_config(running_config.json())
    print("Config has been backup successfully.")
    print("-" * 20)
