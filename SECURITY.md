# Security policy

This is a pre-release learning repository, not a supported production service. The current development branch receives fixes on a best-effort basis; no released version has a support guarantee.

## Report a vulnerability

Use GitHub's **Security -> Report a vulnerability** option if private vulnerability reporting is enabled. Include the affected revision, minimal synthetic reproduction, expected boundary, and impact. Never include real tokens or customer records.

If that option is unavailable, use a private contact method explicitly published by the maintainer on their GitHub profile. If none is available, open a non-sensitive issue requesting a private reporting channel without exploit details. A dedicated private reporting channel is not yet confirmed. Do not publish sensitive material in an ordinary issue.

## Safe learning boundaries

- Use fictional organizations and synthetic inputs only.
- Keep `.env` ignored; `.env.example` contains configuration names, not secrets.
- Authentication establishes identity. Authorization determines permitted actions and data.
- Treat retrieved documents and tool output as untrusted input, never as authority to grant permissions.
- Future write tools must enforce approval and least privilege in code, with audit records and denial tests.
- Approval does not replace authorization. A reviewer cannot grant access they do not possess.

If a secret is accidentally exposed, revoke or rotate it first, then coordinate removal from history and logs. Deleting the latest file alone does not invalidate the secret. Learning deployments should not be exposed publicly without an explicit security and operational review.
