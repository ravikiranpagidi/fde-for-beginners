# From field observation to reusable capability

A finished implementation solves a bounded delivery problem. Productization asks which observed need repeats, where a stable boundary exists, and whether someone should own it beyond this engagement. A one-customer feature is not automatically a product capability.

## The evidence ladder

| Step | Question | Artifact or stop condition |
| --- | --- | --- |
| Field observation | What happened to a real workflow in the exercise? | Trace, operator report, failed case, or measured manual step |
| Repeated need | Did Northstar and Atlas encounter the same need under comparable conditions? | Two concrete examples; label similarities that are only superficial |
| Pattern | Which inputs, outputs, invariants, and failures repeat? | Small contract plus counterexample |
| Abstraction boundary | What can be shared without hiding authority or customer rules? | Shared core versus configuration versus customer adapter |
| Reusable primitive | Can a small tested component solve the repeated problem? | API, compatibility expectations, tests, owner, and migration plan |
| Platform candidate | Do multiple teams need shared operation, governance, or scale? | Adoption evidence, service responsibility, isolation, support cost |
| Product decision | Is there a recurring user/buyer problem worth sustained investment? | Value hypothesis, demand evidence, alternatives, maintenance cost, go/no-go owner |

Do not skip directly from an incident to a platform. A shared library may be enough. A template can capture judgment that should not be automated. Repeated nouns such as "policy" or "approval" do not prove identical semantics.

## Exercise: Atlas and Northstar

Complete after [Atlas handoff](../../simulation/atlas-logistics/05-handoff.md), before its reference. This is the single Phase 3 productization exercise. Preserve evidence from both engagements and choose four to six findings of your own.

For each finding, answer: what was unique to Atlas, what repeated from Northstar, what evidence establishes repetition, what should be reusable code, what belongs in a template, what requires platform operation, and what should stay customer-specific? Explain whether a product candidate has actual demand evidence or merely a hypothesis.

The learner table is intentionally blank:

| Finding and evidence | Customer-specific | Reusable library | Template | Platform candidate | Product candidate | Owner, counterexample, and next evidence |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

Classifications may span columns, but explain each boundary. Then write a one-page proposal for **one** candidate:

1. Two observed examples, affected users, and the cost of leaving the implementations separate.
2. Smallest shared contract: inputs, outputs, invariants, failures, and customer-owned configuration.
3. A case that must remain outside that contract and why.
4. Migration plan for existing consumers, compatibility policy, maintenance owner, and rollback.
5. Validation plan using both engagements, including denial and degraded behavior.
6. Adoption/value measure, ongoing support cost, next evidence to collect, and a stop/revisit decision.

Explicitly reject one premature abstraction. "We might need it later" is not evidence. A proposal can conclude that a customer adapter or template is the correct outcome.

## Premature generalization risks

A universal API can hide different authorization rules. A configuration system can become a programming language without tests or ownership. A shared retry default can violate a customer's rate budget. A platform can make every team depend on an operator nobody funded. Keep the shared contract small, expose unresolved differences, and require evidence before centralizing operations.

Evaluate maintenance cost and failure semantics, not just removed lines of code. A reusable module with no owner or compatibility plan transfers work rather than eliminating it. Keep customer-specific labels, source authority, and rollout thresholds visible.

## Project and FDE optimization targets

A project delivery view optimizes for completing an agreed implementation within scope, time, and cost. An FDE view follows the workflow outcome through integration, evaluation, operation, and recurring capability discovery. Both need good engineering; neither is morally superior. Their success boundaries differ. A contract may deliberately stop at delivery, while an FDE engagement may need to renegotiate scope when evidence invalidates the requested implementation.

Your proposal should therefore identify who owns the ongoing outcome and who decides whether the pattern belongs in a product. Record evidence and gaps in the [field-readiness rubric](../learning-paths/field-readiness-rubric.md), rather than treating code reuse as sufficient proof.
