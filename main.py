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
from ipaddress import ip_network
from rich.console import Console
from rich.table import Table
from get_operational import get_interf_operational
from get_interfaces import get_interfaces


console = Console()

def main():
    """
    Prints table with DevNet Always-On Sandbox interfaces status

    return: None
    """
    # Prints the table to the terminal window
    console.print(create_table())


def create_table() -> Table:
    """
    Calls function GET interface info and print results

    return: Table
    """
    # Creates Table with Headers
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Interface Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="cyan", no_wrap=True)
    table.add_column("IP Address", justify="left", style="cyan", no_wrap=True)
    table.add_column("Mac Address", justify="left", style="cyan", no_wrap=True)
    table.add_column("Up/Down", justify="left")
    table.add_column("Last Modified", justify="left", style="cyan", no_wrap=True)

    # GET request to get interface operational data
    operational = get_interf_operational()

    # Counter for each interface
    i = 1

    # for loop to add interface data to Table
    for interface in operational['ietf-interfaces:interfaces-state']['interface']:
        style = "green" if interface['admin-status'] == "up" else "bold red"
        interface_info = get_interfaces(interface=interface['name'].strip())
        if interface_info['ietf-interfaces:interface'].get('ietf-ip:ipv4'):
            address = (interface_info['ietf-interfaces:interface'].get('ietf-ip:ipv4')
                       ['address'][0]['ip'])
            subnet = (interface_info['ietf-interfaces:interface'].get('ietf-ip:ipv4')
                      ['address'][0]['netmask'])
            ip_address = ip_network(f"{address}/{subnet}", strict=False)
        else:
            ip_address = None
        table.add_row(f"{i}. {interface['name']}",
                      interface_info['ietf-interfaces:interface'].get('description'),
                      str(ip_address), interface['phys-address'],
                      interface['admin-status'],
                      interface['last-change'], style=style)
        i += 1

    # Returns a fully populated table
    return table

if __name__ == "__main__":
    # Calls the main function to print the table
    main()
