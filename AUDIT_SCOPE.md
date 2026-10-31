# Audit scope

Written for an outside, independent security audit. Revision described:
`4f405e1093b923d8252cead889c4669b7e0c3cdf` on `main`, 2026-10-26. Everything below is taken from
the repository's own files at that revision; items marked NOT_RUN were not executed while writing
this document.

## What this repository is

The publication repository for projects built with Allen at https://www.aienos.com/allen/. Each
project is meant to live in `projects/<slug>/` with an `index.html`, the Omega source
(`<name>.om`), a `README.md` and a `meta.json`. Submissions arrive as pull requests on
`submissions/<slug>-<id>` branches, and only the maintainer's merge to `main` publishes them through
GitHub Pages. At this revision no projects are live: the tree holds the root `index.html`,
`projects/README.md`, issue forms, a CODEOWNERS file and licence files. There is no code and no
build.

## What an auditor can and cannot check here

Can check:

- The root `index.html` and its Content-Security-Policy.
- The issue forms under `.github/ISSUE_TEMPLATE/` and the code owner rule.
- The stated publication rule (review and merge before anything is served).

Cannot check here:

- Allen, the service that opens submission pull requests and files issues, and the removal of
  email addresses and phone numbers before filing. That code is not in this repository.
- Any project page, because none is live yet.
- Branch protection settings, which live in GitHub, not in the tree.

## What to review, in priority order

1. `index.html` (24 lines). Served from `main` by GitHub Pages. It sets
   `Content-Security-Policy: default-src 'self'; script-src 'none'; style-src 'unsafe-inline'` and
   links only to aienos.com and GitHub. Check that the policy is what the README promises
   ("no external scripts, stylesheets, frames or network requests").
2. The publication path described in `README.md`: submission branch, review, merge to `main`,
   Pages. Every future `projects/<slug>/index.html` shares the Pages origin with the others. Check
   that a submission cannot carry script that reaches other projects or the root page; at this
   revision nothing in the tree enforces this beyond review.
3. `.github/CODEOWNERS`: one rule, `*` owned by the single maintainer account.
4. `.github/ISSUE_TEMPLATE/` (`bug_report.yml`, `feature_request.yml`, `question.yml`,
   `config.yml`). Blank issues are disabled and the contact link points to Allen. Check the forms
   do not ask for personal data.
5. `meta.json` format described in README: slug, title, description, submission date, item id, no
   personal data. No example exists yet.

There is no `.github/workflows/` directory; GitHub Pages serves `main` directly (`.nojekyll` is
present, so no Jekyll build runs).

## Trust boundaries

- Untrusted: the content of submission pull requests (HTML and `.om` source generated with or
  by Allen for outside users) and issues filed from Allen.
- Trusted: the maintainer who reviews and merges to `main`.
- Served: whatever is on `main`, on the GitHub Pages origin.

## Threat model summary

- Assets: visitors to the Pages site; the personal data of people who use Allen; the publication
  decision.
- Attackers considered: a user who crafts a submission with hostile HTML or script; a filed issue
  that carries personal data.
- Defended: human review before merge; self-contained page rule; CSP on the root page; personal
  data removal stated in README (implemented outside this repository).
- Not defended / explicitly out of scope: no automated check in this repository enforces the
  self-contained rule or a CSP on project pages; GitHub Pages and Allen are outside this tree.

## Build from source at a pin

Nothing to build. The site is static HTML served as committed.

## Run every test

There is no test suite and no CI in this repository. A manual check an auditor can run on a
plain host (NOT_RUN while writing this document):

```sh
grep -rniE '<script|<iframe|src="http|href="http' --include='*.html' .
```

## Known limitations and NOT_RUN

- No project is live, so the per-project page rules are untested.
- The personal-data removal and the submission flow live in Allen, not here.
- No automated enforcement of "no external requests" on project pages.

## Dependencies and provenance

- No lockfile, no vendored code, no dependencies.
- No GitHub Actions. GitHub Pages hosting only.
- Licence: Apache License 2.0 with LLVM Exceptions (`LICENSE`, `NOTICE`).

## Evidence

There are no receipts in this repository. The record of what was published is the git history of
`main` and the merged pull requests.
