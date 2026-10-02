# Progress tracker

Copy this page into your personal notes. Record evidence and feedback, not just reading completion. Use `not started`, `attempted`, `reviewed`, or `needs revision`. A review should identify at least one limitation, not merely say "looks good."

| Milestone | Evidence to preserve | Status | Reviewer and next action |
| --- | --- | --- | --- |
| Role and workflow | Response to Northstar's request and delivery loop | Not started | Assign a reviewer |
| Discovery | Observations, questions, workflow, decision owners, unknowns | Not started | Test the riskiest assumption |
| Success criteria | Problem statement, baseline plan, metric denominators, stop conditions | Not started | Confirm acceptance owner |
| Design | Boundaries, contracts, alternatives, exclusions, failure table | Not started | Challenge an integration assumption |
| Readiness | Evidence locations, launch blockers, rollback and support owners | Not started | Rehearse an incident response |
| Local contribution setup | Actual lint, test, and docs-build output | Not started | Resolve setup failures |

## Phase 2 engineering evidence

- [ ] Reliable API integration passes failure-mode tests.
- [ ] Idempotency and conflicting-payload tests pass.
- [ ] RAG evaluation report produced and denominators explained.
- [ ] One retrieval failure analyzed without changing the expected label.
- [ ] MCP unapproved and invalidly approved writes rejected.
- [ ] MCP explicitly approved write succeeds; replay fails.
- [ ] One [ADR](../../templates/architecture-decision-record.md) completed.
- [ ] One [readiness checklist](../../templates/production-readiness-checklist.md) completed with limitations.

The integrated Northstar project and Atlas engagement/incident artifacts remain deferred to Phase 3. This tracker does not certify production experience.

## Record one decision

For each milestone, capture the date, problem, constraints, decision, evidence, outcome, and lesson. Mark assumptions explicitly. Include what you chose not to build and the trigger for revisiting that choice. Keep customer and employer information out of public portfolio material.

Example: "I proposed cached order data, then learned freshness is required for eligibility. I changed the first slice to direct reads with an unavailable state. Upstream latency remains unverified." This demonstrates learning even before code exists.

## Peer review exercise

Give a reviewer your problem statement and design without narrating them. Ask them to identify the user, authoritative system, stop condition, operator, and largest uncertainty. Record what they misunderstood and revise the artifacts. Retain both versions so your portfolio shows how evidence changed the design.

## Checkpoint 1 self-review

- [ ] I can explain the workflow without naming a framework.
- [ ] I separated observed facts from assumptions and assigned unknowns.
- [ ] My metrics distinguish technical quality, workflow value, adoption, and business outcomes.
- [ ] My design includes denied access, unavailable data, and uncertain write outcomes.
- [ ] My readiness review has real blockers rather than automatically checked boxes.
- [ ] I can explain one issue to an engineer, manager, and business stakeholder.
- [ ] I have identified one customer-specific rule and one candidate reusable pattern.

Choose the next step using [choose your path](choose-your-path.md). The release sequence and approval gates are in [ROADMAP](../../ROADMAP.md).
