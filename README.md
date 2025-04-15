# NetworkChecker 🛠️🌐

**NetworkChecker** is a Python-based network diagnostics and cybersecurity tool I've been building while studying for my A+ and Net+ exams. It allows users to:

- Ping individual or ranges of IP addresses
- Perform quick or targeted port scans using Nmap
- Log detailed system, network, and scan information
- View and log scan results with clean formatting
- Leverage concurrency for fast batch scanning

---

## Features

- ✅ IP Ping Tool with Range Support
- ✅ Port Scanner with Single & Top-Port Modes
- ✅ Local System & Network Info Logging
- ✅ Threaded Concurrent Scanning
- ✅ Regex-based Output Formatting
- ✅ Scan Result Logging (to `net_log.txt`)

---

# Tutorial

Clone this repo to your local machine:
`git clone https://github.com/antohi/NetworkChecker.git`

Install the required Python dependencies:
`pip install -r requirements.txt`

Run the Program
`python network_checker.py`

---
# Screenshots
## Console Output 

IP Ping Output (Single IPs and Range):

![Scan Results](Assets/Screenshots/CMLOutputPings.png)

Single Port Scans for IP:

![Scan Results](Assets/Screenshots/cml_singleport.png)

Quick Scans (Top 10 Ports in IP):

![Scan Results](Assets/Screenshots/cml_quickscan.png)


## Net_Log Output
Net_Log holds program output for future reference and troubleshooting in the form of a txt file

Net_Log Ping Tool Output:
![Terminal View](Assets/Screenshots/Net_Log_Output_Pings.png)

Net_Log Output for Port Scanner
![Terminal View](Assets/Screenshots/portscanner_netlog.png)

---

# Future ideas: 
- Scan multiple ports and filter by opened
- Traceroute

