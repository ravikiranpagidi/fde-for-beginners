# Problem framing and success criteria

A useful problem statement identifies a user, workflow, observed obstacle, consequence, and testable outcome. It also states what you do not know. "Build a chatbot" specifies an interface without explaining the problem.

## Frame Northstar's first slice

Example, based on the fictional discovery exercise:

> Northstar support representatives need to locate the applicable return policy while reviewing an order. They report switching between systems and uncertainty about policy versions. We will test whether a read-only view with order facts and cited policy passages reduces lookup work without increasing incorrect advice. Baseline time and error rate are not yet measured. Automatic refunds and exception adjudication are out of scope.

This statement is intentionally narrower than the sponsor's request. Confirm it with representatives, the sponsor, and the policy owner. Record any disagreement and the evidence needed to resolve it.

## Keep metric families separate

The following targets are **synthetic exercise proposals**, not industry standards or measured results. Learners must negotiate thresholds before seeing evaluation output.

| Family | Measure and denominator | Proposed exercise criterion | Reviewer |
| --- | --- | --- | --- |
| Technical | Successful eligible requests / all eligible requests; p95 response latency | At least 98% success and p95 under 3 seconds in the declared test workload | Integration owner |
| Retrieval/model quality | Relevant policies retrieved / expected relevant policies; supported drafts / all drafts | Every mandatory safety case abstains or cites correct current evidence | Policy reviewer |
| Workflow | Median active lookup time per matched eligible case | At least 20% lower than measured manual baseline, with no rise in rework | Support lead |
| Adoption | Representatives using the view / representatives eligible and offered training | Review weekly usage and documented bypass reasons during the pilot | Team lead |
| Business | Completed cases per staffed hour, alongside repeat-contact and complaint rates | Agree a continuation threshold after baseline collection, before pilot rollout | Sponsor |

A faster response is not automatically a better workflow. Repeatedly polling a fast tool may still take longer than manual lookup. High usage may reflect mandatory policy rather than user trust. Record those interpretation limits with the metric.

## Design the measurement before the solution

Define eligible cases, excluded cases, start/stop timestamps, error categories, and the source of truth. Compare like with like: ordinary returns against ordinary returns, not simple prototype examples against difficult manual cases. Record the sample size and distribution; a small pilot cannot establish rare-event safety.

For a paired synthetic exercise, replay the same cases manually and through the proposed view, vary the order to reduce practice effects, and record both active time and waiting time. Capture wrong advice and missing information, including abstentions. Save raw sanitized observations and the calculation, not just a percentage improvement.

Do not assign a dollar value to time saved without an agreed cost model. If no baseline exists, the first deliverable is instrumentation or observation. Claiming a benefit before measuring the baseline makes later evaluation difficult to trust.

## Guardrails and stop conditions

Northstar's pilot should stop on cross-region data exposure or an unauthorized write. Incorrect or stale policy citations require review and may narrow the allowed case set. A transient upstream outage should be visible as unavailable data, not silently transformed into "no order found."

Record for each guardrail: detecting signal, threshold, decision owner, immediate containment, and restart evidence. A guardrail that nobody can observe cannot protect a rollout.

## Exercise: challenge a metric

The sponsor proposes "90% of tickets resolved by AI." Identify how that metric could reward unsafe closure, exclude hard cases, or hide repeat contacts. Replace it with one primary workflow metric and two guardrails. Specify denominators, collection method, reviewer, and a decision date.

Preserve a one-page success agreement with assumptions and exclusions. Review it by asking: could a system pass these criteria while making the customer worse off? If yes, revise the criteria. Then explain the same risk in three short messages: an engineer needs failure semantics; a manager needs scope and staffing impact; an executive needs outcome uncertainty and the decision required.

## FDE Decision

Build, integrate, or stop? Prefer an existing capability if it meets the workflow and constraints at acceptable operational cost. Build only the missing slice. Stop or reframe when data access, ownership, or expected value cannot justify the integration burden. A written no-build recommendation supported by evidence is valid field work.

Next: carry the agreement into [solution design](solution-design.md).
