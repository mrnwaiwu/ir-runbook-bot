# IR Runbook Bot — Usage Guide

This document covers common usage patterns and operational tips for the IR Runbook Bot.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set required environment variables
export SLACK_BOT_TOKEN=xoxb-...
export OPENAI_API_KEY=sk-...

# Run the bot
python app.py
```

## Triggering a Runbook

The bot listens for incident keywords in configured Slack channels. You can also trigger runbooks directly via slash command:

```
/runbook <incident-type>
```

Supported incident types:
- `data-breach` — Data exfiltration or unauthorized access
- `ransomware` — Ransomware detection and containment
- `ddos` — Distributed denial-of-service mitigation
- `insider-threat` — Insider threat investigation
- `phishing` — Phishing campaign response
- `credential-compromise` — Compromised credential containment

## Running a Runbook Manually

```python
from runbook import RunbookEngine

engine = RunbookEngine()
result = engine.run(incident_type="data-breach", severity="high")
print(result.summary())
```

## Severity Levels

| Level    | Response SLA | Auto-escalate |
|----------|-------------|---------------|
| Critical | 15 min      | Yes (PagerDuty) |
| High     | 1 hour      | Yes (Slack DM) |
| Medium   | 4 hours     | No |
| Low      | 24 hours    | No |

## Customizing Runbooks

Add or edit runbook templates in `runbook.py`. Each runbook is a Python class
inheriting from `BaseRunbook` with a `steps` list and optional `rollback` method.

```python
class CustomRunbook(BaseRunbook):
    incident_type = "custom-event"
    steps = [
        "Identify affected systems",
        "Isolate the blast radius",
        "Notify stakeholders",
        "Begin remediation",
        "Post-incident review",
    ]
```

## Logging & Audit Trail

All runbook executions are logged to `logs/ir-audit.log` with timestamps,
operator ID, and step completion status. Retain logs per your organization's
compliance policy (recommended: 1 year minimum).

## Troubleshooting

- **Bot not responding in Slack**: Verify `SLACK_BOT_TOKEN` is valid and the bot is invited to the channel.
- **Runbook not found**: Check that `incident_type` matches a registered runbook class.
- **OpenAI errors**: Ensure your API key has sufficient quota and the model specified in config is available.
