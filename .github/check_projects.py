#!/usr/bin/env python3
"""Checks every pull request to main: the files Allen's visitors build must stay inside their
home, be plain allowlisted text, load nothing from elsewhere and carry no secret or personal data.

Run by .github/workflows/project-checks.yml from the main branch's copy of this file (the
pull request's copy is used only while main has none), with no token and no secrets:

  check_projects.py BASE_REV PR_REV HEAD_REF

Rules (kept in step with allen_build.py / allen_spool.py in aien-dev/aienos.com, which apply
them before anything is pushed; this check is the second, independent look):
  - projects/<handle>/<project>/<file> only; handle and project are lowercase names;
    files: index.html, README.md, meta.json, name.om|js|css|md|txt|patch; no folders below;
  - UTF-8 text, no control characters, at most 64 KiB a file and 12 files a project;
  - index.html, .js and .css load or send nothing from elsewhere (no remote script, link,
    frame, fetch, WebSocket, beacon, import...);
  - nothing shaped like a key, token or password; no email address anywhere and no phone
    number in prose or the meta.json title and description (Allen removes them before filing; one here is a leak);
  - meta.json is the pusher's: exactly its fields, matching the folder, no personal data;
  - every touched project still has README.md, meta.json and index.html or an .om file;
  - a branch named u/<handle> or p/<handle>/<project> (Allen's) changes nothing else.
Exit 0 when every rule holds, 1 with one line per finding otherwise.
"""

import json
import re
import subprocess
import sys

HANDLE = r"(?:[a-z](?:[a-z0-9]|-(?=[a-z0-9])){1,23}-[0-9a-f]{8}|anon-[0-9a-f]{10})"
NAME = r"[a-z0-9](?:[a-z0-9-]{0,38}[a-z0-9])?"
PATH = re.compile(r"^projects/(%s)/(%s)/([^/]+)$" % (HANDLE, NAME))
FILENAME = re.compile(r"^(?:index\.html|README\.md|meta\.json|[a-z0-9][a-z0-9_-]{0,39}\.(?:om|js|css|md|txt|patch))$")
WEB = (".html", ".js", ".css")
PROSE = (".md", ".txt")
MAX_FILE = 64 * 1024
MAX_FILES = 12
META = {"v", "handle", "project", "title", "description", "saved", "item", "built_with", "files"}
SECRET = [re.compile(p) for p in (
    r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}", r"\bsk-[A-Za-z0-9_-]{20,}",
    r"\bsk-ant-[A-Za-z0-9_-]{10,}", r"\bAKIA[0-9A-Z]{16}\b", r"\bAIza[0-9A-Za-z_-]{30,}",
    r"xox[abprs]-[A-Za-z0-9-]{10,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.",
    r"(?i)\b(api[_-]?key|secret|passw(or)?d|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*['\"]?[^\s'\"]{12,}")]
EXTERNAL = [re.compile(p, re.I) for p in (
    r"<script\b[^>]*\bsrc\s*=", r"<link\b", r"<iframe\b", r"<object\b", r"<embed\b", r"<base\b",
    r"<meta\b[^>]*http-equiv", r"\b(src|href|action|formaction|poster|data)\s*=\s*['\"]?\s*(https?:)?//",
    r"url\(\s*['\"]?\s*(https?:)?//", r"@import\b", r"\bfetch\s*\(", r"XMLHttpRequest", r"WebSocket",
    r"EventSource", r"sendBeacon", r"\bimport\s*\(", r"\bimportScripts\b", r"\bwindow\.open\b")]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w.])\+?\d[\d ().-]{7,}\d(?!\w|\.\d)")


def git(*args):
    return subprocess.run(("git",) + args, check=True, capture_output=True).stdout


def bad_text(text):
    for ch in text:
        o = ord(ch)
        if ((o < 32 and ch not in "\n\t\r") or o == 127 or 0xD800 <= o <= 0xDFFF or 0xFDD0 <= o <= 0xFDEF
                or (o & 0xFFFE) == 0xFFFE or o == 0xFFFD):
            return "a control or binary character"
    return None


def check_file(path, name, handle, project, raw):
    out = []
    if not FILENAME.match(name):
        out.append("file name not allowed (index.html, README.md, meta.json, name.om|js|css|md|txt|patch)")
        return out
    if len(raw) > MAX_FILE:
        out.append("larger than %d KiB" % (MAX_FILE // 1024))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return out + ["not UTF-8 text"]
    why = bad_text(text)
    if why:
        out.append("contains " + why)
    for pat in SECRET:
        if pat.search(text):
            out.append("looks like it contains a secret (%s)" % pat.pattern[:30])
            break
    if name.endswith(WEB):
        for pat in EXTERNAL:
            if pat.search(text):
                out.append("loads or sends something from elsewhere (%s)" % pat.pattern[:40])
                break
    if EMAIL.search(text):
        out.append("contains an email address")
    if name.endswith(PROSE) and PHONE.search(text):
        out.append("contains a phone number")
    if name == "meta.json":
        try:
            m = json.loads(text)
        except ValueError:
            return out + ["meta.json is not JSON"]
        if not isinstance(m, dict) or set(m) != META:
            out.append("meta.json fields must be exactly %s" % ", ".join(sorted(META)))
        elif m.get("handle") != handle or m.get("project") != project:
            out.append("meta.json names another home or project")
        elif any(PHONE.search(str(m.get(k, ""))) for k in ("title", "description")):
            out.append("meta.json contains a phone number")
    return out


def main(base, pr, head_ref):
    findings = []
    changed = git("diff", "--name-status", "--no-renames", "-z", base, pr).decode().split("\0")
    entries = [(changed[i], changed[i + 1]) for i in range(0, len(changed) - 1, 2)]
    allen = re.fullmatch(r"u/(%s)|p/(%s)/(%s)" % (HANDLE, HANDLE, NAME), head_ref)
    touched = set()
    for status, path in entries:
        m = PATH.match(path)
        if not path.startswith("projects/") or path == "projects/README.md":
            if allen:
                findings.append("%s: a branch from Allen may only change its own project folder" % path)
            elif path.startswith(".github/"):
                print("note: %s changes the repository's automation; review it by hand" % path)
            continue
        if not m:
            findings.append("%s: outside projects/<handle>/<project>/<file>" % path)
            continue
        handle, project, name = m.groups()
        if allen and allen.group(2) and (handle, project) != (allen.group(2), allen.group(3)):
            findings.append("%s: branch %s may only change projects/%s/%s/" % (path, head_ref, allen.group(2),
                                                                             allen.group(3)))
        if allen and allen.group(1) and handle != allen.group(1):
            findings.append("%s: branch %s may only change projects/%s/" % (path, head_ref, allen.group(1)))
        touched.add((handle, project))
        if status == "D":
            continue
        mode = git("ls-tree", pr, "--", path).decode().split(" ", 1)[0]
        if mode != "100644":
            findings.append("%s: must be a plain file (mode %s)" % (path, mode or "?"))
            continue
        for f in check_file(path, name, handle, project, git("show", "%s:%s" % (pr, path))):
            findings.append("%s: %s" % (path, f))
    for handle, project in sorted(touched):
        d = "projects/%s/%s/" % (handle, project)
        names = [p[len(d):] for p in git("ls-tree", "-r", "--name-only", pr, "--", d).decode().splitlines()]
        if not names:
            continue  # the project was removed
        if any("/" in n for n in names):
            findings.append("%s: no folders inside a project" % d)
        if len(names) > MAX_FILES + 1:
            findings.append("%s: more than %d files" % (d, MAX_FILES))
        for need in ("README.md", "meta.json"):
            if need not in names:
                findings.append("%s: needs %s" % (d, need))
        if not any(n == "index.html" or n.endswith(".om") for n in names):
            findings.append("%s: needs index.html or an .om file" % d)
    for f in findings:
        print("FAIL " + f)
    print("%d changed file(s), %d project(s), %d finding(s)" % (len(entries), len(touched), len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
