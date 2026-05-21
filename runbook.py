"""
ir-runbook-bot
---------------
AI-powered incident response runbook generator.

Given a raw alert or IOC, this tool:
  1. Classifies the incident using GPT-4o
  2. Maps it to a MITRE ATT&CK tactic and technique
  3. Assesses HIPAA breach notification requirements
  4. Generates a full IR runbook (contain, eradicate, recover, review)
  5. Outputs Markdown and JSON

Usage:
  python runbook.py
  python runbook.py --alert "Ransomware detected on EHR server"
  python runbook.py --alert "..." --output runbook.md

Requires: pip install openai
"""

import os
import json
import argparse
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MITRE_TACTICS = {
    "Initial Access":       {"id": "TA0001"},
    "Execution":            {"id": "TA0002"},
    "Persistence":          {"id": "TA0003"},
    "Privilege Escalation": {"id": "TA0004"},
    "Defense Evasion":      {"id": "TA0005"},
    "Credential Access":    {"id": "TA0006"},
    "Discovery":            {"id": "TA0007"},
    "Lateral Movement":     {"id": "TA0008"},
    "Collection":           {"id": "TA0009"},
    "Exfiltration":         {"id": "TA0010"},
    "Command and Control":  {"id": "TA0011"},
    "Impact":               {"id": "TA0040"},
}

CLASSIFICATION_PROMPT = """
You are a senior incident response analyst with deep knowledge of MITRE ATT&CK and HIPAA regulations.

Given a security alert, return a JSON object with these exact keys:
  - incident_type: short label (e.g. "Ransomware", "Phishing", "Insider Threat", "C2 Beacon")
  - severity: one of CRITICAL | HIGH | MEDIUM | LOW
  - mitre_tactic: the most relevant MITRE ATT&CK tactic name
  - mitre_technique_id: e.g. T1486
  - mitre_technique_name: e.g. Data Encrypted for Impact
  - hipaa_phi_risk: true if this incident likely involves PHI exposure or breach, else false
  - hipaa_breach_notification_required: true if it meets HIPAA Breach Notification Rule threshold
  - affected_systems: list of likely affected system types
  - summary: 2-sentence plain-English summary of what happened and why it matters
"""

RUNBOOK_PROMPT = """
You are a senior incident responder. Based on the classification and alert below,
generate a detailed IR runbook.

Classification:
{classification}

Alert:
{alert}

Return a JSON object with these exact keys:
  - containment_steps: list of 5-8 specific, actionable containment steps
  - evidence_collection: list of 5-8 artifacts/logs to collect and preserve
  - eradication_steps: list of 4-6 steps to remove the threat
  - recovery_steps: list of 4-6 steps to restore normal operations safely
  - hipaa_actions: list of HIPAA-specific actions required
  - lessons_learned_template: list of 5 post-incident review questions
  - estimated_resolution_hours: integer
"""


def classify_alert(alert: str) -> dict:
    print("  [1/3] Classifying alert with GPT-4o...")
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": CLASSIFICATION_PROMPT},
            {"role": "user",   "content": f"Alert:\n{alert}"},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def generate_runbook_steps(alert: str, classification: dict) -> dict:
    print("  [2/3] Generating IR runbook steps...")
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a senior incident responder. Return only valid JSON."},
            {"role": "user",   "content": RUNBOOK_PROMPT.format(
                classification=json.dumps(classification, indent=2),
                alert=alert
            )},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def build_markdown(alert: str, classification: dict, runbook: dict) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    tactic = classification.get("mitre_tactic", "")
    mitre_id = MITRE_TACTICS.get(tactic, {}).get("id", "--")
    phi = classification.get("hipaa_phi_risk", False)
    breach = classification.get("hipaa_breach_notification_required", False)

    def bullets(items): return "\n".join(f"- {i}" for i in items)
    def checklist(items): return "\n".join(f"- [ ] {i}" for i in items)
    def numbered(items): return "\n".join(f"{n+1}. {i}" for n, i in enumerate(items))

    return f"""# Incident Response Runbook

| Field | Value |
|-------|-------|
| Generated | {now} |
| Incident Type | **{classification.get('incident_type', '--')}** |
| Severity | **{classification.get('severity', '--')}** |
| MITRE Tactic | {tactic} ({mitre_id}) |
| MITRE Technique | {classification.get('mitre_technique_id', '--')} -- {classification.get('mitre_technique_name', '--')} |
| PHI at Risk | {'YES - Potential PHI involved' if phi else 'Not indicated'} |
| Breach Notification | {'REQUIRED - Review HIPAA actions section' if breach else 'Not required at this time'} |
| Est. Resolution | {runbook.get('estimated_resolution_hours', '--')} hours |

## Alert
> {alert}

## Summary
{classification.get('summary', '')}

## Affected Systems
{bullets(classification.get('affected_systems', []))}

---

## Phase 1 -- Containment
{numbered(runbook.get('containment_steps', []))}

## Phase 2 -- Evidence Collection
{checklist(runbook.get('evidence_collection', []))}

## Phase 3 -- Eradication
{numbered(runbook.get('eradication_steps', []))}

## Phase 4 -- Recovery
{numbered(runbook.get('recovery_steps', []))}

## HIPAA-Specific Actions
{checklist(runbook.get('hipaa_actions', []))}

---

## Post-Incident Review
{numbered(runbook.get('lessons_learned_template', []))}

---
*Generated by ir-runbook-bot | GPT-4o + MITRE ATT&CK framework*
"""


SAMPLE_ALERTS = [
    "Outbound connection to known C2 IP 45.33.32.156:4444 from host web01. Connection sustained 14 min. 2.1GB transferred.",
    "47 failed SSH login attempts to root@10.0.0.15, followed by 1 successful login from the same IP.",
    "Ransomware note found on shared drive //ehr-server/PHI/. Multiple .encrypted files detected. EHR system unresponsive.",
]


def main():
    parser = argparse.ArgumentParser(description="IR Runbook Bot")
    parser.add_argument("--alert",  default=None)
    parser.add_argument("--output", default="runbook.md")
    args = parser.parse_args()

    alert = args.alert or SAMPLE_ALERTS[2]
    print(f"\nIR Runbook Bot\n{'='*60}")
    print(f"Alert: {alert[:100]}...\n")

    classification = classify_alert(alert)
    runbook_steps  = generate_runbook_steps(alert, classification)
    md = build_markdown(alert, classification, runbook_steps)

    print("  [3/3] Writing output...")
    with open(args.output, "w") as f:
        f.write(md)
    print(f"  Markdown -> {args.output}")

    json_out = args.output.replace(".md", ".json")
    with open(json_out, "w") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat(),
                   "alert": alert, "classification": classification,
                   "runbook": runbook_steps}, f, indent=2)
    print(f"  JSON     -> {json_out}")

    print(f"\nSeverity : {classification.get('severity')}")
    print(f"Tactic   : {classification.get('mitre_tactic')}")
    print(f"PHI Risk : {classification.get('hipaa_phi_risk')}")
    if classification.get("hipaa_breach_notification_required"):
        print("\n>>> HIPAA BREACH NOTIFICATION MAY BE REQUIRED <<<")
        print(">>> Review HIPAA actions section of the runbook <<<")


if __name__ == "__main__":
    main()
