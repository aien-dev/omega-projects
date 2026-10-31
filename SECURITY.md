# Security policy

## Reporting a vulnerability

Report privately. Do not open a public issue, pull request or discussion about it.

1. GitHub: open this repository's Security tab and choose "Report a vulnerability". This
   creates a private advisory that only the maintainers can see. If that option is not shown,
   private vulnerability reporting has not been enabled for this repository yet; use email.
2. Email: drake@aienos.com with the subject `[omega-projects] security report`.

Include the commit or release you tested, the component (path), steps to reproduce, and what an
attacker gains. If the report involves a secret, say where it was exposed and do not send the
secret itself. Encrypted mail is not required; do not post proof-of-concept payloads publicly.

## Response targets

This project has one maintainer; the targets below are best effort and stated honestly.

- Acknowledgement: within 3 working days.
- Triage and severity: within 7 days of acknowledgement.
- Fix or mitigation for confirmed issues: aim for 30 days for high and critical, 90 days
  otherwise, with a status update at least every 14 days until closed.
- Disclosure: coordinated. An advisory is published with credit (unless you ask otherwise)
  once the fix is on the default branch. Default embargo 90 days, negotiable.

## Scope

This repository holds projects submitted from Allen at https://www.aienos.com/allen/ and serves
them with GitHub Pages from `main`.

In scope:

- A page under `projects/<slug>/` or the root `index.html` that loads an external script,
  stylesheet, frame or network request. README requires pages to be self-contained.
- A page that runs script against the GitHub Pages origin in a way that could affect other
  projects served from the same origin, or weakens the root page's Content-Security-Policy
  (`script-src 'none'`).
- Personal data (email addresses, phone numbers) in a project, a `meta.json`, or an issue filed
  from Allen. README says these are removed before anything is filed.
- A way for a submission to be published without the maintainer's review and merge to `main`.

Out of scope:

- Allen itself and the aienos.com site; report those through the aienos.com site repository.
- The Omega compiler (`aien-dev/omega-mv`) and GitHub Pages hosting.

## Supported versions

Only the default branch `main`; there is no release. Reports against older commits are welcome
but fixes land on the default branch only.

## Status

No projects are live yet (`projects/README.md`). Every submission arrives as a pull request and goes
live only after the maintainer reviews and merges it. No certification, no bug bounty. See
AUDIT_SCOPE.md for what to review.
