import logging
import re
import subprocess

import requests
import os
import textwrap
from dotenv import load_dotenv

class RiskScanner:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NVD_API_KEY")
        self.risk_db = {}

        self.risk_logger = logging.getLogger("RiskScanner")
        self.risk_logger.setLevel(logging.INFO)
        handler = logging.FileHandler("risk_log.txt")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.risk_logger.addHandler(handler)
        self.scan_history = []

    # Initiates banner scan using nmap
    def scan_banners(self, host):
        scan = subprocess.run(
            ["nmap", "-sV", host],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        print("\n\n=== SERVICE RISK SCAN ===")
        self.process_banners(scan.stdout) # Formats banner scan results to extract

    # Extracts detailed banner info in order to check the risk of found cves and format them
    def process_banners(self, output):
        pattern = r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+([\S]+)\s*(.*)"
        for port, proto, state, service, version in re.findall(pattern, output):
            # Map generic 'domain' service to actual product
            product = version if service == "domain" else service
            header = f"PORT: {port}/{proto} | STATE: {state.upper()} | SERVICE: {product} | VERSION: {version}"
            print(header)
            self.risk_logger.info(header)

            # Fetch and display relevant CVEs
            cves = self.check_risk(product)
            self.format_risks(cves)

            print("=" * 60)

    # Calls NVD api to extract vulnerability info from json response
    def check_risk(self, product):
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        headers = {"apiKey": self.api_key}
        params = {"keywordSearch": product}

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print("[!] NVD API query failed or no data.")
                return []

            results = []
            data = response.json().get("vulnerabilities", [])
            for item in data:
                meta = item['cve']
                # Filter by CPE criteria
                nodes = meta.get('configurations', {}).get('nodes', [])

                if not any(
                    any(product.lower() in cm['criteria'].lower() for cm in node.get('cpeMatch', []))
                    for node in nodes
                ):
                    continue

                # Matches each risk criteria to metadata values
                cve_id = meta['id']
                desc = meta['descriptions'][0]['value']
                cvss = meta.get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {})
                severity = cvss.get('baseSeverity', 'UNKNOWN')
                score = cvss.get('baseScore', 'N/A')

                # Adds the values found into a dictionary
                entry = {
                    "cve_id": cve_id,
                    "description": desc,
                    "severity": severity,
                    "score": score
                }
                self.risk_db[cve_id] = entry # Adds to the database of risks
                results.append(entry) # Adds entry to current results
                self.scan_history.append(entry) # Adds the scan to the last scan history

            return results

        except Exception as e:
            print(f"[ERROR] CVE lookup failed: {e}") # Issues contacting API
            return []

    # Formats risks based on the minimum severity
    def format_risks(self, results, min_severity="LOW", top_n=3):
        order = ["UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"] # Sets up order from lowest risk to critical risks
        # Log every CVE
        for e in results:
            self.risk_logger.info(f"{e['cve_id']} | {e['severity']} | {e['score']} | {e['description'][:50]}...")

        # Filter and sort
        filtered = [e for e in results if order.index(e['severity']) >= order.index(min_severity)]
        filtered.sort(key=lambda e: (e['score'] if isinstance(e['score'], (int, float)) else 0), reverse=True)

        # If no results were found for the specified min_severity
        if not filtered:
            print("[+] No CVEs at or above severity:", min_severity)
            return
        # Prints cve information and risk
        for e in filtered[:top_n]:
            print(f"\n[!] {e['cve_id']}  ({e['severity']})")
            print(f"[!] Description:\n{textwrap.fill(e['description'], width=80)}")
            print(f"[!] Score: {e['score']}\n")

    # Formats and retrieves scan history
    def get_scan_history(self):
        reversed_scans = list(reversed(self.scan_history)) # Reverses to display more recent scan first
        self.format_risks(reversed_scans)
        return reversed_scans







