# Escalation Procedures

This document outlines the escalation paths used by the IR Runbook Bot when automated triage determines that human intervention is required.

## Severity Levels

| Level | Label       | Response SLA | Escalation Target          |
|-------|-------------|--------------|----------------------------|
| P0    | Critical    | 15 minutes   | On-call lead + CISO        |
| P1    | High        | 1 hour       | On-call lead               |
| P2    | Medium      | 4 hours      | Security operations team   |
| P3    | Low         | 24 hours     | Security analyst queue     |

## Escalation Triggers

The bot automatically escalates to human review under these conditions:

- **Confidence score < 0.70** — runbook match is ambiguous; human judgment required
- **Novel indicator pattern** — no matching runbook found for the detected IOC type
- **Multi-system blast radius** — incident affects more than 3 distinct systems
- **Privileged account involved** — any alert touching admin, root, or service accounts
- **Regulatory scope** — affected data classified as PII, PHI, or PCI in the asset inventory

## Escalation Channels

### PagerDuty (P0 / P1)
The bot calls the PagerDuty Events API (`/v2/enqueue`) with:
- `routing_key`: configured per environment in `config.yaml`
- `payload.severity`: mapped from internal P-level
- `payload.summary`: first 255 chars of the triage summary
- `links`: direct link to the incident record

### Slack (P1 / P2)
Posts to `#security-incidents` with:
- Incident ID and severity badge
- Affected systems list
- Recommended runbook (if confidence ≥ 0.50)
- Link to full triage report

### Email (P2 / P3)
Sends digest to the security alias with:
- Incident summary table
- Assigned analyst (round-robin from on-call roster)
- 24-hour resolution deadline reminder

## Override Behavior

Any team member can manually override the escalation level via the `/escalate` slash command:

```
/escalate <incident-id> p0 "Reason for upgrade"
```

Overrides are logged with the caller's identity and timestamp for audit trail purposes.

## Runbook Integration

When escalating, the bot attaches the highest-confidence runbook as context:

```json
{
  "runbook_id": "RB-0042",
  "title": "Credential Stuffing Response",
  "confidence": 0.85,
  "steps_completed": 3,
  "steps_remaining": 7
}
```

This gives the responder immediate context without needing to re-triage from scratch.

---

*Last updated: 2026-06-27*
