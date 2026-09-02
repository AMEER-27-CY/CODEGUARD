# CodeGuard 🛡️

A **local, offline-first security scanner** for AI-generated code.

Built for "vibe coders" — non-technical founders, students, freelancers, and
small teams who build apps using AI tools (Lovable, Cursor, Bolt, Replit,
Copilot) but have no way to check whether the code their AI wrote is
actually safe before shipping it.

---

## Why this exists

AI coding tools are great at making code that *works*. They aren't
optimized for making code that's *safe*. Studies in 2026 found that a
majority of AI-assisted "vibe coded" apps in production have at least one
security issue — including exposed secrets and injection vulnerabilities.

**CodeGuard catches the most common of these patterns before you ship.**

## What makes it different

| | Enterprise tools (Snyk, Checkmarx) | CodeGuard |
|---|---|---|
| Where code is scanned | Uploaded to the cloud | Stays on your machine |
| Cost | Per-seat, enterprise pricing | Free, open source |
| Setup | Account + procurement | One command |
| Output | Dashboards, CVE jargon | Plain-language explanations |
| Built for | Security teams | Individuals with no security background |

CodeGuard **never executes the code it scans** — it only reads it as text.

---

## Supported languages

Scans: Python, JavaScript, TypeScript, JSX/TSX, Java, Ruby, PHP, Go, C,
C++, C#, plus `.env`, `.yml`/`.yaml`, and `.json` config files.

Detection depth varies by pattern — hardcoded secrets, SQL injection, and
wildcard CORS checks are language-agnostic. A few checks (`shell=True`,
`pickle.loads`, `hashlib.md5`) currently target Python syntax specifically;
broader per-language coverage is on the roadmap.

## What it checks for

- Hardcoded API keys / secrets
- Hardcoded AWS access keys
- `eval()` / `exec()` usage
- Shell injection (`shell=True`)
- SQL injection via string concatenation
- Insecure deserialization (`pickle`)
- Debug mode left enabled
- Wildcard CORS policy
- Weak hashing (MD5/SHA1)

---

## Installation

**Requirements:** Python 3.8 or newer.

1. Download this project — click the green **Code** button on this GitHub
   page → **Download ZIP**, then extract it. (Or `git clone` this repo if
   you use Git.)
2. Open the extracted `codeguard` folder in VS Code (or any terminal).
3. Open a terminal in that folder and run:

   ```
   pip install -e .
   ```

   *(On Windows, if `pip` isn't recognized, use `py -m pip install -e .` instead.)*

That's it — installed once, works from anywhere on your machine afterward.

---

## Usage

```bash
codeguard scan myfile.py            # scan one file
codeguard scan .                    # scan every file in the current folder
codeguard scan . --json             # machine-readable output
codeguard scan . --explain          # AI-written explanations (needs ANTHROPIC_API_KEY set)
```

### If the `codeguard` command isn't recognized

Some Windows setups don't automatically add the command to PATH. Use this
instead — it works identically, no setup needed:

```bash
python -m codeguard.cli scan myfile.py
```

(On Windows, use `py` instead of `python` if that's what your system uses.)

### Example output

```
API_KEY = "sk-live-8f3a9b2c1d4e5f6a7b8c9d0e"

[HIGH] Hardcoded API key or secret
  myfile.py:3
  > API_KEY = "sk-live-8f3a9b2c1d4e5f6a7b8c9d0e"
  Why: A secret written directly into source code gets committed to
       version control and can leak publicly.
  Fix: Load secrets from environment variables instead.
```

---

## Troubleshooting

**"'codeguard' is not recognized" (Windows)**
The install worked, but the command's location isn't in your system PATH.
Either use the `python -m codeguard.cli scan ...` fallback above, or add
the folder shown in the install warning message (something like
`...\Python313\Scripts`) to your PATH via *Environment Variables* in
Windows settings, then restart your terminal.

**"No module named codeguard.cli"**
You're not inside the project folder. Run `cd codeguard` (or navigate to
wherever you extracted/cloned it) before running the scan command.

**"package not found" when checking with `pip show codeguard`**
The install step hasn't completed yet — run `pip install -e .` (or
`py -m pip install -e .` on Windows) from inside the project folder.

---

## Roadmap

- Live CVE checking against dependencies via OSV.dev
- Scan history and security-score trend tracking
- Auto-fix suggestions for common patterns
- Git pre-commit hook integration
