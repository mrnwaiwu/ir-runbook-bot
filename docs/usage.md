# IR Runbook Bot — Usage Guide

## Overview

`ir-runbook-bot` automates incident response playbook execution by integrating with your alerting stack and triggering pre-defined runbooks based on alert type and severity.

## Getting Started

### Prerequisites

- Python 3.10+
- A configured `config.yaml` (see `config.example.yaml`)
- Slack webhook URL or PagerDuty API key for notifications

### Installation

```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml
# Edit config.yaml with your credentials and runbook mappings
```

### Running the Bot

```bash
python main.py --config config.yaml
```

## Triggering a Runbook

Runbooks are triggered automatically when an alert is received via the webhook endpoint:

```
POST /webhook/alert
Content-Type: application/json

{
  "alert_name": "HighCPUUsage",
  "severity": "critical",
  "service": "api-gateway",
  "timestamp": "2026-06-13T10:00:00Z"
}
```

The bot maps `alert_name` to a runbook in `runbooks/` and executes each step sequentially.

## Manual Execution

To run a specific runbook manually:

```bash
python main.py --runbook runbooks/high_cpu.yaml --dry-run
```

Remove `--dry-run` to execute live steps.

## Runbook Format

Runbooks are YAML files in the `runbooks/` directory:

```yaml
name: High CPU Usage
steps:
  - action: notify_slack
    message: "High CPU detected on {{ service }}"
  - action: scale_up
    target: "{{ service }}"
    replicas: 3
  - action: collect_logs
    duration: 300
```

## Logging

All executions are logged to `logs/runbook.log` with step-level detail and timestamps.
