# FDE skills matrix

Use levels as descriptions of evidence, not numeric scores. **Foundation:** explain and inspect. **Working:** implement a bounded case. **Production:** validate failures and operation. **Field-ready:** negotiate constraints, deliver with others, and transfer ownership. A tutorial alone cannot establish field readiness; that requires reviewed practice in a realistic engagement.

Each row describes what grows across those four levels. "Planned" means the repository does not yet provide implementation practice for that area. The current guides supply judgment exercises, not a claim of complete technical coverage.

| Area | Foundation -> Working -> Production -> Field-ready | Repository practice and evidence |
| --- | --- | --- |
| Programming | Read functions -> implement explicit contracts -> test failure behavior -> maintain another person's integration | Setup and three labs available. Preserve tested source and debugging notes |
| APIs | Explain request/response -> validate a client -> bound retries and deadlines -> negotiate upstream contracts | Solution design and Lab 1 failure tests. Produce an error/contract table |
| Databases | Identify keys -> query/update safely -> reason about consistency and migrations -> negotiate data ownership | Design discussion only; deeper work deferred. Produce a source-of-truth map |
| Data engineering | Inspect schema -> transform records -> detect drift and freshness loss -> agree correction ownership | Discovery and design now. Produce a schema/freshness risk record |
| Cloud | Describe service boundaries -> configure a service -> manage access and recovery -> agree deployment constraints | Readiness planning now; cloud implementation deferred. Produce deployment assumptions |
| Containers | Explain isolation -> package a process -> handle config and shutdown -> hand off operations | Conceptual readiness only; practical coverage deferred. Record an environment contract |
| Distributed systems | Explain partial failure -> handle timeout -> reconcile uncertain outcomes -> negotiate consistency needs | Lab 1 retries, timeouts, and idempotency tests. Produce duplicate-write and outage cases |
| LLM applications | Explain uncertain output -> validate a draft -> evaluate failures/cost -> justify model use | Shared typed provider and deterministic mock available; project deferred. Preserve baseline and model-use decision |
| RAG | Explain retrieval/grounding -> retrieve cited evidence -> evaluate freshness/access -> agree acceptable unsupported cases | Lab 2 retrieval and reproducible evaluation. Define a case set and abstention rules |
| Agents | Distinguish flexible sequencing -> constrain tools -> bound actions and recovery -> justify autonomy | Design decision now; deeper agent work deferred. Produce a deterministic alternative |
| MCP | Explain protocol role -> expose a narrow capability -> enforce approval/errors -> agree client/server boundaries | Lab 3 protocol, approval, replay, and audit tests. Produce denial and success evidence |
| Evaluations | Define expected behavior -> run representative cases -> gate regressions -> negotiate launch evidence | Problem framing and executable Lab 2 evaluation. Preserve acceptance criteria |
| Security | Separate identity/permission -> validate access -> test denial and audit -> align with data owners | Lab 3 invalid, expired, changed, and reused approval tests. Produce an access matrix |
| Reliability | Identify failures -> implement fallback -> rehearse recovery -> agree service/support scope | Readiness plus Lab 1 controlled failure modes. Produce failure and recovery table |
| Observability | Distinguish logs/metrics/traces -> instrument a request -> diagnose across dependencies -> route actionable signals | Lab retry/retrieval events and tool audits; project instrumentation deferred. Design a redacted event |
| Customer discovery | Ask workflow questions -> map observed cases -> expose exception paths -> reconcile competing stakeholders | Discovery exercise now. Preserve observations, unknowns, and playback |
| Architecture | Draw dependencies -> compare options -> include failure/ownership -> revise under constraints | Solution design now. Preserve boundaries, alternatives, and revisit triggers |
| Product judgment | Identify user outcome -> scope useful slice -> measure adoption/value -> productize repeated needs | Framing/lifecycle now. Produce exclusions and a reuse proposal |
| Communication | Explain an issue -> adapt to audience -> communicate incidents -> secure shared decisions | Framing exercise now. Produce engineer, manager, and sponsor messages |
| Production delivery | Distinguish demo/pilot -> plan rollout -> verify rollback/support -> complete handoff | Readiness exercise now; project/simulation planned. Produce launch evidence and blockers |

## Exercise: assess with evidence

Select one technical row and one customer-facing row. Link an artifact and explain which level it supports, what remains untested, and what counterexample would invalidate your assessment. Have a peer inspect one claim. Do not promote yourself from Working to Production because a happy-path example passed.

Use the [progress tracker](progress-tracker.md) for the resulting next steps and the [path guide](choose-your-path.md) to choose exercises.

## Phase 2 evidence

[Lab 1](../../labs/01-reliable-api-integration/README.md) supports Working API competency and practice with production failure semantics. [Lab 2](../../labs/02-rag-and-evaluation/README.md) supports evaluation competency through an actual report and failure analysis. [Lab 3](../../labs/03-mcp-safe-tools/README.md) supports tool-approval competency through protocol-level denial, success, and replay tests. None alone establishes field readiness or production experience.
