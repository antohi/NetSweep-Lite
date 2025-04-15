import re
import subprocess
import logging

class PortScanner:
    # Scan a single port based on an IP address
    def scan_single_port(self, port, host):
        scan_cmd = ["nmap", "-p", port, host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return self.format_scan(s.stdout)

    # Formats output of scan to make more readable when printing/logging
    def format_scan(self, s):
        match = re.search(r"(\d+)/(tcp|udp)\s+(open|filtered|closed)", s)
        if match:
            port, protocol, state = match.groups()
            logging.info(f"[SUCCESS] {port}/{protocol} Status: {state}")
            return f"Port {port}/{protocol} was found. Status: {state}"
        else:
            logging.error("The was an issue finding this port.")
            return "[ERROR] Port was not found"

# Work in progress, functionality for scanning top ports, locating opened ones.
"""
    def find_open_ports(self, s):
        format = re.findall("(\d+)/(tcp|udp)\s+open", s)

    def scan_top_ports(self, host):
        scan_cmd = ["nmap", "--scan-ports", host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return s.stdout
"""
