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
# Imports the pprint library to print the http response in a pretty format
from pprint import pprint
# Imports the requests library for making HTTP requests
import requests

# Disables unverified HTTPS requests warning
requests.urllib3.disable_warnings()

# Variables that will be used for RESTCONF authentication
HOST = "sandbox-iosxe-latest-1.cisco.com"
USERNAME = "developer"
PASSWORD = "C1sco12345"
PORT = '443'

# Headers that tell the server that we are sending/receiving YANG data in json format
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def get_interfaces(host: str=HOST, username: str=USERNAME,
                   password: str=PASSWORD, port: str=PORT, interface=None) -> dict:
    """GET RESTCONF function request to gather devices interfaces

    Args:
        host (str): hostname or ip of device
        username (str): API username for authentication
        password (str): API user password for authentication
        port (str): port for API uri
        interface (str): Name of interface

    return: None
    """
    if interface:
        url = (f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces/"\
                "?interface={interface}")
    else:
        url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces"
    response = requests.get(url=url, headers=HEADERS, auth=(username, password), verify=False)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Print interfaces in pretty dictionary format
    pprint(get_interfaces())
