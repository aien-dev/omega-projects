# omega-projects

Every project anyone builds with Aien at [aienos.com/allen/](https://www.aienos.com/allen/) goes here.

- Every builder has a home, `projects/<handle>/`, and each project lives in
  `projects/<handle>/<project>/`: a `README.md` (what it is and who it helps), the source (`index.html`
  that runs in the browser, Omega `<name>.om`, `.js`, `.css`, notes), and a `meta.json` written by
  Aien's filing service (handle, project, title, description, date, item id, file list; no personal
  data). A handle is a chosen name plus a tag tied to the visitor's Aien key (`ada-1a2b3c4d`), or a
  one-time `anon-...` handle for anonymous builders; never an email address.
- **Save** commits the project to the builder's branch `u/<handle>`, viewable here at once.
- **Publish** opens a pull request from `p/<handle>/<project>` to `main`. Aien never merges and never
  writes `main`; Drake reviews every project and only his merge publishes it ("Built with Aien").
- Every pull request to `main` runs `project checks` (`.github/workflows/project-checks.yml`):
  `pull_request` only, read-only token, no secrets, no third-party actions; the checker comes from
  `main` and enforces the file allowlist, size caps, no external loads, and the secret and personal
  data scan.
- Live projects are served by GitHub Pages from `main` at
  `https://aien-dev.github.io/omega-projects/projects/<handle>/<project>/`.
- Issues filed from [aienos.com/allen/](https://www.aienos.com/allen/) arrive here labelled
  `from-aien` (issues filed before the 2026-10-26 rename carry `from-allen`), with an `area:<repo>`
  label naming the repository they concern, and are transferred
  to the right repository.
- Email addresses and phone numbers are removed before anything is filed.

## Licence

Every project stays its author's. By submitting it here the author licences it under
[Apache-2.0](LICENSE).
