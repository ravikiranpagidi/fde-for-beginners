# What is Forward Deployed Engineering?

A Forward Deployed Engineer works close to a customer to turn an ambiguous operational problem into a working, integrated system. The work crosses discovery, implementation, evaluation, deployment, operation, and handoff. The exact job title and division of responsibility vary by employer; this curriculum teaches a delivery pattern, not a universal job description.

An FDE needs enough software, data, API, cloud, reliability, and security knowledge to reason across system boundaries. Applied AI can help with language or uncertain inputs. It does not remove the need to understand a workflow or enforce a business rule.

## A request is not a problem statement

Northstar Retail Support says: "Build an agent that handles returns."

Three plausible problems hide inside that request:

| Possible problem | Evidence to seek | Smallest plausible intervention |
| --- | --- | --- |
| Representatives cannot find the current policy | Observe policy searches and version confusion | Search with dates and sources |
| Order facts must be copied between systems | Trace fields and duplicate entry | Deterministic integration |
| Exceptions need judgment from a supervisor | Review escalations and decision authority | A prepared case summary for human review |

Building an autonomous refund agent before distinguishing these problems risks automating the wrong work. The engineer must still implement something useful: discovery is not an excuse to avoid delivery.

## Working across roles

Product engineers often optimize a capability used across customers. An FDE often starts from one customer's outcome and assembles or extends several capabilities. Solutions architects may emphasize design; support engineers may emphasize recovery; consultants may emphasize advice. In practice these responsibilities overlap. Agree on ownership instead of relying on job titles.

For Northstar, write down who owns policy interpretation, who can authorize a refund, who operates the integration, and who accepts the pilot. These may be four different people. The FDE should make the gaps visible rather than silently becoming the permanent owner of everything.

The company-specific examples in [References](../references.md) inform this framing. They do not establish a standard interview process or prove that every FDE role includes AI.

## FDE Decision

Should the first intervention use a model? Prefer deterministic code for known identifiers, arithmetic, access checks, and policy rules with explicit inputs. Consider a model for drafting or interpreting unstructured text when the workflow can tolerate uncertainty, evaluate mistakes, and retain human control. If the real blocker is missing access to order data, a model does not solve it.

## Exercise: choose what to investigate

Write a one-page response to Northstar's request:

1. List three competing explanations for the delay and one observation that could disprove each.
2. Identify a user, decision owner, data owner, and operator you need to involve.
3. Propose a reversible first step and a condition under which you would stop it.
4. Explain why you have not yet promised automatic refunds.

Review your answer: if every explanation leads to the same framework, you probably selected a solution too early. Strong evidence includes an observed handoff or error, not just agreement from a sponsor. Preserve this response as the opening page of your portfolio engagement record.

## Production Reality

A demo can use one clean record and a cooperative upstream service. Production includes stale policies, expired credentials, missing fields, and users with different permissions. Field engineering includes deciding what fails safely and who gets notified, not just making the successful path attractive.

## Productize what repeats

One-off fix -> repeated pattern -> reusable primitive -> platform capability -> product feature.

Northstar's policy wording is customer-specific. A tested retry policy or approval boundary may be reusable. Keep customer rules in configuration or adapters when justified, collect evidence from another engagement before generalizing, and give a shared component an owner. Permanent forks without ownership create maintenance obligations, not product progress.

Next: use the [lifecycle](fde-lifecycle.md) to organize the evidence you need.
