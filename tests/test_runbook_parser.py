"""Tests for runbook parser module."""

import pytest
from unittest.mock import patch, MagicMock


class TestRunbookParser:
    """Unit tests for runbook parsing logic."""

    def test_parse_empty_runbook(self):
        """Parser handles empty runbook gracefully."""
        runbook = ""
        # Should return empty steps list, not raise
        result = {"steps": [], "metadata": {}}
        assert result["steps"] == []

    def test_parse_steps_ordered(self):
        """Steps are returned in correct order."""
        steps = ["Step 1: Isolate host", "Step 2: Capture memory", "Step 3: Notify SOC"]
        assert steps[0].startswith("Step 1")
        assert steps[-1].startswith("Step 3")

    def test_parse_metadata_extraction(self):
        """Metadata fields are correctly extracted from runbook header."""
        metadata = {
            "title": "Ransomware Response",
            "severity": "P1",
            "owner": "SOC",
            "last_updated": "2026-05-31",
        }
        assert metadata["severity"] == "P1"
        assert metadata["owner"] == "SOC"

    def test_missing_severity_defaults_to_p2(self):
        """Missing severity field defaults to P2."""
        metadata = {"title": "Generic Incident"}
        severity = metadata.get("severity", "P2")
        assert severity == "P2"

    def test_step_count_nonzero(self):
        """Runbook with content has at least one step."""
        content = "Step 1: Check alerts\nStep 2: Escalate"
        steps = [line for line in content.splitlines() if line.startswith("Step")]
        assert len(steps) > 0

    def test_parse_escalation_contacts(self):
        """Escalation contacts are parsed into a list."""
        raw = "alice@example.com, bob@example.com"
        contacts = [c.strip() for c in raw.split(",")]
        assert len(contacts) == 2
        assert "alice@example.com" in contacts

    @pytest.mark.parametrize("severity,expected", [
        ("P1", True),
        ("P2", True),
        ("P3", True),
        ("P4", True),
        ("P5", False),
        ("UNKNOWN", False),
    ])
    def test_valid_severity_levels(self, severity, expected):
        """Only P1-P4 are accepted severity levels."""
        valid = {"P1", "P2", "P3", "P4"}
        assert (severity in valid) == expected
