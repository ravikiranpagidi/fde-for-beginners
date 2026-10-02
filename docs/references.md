# References and source boundaries

These first-party sources support the curriculum's framing and tooling. Access date: **2026-10-01**. External pages can change; no automated external-link check is required for local tests. Exercise companies, numbers, and decisions are synthetic.

## Forward Deployed Engineering

- [Palantir careers](https://www.palantir.com/careers/index.html): its indexed role descriptions connect customer problem identification, workflows, stakeholder alignment, and technical delivery. This informs our cross-functional framing. It is a company-specific account, not a universal definition of the job. Search-indexed text was accessible; the direct page fetch timed out.
- [Palantir students and early talent](https://www.palantir.com/careers/students-and-early-talent/): contrasts product-capability focus with customer-focused engineering across capabilities. We use the distinction as a teaching aid, not a rigid boundary between roles. The page's text was available in search indexing; the direct page uses dynamic rendering.

## Engineering tools

- [uv project workflow](https://docs.astral.sh/uv/guides/projects/): project environments, lockfiles, and execution. The repository uses a locked development extra and separates installation from offline checks.
- [MkDocs configuration](https://www.mkdocs.org/user-guide/configuration/): navigation and strict validation settings.
- [MkDocs plugin events](https://www.mkdocs.org/dev-guide/plugins/): file collection hook used to publish canonical root and guide pages without duplicating authored Markdown.
- [Material for MkDocs diagrams](https://squidfunk.github.io/mkdocs-material/reference/diagrams/): Mermaid fence configuration. Browser rendering may need network access for the renderer even though the documentation build is local.

## How to use sources

Separate source claims from engineering judgment. A company's role description can show how that company organizes work; it cannot prove salary ranges, hiring bars, interview loops, or industry-wide preferences. A documentation page can define an API; it cannot prove our code works. That requires recorded validation against the actual implementation.

Before Phase 2, verify the current official MCP Python SDK documentation and stable release API. MCP implementation is deliberately not part of this checkpoint.
