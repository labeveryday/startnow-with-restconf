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

from requests.models import Response

requests.urllib3.disable_warnings()

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def get_date() -> str:
    "Return Today's date in Month-Day-Year"
    return datetime.today().strftime('%m-%d-%Y')

def get_modules(hostname: str, username: str, password: str, port: str='443') -> list:
    """GET all YANG modules on a devices"""
    url = f"https://{hostname}:{port}/restconf/data/ietf-yang-library:modules-state"
    response = requests.get(url=url, headers=HEADERS, auth=(username, password), verify=False)
    response.raise_for_status()
    if response.ok:
        return response.json()['ietf-yang-library:modules-state']['module']
    return None

def get_run_config(hostname: str, username: str, password: str, port: str='443') -> Response:
    """GET RESTCONF request to gather current running config"""
    url = f"https://{hostname}:{port}/restconf/data/native"
    response = requests.get(url=url, headers=HEADERS, auth=(username, password), verify=False)
    response.raise_for_status()
    if response.ok:
        return response
    return None

def get_interfaces(hostname: str, username: str, password: str,
                   port: str='443', interface: str=None) -> Response:
    """GET RESTCONF request to gather devices interfaces"""
    if interface:
        url = (f"https://{hostname}:{port}/restconf/data/ietf-interfaces:interfaces/"\
                "?interface={interface}")
    else:
        url = f"https://{hostname}:{port}/restconf/data/ietf-interfaces:interfaces"
    response = requests.get(url=url, headers=HEADERS, auth=(username, password), verify=False)
    response.raise_for_status()
    if response.status_code == 200:
        return response
    return None

def save_config(config: dict) -> None:
    """Store running config as json"""
    hostname = config['Cisco-IOS-XE-native:native']['hostname']
    today = get_date()
    with open(f"./backups/{hostname}_{today}.json", "w") as file:
        json.dump(config, file, indent=2)


if __name__ == "__main__":
    kwargs = {
        "hostname": "sandbox-iosxe-latest-1.cisco.com",
        "username": "developer",
        "password": "C1sco12345"
    }
    print("-" * 20)
    print("Please wait while gathering device running config....")
    running_config = get_run_config("sandbox-iosxe-latest-1.cisco.com", "developer", "C1sco12345")
    #save_config(running_config.json())
    print("Config has been saved successfully.")
    print("-" * 20)
    #print(running_config.json())
    modules = get_modules("sandbox-iosxe-latest-1.cisco.com", "developer", "C1sco12345")
    print(modules.json())
