# Start here

Begin with a workflow, not a stack. At fictional Northstar Retail Support, representatives switch between customer records, orders, policies, and tickets to answer a return question. A manager asks for an AI agent. Your first job is to discover which step is slow, error-prone, or unsupported by evidence.

## Your first session

1. Read [What is FDE?](docs/foundations/what-is-fde.md) and select a [learning path](docs/learning-paths/choose-your-path.md).
2. Attempt the [discovery exercise](docs/field/customer-discovery.md). Write questions before reading its review guidance.
3. Produce a one-paragraph [problem statement](docs/field/problem-framing.md), including a measurable outcome and a non-goal.
4. Save your evidence in a personal copy of the [progress tracker](docs/learning-paths/progress-tracker.md). Keep assumptions separate from observations.

You can do the foundation exercises without installing Python. Then follow [Reliable Integration](labs/01-reliable-api-integration/README.md) -> [RAG and Evaluation](labs/02-rag-and-evaluation/README.md) -> [Safe MCP Tools](labs/03-mcp-safe-tools/README.md). Experienced learners may jump directly to a lab after setup. The integrated project and simulation remain deferred to Phase 3.

## Install the development environment

Requirements: Git, Python 3.11 or newer, and internet access for the initial dependency installation. Python 3.11 and 3.13 are the CI targets. From a checkout of this repository:

```sh
python -m pip install uv
python -m uv sync --locked --extra dev
python -m uv run --offline ruff check .
python -m uv run --offline pytest
python -m uv run --offline mkdocs build --strict
```

Using `python -m uv` works even if the uv executable is not on PATH. `uv` is equivalent when it is on PATH. The lockfile fixes dependency versions; do not regenerate it just to install. Setup downloads packages, but checks and labs do not need external services once installation is complete. No `.env` file is needed. Provider selection reads the process environment, defaults to mock, and rejects unknown providers; `.env` files are not loaded automatically.

Expected results: Ruff reports success, pytest exits with zero failures, and MkDocs writes `site/` without build warnings. Tests validate documentation, providers, API failures, RAG behavior, and actual MCP protocol exchanges. They do not certify production readiness. The theme may print an upstream advisory about a future MkDocs major release; this project remains pinned below that release.

## Run the engineering core

From the repository root, start the API in one terminal:

```sh
uv run --offline uvicorn fde_beginners.integration.upstream:app --host 127.0.0.1 --port 8001
```

In another terminal:

```sh
uv run --offline fde-api --mode rate_limit
uv run --offline fde-api --reserve --mode duplicate_request --key first-reservation
uv run --offline fde-rag evaluate
uv run --offline fde-mcp-demo
```

The MCP demo displays a proposed synthetic ticket and waits for an explicit `APPROVE`. Read each lab's failure, reset, and expected-output sections. Local tests use loopback networking and stdio, never external services. The RAG baseline intentionally has imperfect retrieval; inspect failed cases instead of treating test success as answer-quality proof.

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
