# Changelog

## [Unreleased]
- Planned: Slack integration for runbook notifications
- Planned: automated playbook triggering via webhook

## [1.2.4] - 2026-07-13
- Added support for runbook approval gates requiring operator sign-off before critical steps execute
- Improved incident deduplication logic to suppress redundant triggers within a configurable window
- Minor refactor of the runbook loader to support hot-reload without service restart

## [1.2.3] - 2026-07-06
- Added support for runbook execution audit trail to capture step-level timing and operator identity
- Improved incident severity auto-classification using keyword-weighted scoring across alert fields
- Fixed edge case where nested runbook step dependencies caused incorrect execution ordering
- Added configurable cooldown period between repeated runbook triggers for the same incident class

## [1.2.2] - 2026-06-27
- Added support for runbook tagging to enable category-based filtering and discovery
- Improved execution context passing between runbook steps for stateful workflows
- Added validation schema for runbook YAML to catch misconfiguration at load time
- Minor performance improvements to the runbook lookup index

## [1.2.1] - 2026-06-20
- Added timeout handling for long-running runbook steps to prevent stalled executions
- Improved runbook step retry logic with configurable backoff intervals
- Added metrics emission for runbook execution duration per step

## [1.2.0] - 2026-06-06
- Added structured JSON logging for runbook execution steps
- Improved error handling in multi-step runbook sequences
- Added support for conditional branching in runbook flows
- Introduced runbook versioning to track playbook revisions

## [1.1.0] - 2026-06-03
- Added support for multi-step runbook execution
- Improved incident classification logic
- Added dry-run mode for runbook validation

## [1.0.0] - 2026-05-01
- Initial release
- Basic IR runbook bot scaffolding
- Runbook parsing and execution engine
