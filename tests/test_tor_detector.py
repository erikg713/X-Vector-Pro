import pytest
from engine.network.tor_detector import run_detection

@pytest.mark.parametrize("target,expected", [
    ("suspicious.onion", "stealth"),
    ("185.220.101.45", "stealth"),
    ("154.35.10.1", "stealth"),
    ("51.15.12.34", "stealth"),
    ("example.com", "clear"),
    ("256.300.0.1", "clear"),  # Invalid IP
])
def test_run_detection(target, expected):
    result = run_detection(target)
    assert result["status"] == expected
    assert "details" in result
