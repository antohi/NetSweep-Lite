import csv
import json
import logging
import re
import subprocess
import os
from dotenv import load_dotenv
import datetime


class RiskScanner:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NVD_API_KEY")
        self.service_map = { # Map of nmap services to common vendors in CISA
            "ssh": "OpenSSH",
            "http": "Apache",
            "microsoft-ds": "SMB",
            "smtp": "Postfix",
            "dns": "BIND",
            "imap": "Dovecot",
            "ftp": "vsftpd",
            "mysql": "MySQL",
            "msrpc": "RPC",
            "tcpwrapped": "generic",
            "telnet": "Telnet",
        }

    # Initiates banner scan using nmap
    def scan_banners(self, host):
        scan = subprocess.run(
            ["nmap", "-sV", host],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        print("\n\n=== SERVICE RISK SCAN ===")
        self.process_banners(scan.stdout) # Formats banner scan results to extract

    # Extracts detailed banner info in order to check if any KEVs match
    def process_banners(self, output):
        pattern = r"(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+([\S]+)\s*(.*)"
        for port, proto, state, service, version in re.findall(pattern, output):
            # Map generic 'domain' service to actual product
            product = version if service == "domain" else service
            header = f"PORT: {port}/{proto} | STATE: {state.upper()} | SERVICE: {product} | VERSION: {version}"

            mapped_product = self.service_map.get(service.lower(), product)
            print(header)
            kevs = self.detect_kevs(mapped_product)

            if isinstance(kevs, dict):
                if kevs:
                    self.print_kevs(kevs)
                    self.log_kevs(kevs)
                else:
                    print("[+] No KEV found")
            else:
                print(kevs)  # This prints the error message string
            print("=" * 60)

    # Scans kev.csv to find similar vulnerabilities
    def detect_kevs(self, product):
        kevs_detected = {}
        try:
            with open("../assets/catalogs/known_exploited_vulnerabilities.csv") as kev:
                reader = csv.DictReader(kev)
                for row in reader:
                    if product.lower() in row["product"].lower() or product.lower() in row["vendorProject"].lower():
                        info = [row["vendorProject"], row["product"], row["vulnerabilityName"], row["dateAdded"], row["shortDescription"], row["notes"]]
                        kevs_detected[row["cveID"]] = info
                    else:
                        continue
                return kevs_detected
        except FileNotFoundError as e:
            return f"[!] ERROR READING CISA KEVs: {e}"

    # Prints found KEVs for console UI
    def print_kevs(self, kevs_detected):
        if not kevs_detected:
            print("[+] No KEV found")
        else:
            for kev in kevs_detected:
                print(f"[!!] {kev} – {kevs_detected[kev][2]}")
                print(f"     Description: {kevs_detected[kev][4]}")
                print(f"     Vendor: {kevs_detected[kev][0]}, Product: {kevs_detected[kev][1]}")
                print(f"     Added: {kevs_detected[kev][3]}\n")

    # Logs KEVs found to kev_log.csv for exports
    def log_kevs(self, kevs_detected):
        try:
            csv_path = "../logs/kev_log.csv"
            # CSV
            with open(csv_path, 'w') as f:
                f.write(
                    "cveID,vendor,product,description,added,time_of_scan\n")
                for kev in kevs_detected:
                    f.write(
                        f"{kev},{kevs_detected[kev][0]},"
                        f"{kevs_detected[kev][1]},{kevs_detected[kev][4]},"
                        f"{kevs_detected[kev][3]}, {datetime.datetime.now()}\n"
                    )
        except Exception as e:
            logging.error(f"[!] ERROR: Unable to write report CSV file. Exception: {e}")















