import re
import subprocess
import logging
import requests
from dotenv import load_dotenv
import os
import textwrap


class PortScanner:
    def __init__(self):
        self.scanned_services_db = {}
        self.risk_db = {}
    # Scan a single port based on an IP address
    def scan_single_port(self, port, host):
        scan_cmd = ["nmap", "-p", port, host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("\n\n===SINGLE SCAN RESULTS===")
        print("\n\n===SINGLE SCAN RESULTS===")
        return self.format_port_scan(s.stdout)

    # Formats output of scan to make more readable when printing/logging
    def format_port_scan(self, s):
        ports = re.findall(r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(\S+)", s)
        for port, protocol, state, service in ports:
            port = f"PORT: {port}/{protocol} | STATE: {state.upper()} | SERVICE: ({service})"
            logging.info(port)
            print(port)

    def format_banner_scan(self, s):
        banners = re.findall(r"(\d+)/(tcp|udp)\s+(\w+)\s+([\S]+)\s*(.*)", s)
        for  port, protocol, state, service, version_info in banners:
            banner = f"PORT: {port}/{protocol} | STATE: {state.upper()} | SERVICE: {service} | VERSION: {version_info}"
            print(banner)
            self.check_risk(service, version_info)
            print("=" * 60)
            logging.info(banner)

    def check_risk(self, service, version_info):
        load_dotenv()
        api_key = os.getenv("NVD_API_KEY")
        headers = {
            "apiKey": api_key
        }

        params = {
            "keywordSearch": f"{service} {version_info}"
        }

        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0?", headers=headers, params=params)
        try:
            vulnerabilities = response.json().get("vulnerabilities", [])
            if response.status_code != 200:
                print("No vulnerabilities in NVD database found.")

            for vuln in vulnerabilities:
                cve_id = vuln['cve']['id']
                description = vuln['cve']['descriptions'][0]['value']
                score_data = vuln['cve'].get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {})
                severity = score_data.get('baseSeverity', 'UNKNOWN')
                score = score_data.get('baseScore', 'N/A')

                print(f"\nCVE: {cve_id}")
                print(f"Description:\n{textwrap.fill(description, width=80)}")
                print(f"Score: {score} ({severity})\n")
        except Exception as e:
            print(f"Error: {e}")


    # Scans top 10 ports using nmap's --top-ports functionality
    def quick_scan(self, host):
        scan_cmd = ["nmap", "--top-ports", "10", host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("\n\n===QUICK SCAN RESULTS===")
        print("\n\n===QUICK SCAN RESULTS===")
        return self.format_port_scan(s.stdout)

    # Scans top 25 ports using nmap's --top-ports functionality
    def deep_scan(self, host):
        scan_cmod = ["nmap", "--top-ports", "25", host]
        s = subprocess.run(scan_cmod, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("\n\n===DEEP SCAN RESULTS===")
        print("\n\n===DEEP SCAN RESULTS===")
        return self.format_port_scan(s.stdout)

    # Nmap banners detection
    def scan_banners(self, host):
        scan_cmd = ["nmap", "-sV", host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\n\n===SERVICE SCAN RESULTS===")
        logging.info("\n\n===SERVICE SCAN RESULTS===")
        return self.format_banner_scan(s.stdout)


