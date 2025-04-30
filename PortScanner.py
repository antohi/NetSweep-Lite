import re
import subprocess
import logging
import requests
from dotenv import load_dotenv
import os

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
            port = f"{port}/{protocol} - {state.upper()} ({service})"
            logging.info(port)
            print(port)

    def format_banner_scan(self, s):
        banners = re.findall(r"(\d+)/(tcp|udp)\s+(\w+)\s+([\S]+)\s*(.*)", s)
        for  port, protocol, state, service, version_info in banners:
            banner = f"Port: {port}/{protocol}, State: {state}, Service: {service}, Version: {version_info}"
            self.scanned_services_db[service] = version_info
            logging.info(banner)
            print(banner)

    def check_risk(self):
        load_dotenv()
        api_key = os.getenv("NVD_API_KEY")
        headers = {
            "apiKey": api_key
        }

        params = {
            "keywordSearch": "openssh"
        }

        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0?", headers=headers, params=params)
        vulnerabilities = response.json().get("vulnerabilities", [])
        print(vulnerabilities)

        for vuln in vulnerabilities:
            cve_id = vuln['cve']['id']
            description = vuln['cve']['descriptions'][0]['value']
            score_data = vuln['cve'].get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {})
            severity = score_data.get('baseSeverity', 'UNKNOWN')
            score = score_data.get('baseScore', 'N/A')
            print(cve_id, description, score, severity)


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


