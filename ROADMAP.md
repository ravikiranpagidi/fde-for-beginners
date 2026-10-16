# Roadmap

This is a release plan, not a claim that planned material exists. New topics must improve a specific learner outcome and fit the content budget.

## v0.1: Field foundations and local delivery

### Phase 1: Foundation (complete)

Six core guides, three navigation guides, references, root policies, Python packaging, locked dependencies, Ruff, pytest, CI, and MkDocs. Merged after local and GitHub CI validation.

### Phase 2: Three labs and eight field templates (complete)

Exactly three labs: Reliable API Integration, RAG and Evaluation, and MCP and Safe Tool Execution. One shared LLM provider protocol and deterministic mock serve the AI workflow. The MCP lab uses the verified official stable v2 SDK. Approval denial and success are tested over the actual protocol.

Exactly eight templates: discovery questionnaire; problem statement and success metrics; technical design; architecture decision record; evaluation plan; production readiness checklist; rollout and handoff; postmortem.

A lab is labeled Runnable only when it works without keys, paid services, or runtime network calls after dependency installation; meaningful success and failure tests pass in CI; setup and expected behavior are validated; and any real-provider path is separate. Approval for writes must be enforced in code and tested.

### Phase 3: Integrated delivery (checkpoint 3)

One [Northstar Support Copilot](project/northstar-support-copilot/README.md) project reuses the lab components for customer and order lookup, policy retrieval, cited response drafts, approved ticket creation, logs, evaluation, and degraded behavior.

One [Atlas Logistics engagement](simulation/atlas-logistics/README.md) simulation begins with incomplete information, requires discovery and delivery artifacts, then reveals a production incident. Its reference solution and incident analysis are separate from learner tasks. Finish with the evidence rubric, handoff, and productization exercise. Stop here for review; no v0.2 implementation is included.

### Release gate

- Follow README -> Start Here -> path -> first lab -> project -> simulation without broken links.
- Demonstrate all three labs locally and in CI, including denial of unapproved writes.
- Produce reproducible retrieval evaluation and controlled failure evidence.
- Complete synthetic-data and secret checks; preserve the MIT license.
- Keep the content compact, with no future placeholder folders; separate staged disclosures rather than exposing answers inline.
- Report validation limits honestly; a local docs build is not a Pages deployment.

## v0.2: Production systems

Candidates: OAuth/OIDC, deeper authorization, secrets management, centralized observability, durable workflows, distributed failures, deployment strategies, and one carefully scoped cloud deployment. Select a provider only when a customer constraint motivates it. AWS, Azure, and Google Cloud comparisons belong here, not in v0.1 certification courses.

## v0.3: Agentic systems

Candidates: deterministic versus agentic execution, state machines, long-running jobs, context management, agent evaluation, security, and multi-agent tradeoffs. Framework examples must follow concepts and show when simpler code is preferable.

## v0.4: Enterprise integration

Candidates: event streaming, legacy systems, databases, identity, private networking, and enterprise data access. Deeper software, data engineering, cloud, and infrastructure foundations can support these exercises instead of becoming disconnected curricula.

## v0.5: Field simulations

Candidates: manufacturing, healthcare, financial services, logistics, SaaS, and public-sector scenarios, each with synthetic data and explicit domain limits. Additional capstones, portfolio guidance, and interview preparation require a separate scope review.

## Proposing future work

Describe the customer problem, learner decision, failure scenario, and evidence produced. Explain why an existing guide or lab cannot teach it. No job board, employer ranking, salary guide, or framework catalog is planned.
