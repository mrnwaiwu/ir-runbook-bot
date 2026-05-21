# ir-runbook-bot

AI-powered incident response runbook generator. Feed it a raw alert or IOC, and it returns a full IR runbook — classified by MITRE ATT&CK tactic, severity-scored, and formatted for immediate action.

## Features
- **AI classification** — GPT-4o maps the alert to a MITRE ATT&CK tactic and technique
- **Auto-generated runbook** — containment, eradication, recovery, and lessons-learned steps
- **HIPAA breach assessment** — flags if the incident triggers PHI breach notification requirements
- **Evidence checklist** — auto-generated based on incident type
- **Multi-format output** — Markdown, JSON, and PDF
- **REST API** — Flask endpoint for SIEM/SOAR integration
- **Slack webhook** — optional real-time team notification

## Setup

```bash
pip install openai flask fpdf2 requests
export OPENAI_API_KEY=your_key
export SLACK_WEBHOOK_URL=your_webhook   # optional

python app.py          # start the API server
python runbook.py      # run CLI with sample alert
```

## API Usage

```bash
curl -X POST http://localhost:5000/api/runbook \
  -H "Content-Type: application/json" \
  -d '{"alert": "Outbound connection to known C2 IP 45.33.32.156:4444 from host web01"}'
```

## Tech Stack
Python · OpenAI GPT-4o · Flask · fpdf2 · MITRE ATT&CK · HIPAA
