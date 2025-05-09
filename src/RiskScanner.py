import logging
import re
import subprocess
import requests
from dotenv import load_dotenv
import os
import textwrap

class RiskScanner:
    def __init__(self):
        self.scanned_services_db = {}
        self.risk_db = {}

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

    # Nmap banners detection
    def scan_banners(self, host):
        scan_cmd = ["nmap", "-sV", host]
        s = subprocess.run(scan_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\n\n===SERVICE SCAN RESULTS===")
        logging.info("\n\n===SERVICE SCAN RESULTS===")
        return self.format_banner_scan(s.stdout)

    def format_banner_scan(self, s):
        banners = re.findall(r"(\d+)/(tcp|udp)\s+(\w+)\s+([\S]+)\s*(.*)", s)
        for  port, protocol, state, service, version_info in banners:
            banner = f"PORT: {port}/{protocol} | STATE: {state.upper()} | SERVICE: {service} | VERSION: {version_info}"
            print(banner)
            self.check_risk(service, version_info)
            print("=" * 60)
            logging.info(banner)