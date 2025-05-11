
import pytest
import requests
from src.RiskScanner import RiskScanner

# Mock JSON response class
class DummyJSONResponse:
    status_code = 200

    # Mock JSON metadate for response
    def json(self):
        return {
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-TEST",
                        "descriptions": [{"value": "SUPER HIGH SECURITY THREAT AHHH"}],
                        "metrics": {
                            "cvssMetricV31": [
                                {"cvssData": {"baseSeverity": "CRITICAL", "baseScore": 9.9}}
                            ]
                        },
                        "configurations": {
                            "nodes": [
                                {"cpeMatch": [{"criteria": "cpe:2.3:a:test:test:1.0"}]}
                            ]
                        }
                    }
                }
            ]
        }

# Tests check_risk func with dummy JSON data
def test_check_risk(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyJSONResponse())

    scanner = RiskScanner()
    results = scanner.check_risk("test")

    assert results[0]['cve_id'] == 'CVE-TEST'
    assert 'Test description' in results[0]['description']

# Tests format_risks func to verify proper results are printed and filtered out
def test_format_risks(capsys):
    scanner = RiskScanner()
    results = [
        {"cve_id": "CVE-LOW",   "description": "Low severity",       "severity": "LOW",      "score": 2.0},
        {"cve_id": "CVE-HIGH1", "description": "High severity 1",     "severity": "HIGH",     "score": 7.5},
        {"cve_id": "CVE-HIGH2", "description": "High severity 2",     "severity": "HIGH",     "score": 8.0},
        {"cve_id": "CVE-CRIT",  "description": "Critical severity",  "severity": "CRITICAL", "score": 9.5},
    ]

    scanner.format_risks(results, min_severity="HIGH", top_n=2)

    captured = capsys.readouterr().out
    print(captured)

    assert "CVE-CRIT" in captured
    assert "CVE-HIGH2" in captured
    assert "CVE-HIGH1" not in captured
    assert "CVE-LOW" not in captured
    assert "Score:" in captured


def test_process_banners(monkeypatch, capsys):
    scanner = RiskScanner()
    dummy_cves = [
        {
            "cve_id": "CVE-dumb-dumb",
            "description": "dumb-dumb description",
            "severity": "HIGH",
            "score": 7.1
        }
    ]

    monkeypatch.setattr(scanner, "check_risk", lambda product: dummy_cves)
    banner_output = "22/tcp open ssh OpenSSH 7.9\n"

    scanner.process_banners(banner_output)
    captured = capsys.readouterr().out

    assert "PORT: 22/tcp | STATE: OPEN | SERVICE: ssh | VERSION: OpenSSH 7.9" in captured



