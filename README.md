# omega-projects

Every project anyone builds with Aien at [aienos.com/allen/](https://www.aienos.com/allen/) goes here.

- Each project lives in `projects/<slug>/`: an `index.html` that runs in the browser, the Omega
  source (`<name>.om`), a `README.md` and a `meta.json` (slug, title, description, submission date,
  item id; no personal data).
- Aien never publishes anything. A project arrives as a pull request on a `submissions/<slug>-<id>`
  branch. Drake reviews every project before it goes live; only Drake's merge to `main` publishes it.
- Live projects are served by GitHub Pages from `main` at
  `https://aien-dev.github.io/omega-projects/projects/<slug>/`.
- Issues filed from [aienos.com/allen/](https://www.aienos.com/allen/) arrive here labelled
  `from-aien` (issues filed before the 2026-10-26 rename carry `from-allen`), with an `area:<repo>`
  label naming the repository they concern, and are transferred
  to the right repository.
- Email addresses and phone numbers are removed before anything is filed.

Pages must be self-contained: no external scripts, stylesheets, frames or network requests.

Licensed under the Apache License 2.0 with LLVM Exceptions; see `LICENSE` and `NOTICE`.
