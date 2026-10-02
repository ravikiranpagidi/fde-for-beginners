# Roadmap

This is a release plan, not a claim that planned material exists. New topics must improve a specific learner outcome and fit the content budget.

## v0.1: Field foundations and local delivery

### Phase 1: Foundation (complete)

Six core guides, three navigation guides, references, root policies, Python packaging, locked dependencies, Ruff, pytest, CI, and MkDocs. Merged after local and GitHub CI validation.

### Phase 2: Three labs and eight field templates (current checkpoint)

Exactly three labs: Reliable API Integration, RAG and Evaluation, and MCP and Safe Tool Execution. One shared LLM provider protocol and deterministic mock serve the AI workflow. The MCP lab uses the verified official stable v2 SDK. Approval denial and success are tested over the actual protocol.

Exactly eight templates: discovery questionnaire; problem statement and success metrics; technical design; architecture decision record; evaluation plan; production readiness checklist; rollout and handoff; postmortem.

A lab is labeled Runnable only when it works without keys, paid services, or runtime network calls after dependency installation; meaningful success and failure tests pass in CI; setup and expected behavior are validated; and any real-provider path is separate. Approval for writes must be enforced in code and tested.

### Phase 3: Integrated delivery (not implemented)

One Northstar Support Copilot project will reuse the lab components for customer and order lookup, policy retrieval, cited response drafts, approved ticket creation, logs, evaluation, and degraded behavior.

One Atlas Logistics engagement simulation will begin with incomplete information, require discovery and delivery artifacts, then reveal a production incident. Its reference solution and incident analysis will be separate from the initial learner task. Finish with final navigation and verification.

### Release gate

- Follow README -> Start Here -> path -> first lab -> project -> simulation without broken links.
- Demonstrate all three labs locally and in CI, including denial of unapproved writes.
- Produce reproducible retrieval evaluation and controlled failure evidence.
- Complete synthetic-data and secret checks; preserve the MIT license.
- Keep roughly 25 to 35 substantive Markdown documents, with no future placeholder folders.
- Report validation limits honestly; a local docs build is not a Pages deployment.

## v0.2: Production systems

Candidates: OAuth, secrets management, deeper observability, distributed failures, deployment strategies, and one carefully scoped cloud deployment. Select a provider only when a customer constraint motivates it. AWS, Azure, and Google Cloud comparisons belong here, not in v0.1 certification courses.

## v0.3: Agentic systems

Candidates: deterministic versus agentic execution, state, long-running jobs, agent evaluation, security, and multi-agent tradeoffs. Framework examples must follow concepts and show when simpler code is preferable.

## v0.4: Enterprise integration

Candidates: event streaming, legacy systems, databases, identity, private networking, and enterprise data access. Deeper software, data engineering, cloud, and infrastructure foundations can support these exercises instead of becoming disconnected curricula.

## v0.5: Field simulations

Candidates: manufacturing, healthcare, financial services, logistics, SaaS, and public-sector scenarios, each with synthetic data and explicit domain limits. Additional capstones, portfolio guidance, and interview preparation require a separate scope review.

## Proposing future work

Describe the customer problem, learner decision, failure scenario, and evidence produced. Explain why an existing guide or lab cannot teach it. No job board, employer ranking, salary guide, or framework catalog is planned.
