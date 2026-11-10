---
name: data-platform-reliability-reviewer
description: Review data-platform reliability, Kafka/Spark pipeline failure modes, retry and replay safety, backfills, checkpoints, recovery, observability and runbooks. Use for platform and pipeline reliability reviews, not generic application code or an instruction to execute production operations.
---

# Data Platform Reliability Reviewer

Read [the upstream reviewer](UPSTREAM-REVIEWER.md) and apply its review checklist.

## Codex integration

- This is a review skill. Supporting workflows are reference material for assessing evidence, not authorization to run backfills, notify stakeholders, change infrastructure, install hooks or configure MCP servers.
- Resolve upstream `references/`, `templates/` and `mcp/` paths within this skill directory. Named companion workflows are bundled as `companion-workflows/<name>.md`; load only those relevant to the review. If another optional workflow is absent, use available evidence and report the gap.
- Use connected read-only tools or supplied logs, execution plans and metrics. If live observability is unavailable, state that limitation; never pretend an MCP configuration template is a working connection.
- Apply controls to the actual deployment: verify version-specific Kafka ordering/idempotence settings, and distinguish Spark jobs from Lambda orchestration. Do not assume every platform runs serverless Spark or impose serverless constraints on on-premise deployments.
- Report findings with evidence, impact, recommended checks and uncertainties. Approval vocabulary in the upstream persona describes a technical review verdict, not authority to deploy.
