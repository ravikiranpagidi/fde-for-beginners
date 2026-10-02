# Start here

Begin with a workflow, not a stack. At fictional Northstar Retail Support, representatives switch between customer records, orders, policies, and tickets to answer a return question. A manager asks for an AI agent. Your first job is to discover which step is slow, error-prone, or unsupported by evidence.

## Your first session

1. Read [What is FDE?](docs/foundations/what-is-fde.md) and select a [learning path](docs/learning-paths/choose-your-path.md).
2. Attempt the [discovery exercise](docs/field/customer-discovery.md). Write questions before reading its review guidance.
3. Produce a one-paragraph [problem statement](docs/field/problem-framing.md), including a measurable outcome and a non-goal.
4. Save your evidence in a personal copy of the [progress tracker](docs/learning-paths/progress-tracker.md). Keep assumptions separate from observations.

You can do these exercises without installing Python. Phase 1 ends with a design and readiness review; the three labs are planned for Phase 2. The integrated project and simulation follow in Phase 3. There is no lab command to run yet.

## Install the development environment

Requirements: Git, Python 3.11 or newer, and internet access for the initial dependency installation. Python 3.11 and 3.13 are the CI targets. From a checkout of this repository:

```sh
python -m pip install uv
python -m uv sync --locked --extra dev
python -m uv run --offline ruff check .
python -m uv run --offline pytest
python -m uv run --offline mkdocs build --strict
```

Using `python -m uv` works even if the uv executable is not on PATH. `uv` is equivalent when it is on PATH. The lockfile fixes dependency versions; do not regenerate it just to install. Setup downloads packages, but these checks do not need external services once installation is complete. No `.env` file is needed in Phase 1.

Expected results: Ruff reports success, pytest exits with zero failures, and MkDocs writes `site/` without warnings. The tests validate documentation integrity and package installation, not the future labs or production readiness.

For a pip-compatible alternative, create and activate a virtual environment, then run `python -m pip install -e ".[dev]"`. This resolves versions from project constraints rather than `uv.lock`; use uv for the exact CI environment.

## Read locally

```sh
python -m uv run --offline mkdocs serve
```

Open the local address printed by MkDocs. Stop with Ctrl+C. Search and code highlighting are configured. Mermaid diagrams also have adjacent prose; the theme may load its diagram renderer from a CDN, so browser rendering can require internet access. Markdown remains readable directly on GitHub.

## If setup fails

| Symptom | Check and next action |
| --- | --- |
| Python not found | Install Python 3.11+ and reopen the terminal; on Windows check `py -3 --version` |
| Dependency download fails | Check proxy and package-index access; do not paste credentials into an issue |
| Lockfile mismatch | Confirm the checkout is complete; contributors changing dependencies must update the lock |
| Module not found | Run from the repository root and repeat `uv sync --locked --extra dev` |
| Documentation link failure | Fix the source link; do not disable strict mode |

When reporting a problem, include OS, Python version, exact command, and sanitized error text. Continue with the Markdown exercises while resolving installation.

## Exit evidence

Before moving beyond the foundation, have a workflow map, problem statement, scoped design, and production review with open blockers. Ask a peer to challenge one assumption. Record what changed. A completed reading list alone is not evidence of field readiness.
