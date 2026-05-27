# IR Runbook Bot — Usage Guide

## Overview

The IR Runbook Bot automates incident response workflows by mapping alert types to predefined runbooks and executing remediation steps.

## Supported Incident Types

| Incident Type | Runbook | Auto-Remediate |
|---|---|---|
| Brute force login | `brute_force.md` | Yes (block IP) |
| Data exfiltration | `data_exfil.md` | No (manual review) |
| Malware detection | `malware.md` | Yes (isolate host) |
| Privilege escalation | `priv_esc.md` | No (page on-call) |
| DDoS | `ddos.md` | Yes (rate limit) |

## Running the Bot

```bash
# Start the bot
python app.py

# Trigger a specific runbook manually
python runbook.py --type brute_force --target 192.168.1.10
```

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | Yes |
| `JIRA_API_TOKEN` | Jira token for ticket creation | No |
| `AUTO_REMEDIATE` | Enable auto-remediation (`true`/`false`) | No (default: false) |

## Adding a New Runbook

1. Create a new `.md` file in `runbooks/`
2. Add the incident type mapping in `runbook.py`
3. Optionally add an auto-remediation handler

## Alerting

The bot sends alerts to Slack for every incident triggered. Set `AUTO_REMEDIATE=true` to allow the bot to take automated action without human approval for supported incident types.
