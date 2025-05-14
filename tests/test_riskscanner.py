# tests/test_RiskScanner2.py

import os

import pytest
from src.RiskScanner import RiskScanner


def test_scan_banners(monkeypatch):
    sample_output = """
    22/tcp open  ssh  OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
    80/tcp open  http Apache httpd 2.4.41 ((Ubuntu))
    """

    def mock_subprocess_run(*args, **kwargs):
        class MockProcess:
            def __init__(self):
                self.stdout = sample_output
                self.stderr = ""

        return MockProcess()

    monkeypatch.setattr("subprocess.run", mock_subprocess_run)
    scanner = RiskScanner()
    scanner.process_banners = lambda output: True  # Mock to avoid actual processing
    assert scanner.scan_banners("127.0.0.1") is None

def test_print_kevs_no_kevs_detected(capfd):
    scanner = RiskScanner()
    scanner.print_kevs({})
    captured = capfd.readouterr()
    assert "[+] No KEV found" in captured.out


def test_print_kevs_with_kevs_detected(capfd):
    kevs_detected = {
        "CVE-2023-12345": ["OpenSSH", "OpenSSH 8.2p1", "Vulnerability A", "2023-01-01", "Test vulnerability",
                           "Test notes"]
    }
    scanner = RiskScanner()
    scanner.print_kevs(kevs_detected)
    captured = capfd.readouterr()
    assert "CVE-2023-12345" in captured.out
    assert "Vulnerability A" in captured.out
    assert "OpenSSH" in captured.out



