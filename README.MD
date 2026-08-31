# CodeGuard
 
A local, offline-first security scanner for AI-generated code.
 
Built for non-technical "vibe coders" (people building apps with AI
tools like Lovable, Cursor, Bolt, Replit) who have no way to check
whether the code their AI wrote is safe before shipping it.
 
## Why
 
AI coding tools optimize for code that *works*, not code that's
*safe*. Studies in 2026 found the majority of AI-assisted "vibe
coded" apps in production have at least one security issue,
including exposed secrets and injection vulnerabilities. CodeGuard
catches the most common of these patterns before you ship.
 
## What makes it different
 
- **Runs entirely on your machine.** No file upload, no cloud scan.
- **Never executes the code it scans** — only reads it as text.
- **Free and open**, no account or pricing tier.
- **Plain-language explanations**, not a jargon-heavy dashboard.
## Install
 
```
pip install -e .
```
 
## Usage
 
```
codeguard scan myfile.py            # scan one file
codeguard scan .                    # scan the whole folder
codeguard scan . --json             # machine-readable output
codeguard scan . --explain          # AI-written explanations (needs ANTHROPIC_API_KEY)
```
 
## What it checks for
 
Hardcoded API keys/secrets, AWS keys, `eval()`/`exec()`, shell
injection (`shell=True`), SQL injection via string building, unsafe
deserialization (`pickle`), debug mode left on, wildcard CORS, and
weak hashing (MD5/SHA1).
 
## License
 
MIT
 