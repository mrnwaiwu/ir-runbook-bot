# Incident Triage Quick Reference

A fast lookup for first responders using ir-runbook-bot during an active incident.

## Severity at a glance

| Severity | Definition | First action |
|----------|-----------|--------------|
| SEV-1 | Customer-facing outage or data exposure | Page on-call lead, open bridge |
| SEV-2 | Major degradation, no full outage | Notify on-call, start runbook |
| SEV-3 | Minor issue, limited blast radius | Create ticket, handle in hours |

## First 10 minutes

1. Acknowledge the alert so others know it is owned.
2. Ask the bot for the matching runbook: `!runbook <alert-name>`.
3. Confirm scope: who and what is affected.
4. Post a short status in the incident channel.
5. Start a timeline so every action is logged.

## Useful bot commands

- `!runbook <name>` — pull the steps for a known scenario
- `!oncall` — show who is currently on call
- `!timeline` — dump the current incident timeline
- `!status <message>` — post a stakeholder update

## After the incident

Capture a short summary, link the timeline, and schedule a blameless review within 48 hours.
