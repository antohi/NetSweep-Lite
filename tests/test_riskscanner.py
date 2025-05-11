
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
                        "descriptions": [{"value": "Test description"}],
                        "metrics": {
                            "cvssMetricV31": [
                                {"cvssData": {"baseSeverity": "MEDIUM", "baseScore": 5.0}}
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

# Tests check_risk function with dummy JSON data
def test_check_risk(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyJSONResponse())

    scanner = RiskScanner()
    results = scanner.check_risk("test")

    assert results[0]['cve_id'] == 'CVE-TEST'
    assert 'Test description' in results[0]['description']




