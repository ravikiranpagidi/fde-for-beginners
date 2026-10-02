# Contributing

Improve what a learner can decide, implement, or verify. Start by identifying a concrete problem with an existing exercise. Use synthetic Northstar Retail Support examples; Atlas Logistics is reserved for the future simulation.

## Local workflow

Follow [setup](START_HERE.md), create a focused branch, and make the smallest coherent change. Run from the repository root:

```sh
python -m uv sync --locked --extra dev
python -m uv run --offline ruff check .
python -m uv run --offline ruff format --check .
python -m uv run --offline pytest
python -m uv run --offline mkdocs build --strict
```

For dependency changes, edit `pyproject.toml`, run `python -m uv lock`, review the lockfile diff, and repeat the checks. Do not hand-edit package hashes. Keep optional provider integrations separate from default offline behavior.

## Review standard

Explain the learner problem and resulting behavior in the PR. Include actual validation results and untested paths. Substantial guides need a scenario, exercise, decision, failure mode, or reusable artifact. A lab needs documented expected output and meaningful failure tests before it can be called Runnable.

Use relative Markdown links and fenced code. Avoid en dashes and em dashes in authored prose. Cite first-party sources with access dates for external claims. Do not add unsupported employment statistics or imply that fictional exercise results were observed in production.

Phase 1 does not implement labs or templates. Later v0.1 work is capped at three labs, eight field templates, one project, and one simulation. Put unrelated ideas in [ROADMAP](ROADMAP.md). Preserve the MIT license and do not contribute confidential material.

## Documentation architecture

Root pages and `docs/` are canonical Markdown. The small `scripts/docs_hook.py` MkDocs hook publishes those same files at repository-relative paths, so GitHub and site links agree. There is no second copy to edit. Add pages to `mkdocs.yml` navigation. Strict builds check links and anchors; pytest guards source links and authored punctuation without relying on external link availability.

## Repository configuration recommendations

These are maintainer actions, not settings automatically applied by this branch:

- Description: "Learn Forward Deployed Engineering through customer discovery, reliable integrations, evaluation, and production delivery."
- Topics: `forward-deployed-engineering`, `fde`, `software-engineering`, `api-integration`, `learning`, `python`. Add `rag` and `mcp` when those labs exist.
- Require PR review and passing `validate (3.11)` and `validate (3.13)` CI jobs on the default branch. Verify GitHub's displayed check names before configuring protection.
- Enable private vulnerability reporting in repository security settings and dependency alerts. Schedule lockfile review; introduce automated dependency updates when a maintainer can review them.
- For Pages, first validate `mkdocs build --strict`. When ready to publish, run `uv run mkdocs gh-deploy` from the intended default branch and configure Pages to serve the `gh-pages` branch. This is an optional publishing action, not part of local validation.

Never publish credentials, customer records, or private incident details in issues or PRs. Follow [SECURITY](SECURITY.md) for sensitive reports and the [code of conduct](CODE_OF_CONDUCT.md) for participation.
