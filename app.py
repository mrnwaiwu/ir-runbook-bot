"""
ir-runbook-bot -- Flask REST API
---------------------------------
Exposes /api/runbook for SIEM/SOAR integration.
Optionally posts severity summary to Slack.

Run:  python app.py
Test:
  curl -X POST http://localhost:5000/api/runbook \
    -H 'Content-Type: application/json' \
    -d '{"alert": "Ransomware detected on EHR server"}'
"""

import os
from flask import Flask, request, jsonify
from runbook import classify_alert, generate_runbook_steps, build_markdown

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ir-runbook-bot"})


@app.route("/api/runbook", methods=["POST"])
def create_runbook():
    data = request.get_json()
    if not data or "alert" not in data:
        return jsonify({"error": "Missing 'alert' field."}), 400
    if len(data["alert"]) < 10:
        return jsonify({"error": "Alert text too short."}), 400

    alert = data["alert"]
    try:
        classification = classify_alert(alert)
        runbook_steps  = generate_runbook_steps(alert, classification)
        markdown       = build_markdown(alert, classification, runbook_steps)

        # Optional Slack notification
        slack = os.getenv("SLACK_WEBHOOK_URL")
        if slack:
            import requests as req
            sev = classification.get("severity", "UNKNOWN")
            emoji = {"CRITICAL": ":rotating_light:", "HIGH": ":warning:",
                     "MEDIUM": ":large_yellow_circle:", "LOW": ":information_source:"}.get(sev, ":bell:")
            req.post(slack, json={"text": (
                f"{emoji} *{sev} Incident: {classification.get('incident_type')}*\n"
                f"Tactic: {classification.get('mitre_tactic')} | "
                f"PHI Risk: {classification.get('hipaa_phi_risk')}\n"
                f"> {alert[:200]}"
            )})

        return jsonify({
            "classification": classification,
            "runbook":        runbook_steps,
            "markdown":       markdown,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
