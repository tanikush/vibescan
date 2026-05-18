# VibeScan

> **Security scanner for AI-generated (vibe-coded) code**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/tanikush/vibescan/scan.yml)](.github/workflows/scan.yml)

---

## The Problem

AI coding tools (Cursor, Claude, Copilot) generate code fast — but **45% of it has security vulnerabilities** (Veracode 2025). Existing scanners (GitLeaks, TruffleHog) scan for secrets only. They miss what VibeScan catches.

---

## Architecture

```
                     ┌──────────────────┐
                     │   VibeScan       │
                     │ CLI / Python     │
                     └────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
       ┌──────▼──────┐  ┌────▼─────┐  ┌──────▼──────┐
       │   INPUT     │  │ SCANNER  │  │   OUTPUT     │
       │             │  │          │  │              │
       │ Files       │─►│ Regex    │─►│ Terminal     │
       │ .env        │  │ 14 secret│  │ table        │
       │ Git repo    │  │ patterns │  │              │
       └─────────────┘  │          │  │ HTML report  │
                        │ Shannon  │  │ (Jinja2)     │
                        │ Entropy  │  │              │
                        │          │  │ JSON export  │
                        │ 22 AI    │  │              │
                        │ patterns │  │ Dashboard    │
                        │          │  │ (score +     │
                        └──────────┘  │  grade)      │
                                     │              │
                                     └──────────────┘
```

---

## Features

| Feature | Status |
|---|---|
| 14 secret patterns (AWS, OpenAI, GitHub, Stripe, JWT, DB URLs…) | ✅ |
| Shannon entropy detection (unknown tokens) | ✅ |
| 22 AI-specific vulnerability patterns | ✅ |
| Live secret validation (GitHub + OpenAI tokens) | ✅ |
| Auto-fix suggestions with safe code snippets | ✅ |
| Git hooks (block push on CRITICAL) | ✅ |
| GitHub Actions PR bot | ✅ |
| HTML report + Security dashboard (0–100 score, A–F grade) | ✅ |
| Config file with allowlist & baseline | ✅ |
| Zero cost · Works offline · MIT license | ✅ |

---

## Quick Start

```powershell
# Install — one time
pip install vibescan

# Scan any project
vibescan scan .

# Save HTML report
vibescan scan . -o report.html
```

**Output:** `File | Line | Issue | Risk | Match` in a colorful Rich table.

---

## Screenshots

| Terminal Output | HTML Report | Security Dashboard |
|----------------|-------------|-------------------|
| ![Terminal Output](screenshots/terminal_output.png) | ![HTML Report](screenshots/html_report.png) | ![Dashboard](screenshots/dashboard.png) |

---

## Demo

[VibeScan v1 Demo](https://youtu.be/us6Efr1zF1U) | [VibeScan v2 Demo](https://youtu.be/yc_Ud2gm5Zs)

---

## Usage

```powershell
# Scan current folder
vibescan scan .

# Scan specific folder
vibescan scan path/to/your/project

# HTML report
vibescan scan . -o report.html

# Security dashboard (0-100 score + A-F grade)
vibescan scan . -d dashboard.html

# JSON export (CI/CD integration)
vibescan scan . -j results.json

# Fast scan — secrets only, skip AI patterns
vibescan scan . --no-vibe

# Fail on critical (exit code 1 for CI/CD)
vibescan scan . --fail-on-critical

# Verify if detected secrets are live or revoked
vibescan scan . --validate
```

---

## Detected Issues

### Secrets
AWS Access Key · AWS Secret Key · OpenAI API Key · GitHub Token / OAuth / PAT · Google API Key · JWT Token · Database URL (PostgreSQL / MongoDB / MySQL / Redis) · Generic API Key · Generic Password · Private Key · Stripe Secret / Test Key · Slack Token · Hardcoded `.env` values

### AI-Specific Vulnerabilities
Prompt injection · Unvalidated LLM input · Password / token logged · `subprocess` with `shell=True` · `os.system()` · Path traversal · `.env` served in route · Hardcoded admin credentials · Weak `random` module · `yaml.load()` · `pickle.loads()` · Missing rate limit on auth · Unvalidated file upload · Missing auth check · SQL injection via f-strings · Debug mode in production · CORS wildcard · Direct `.env` read · `eval()` usage

---

## Why VibeScan Over GitLeaks?

| Feature | GitLeaks | VibeScan |
|---------|----------|----------|
| Secret detection | ✅ | ✅ |
| Entropy analysis | ❌ | ✅ |
| AI-specific patterns | ❌ | ✅ |
| Missing auth detection | ❌ | ✅ |
| SQL injection check | ❌ | ✅ |
| Auto-fix suggestions | ❌ | ✅ |
| GitHub Actions / PR bot | ❌ | ✅ |
| Security dashboard | ❌ | ✅ |
| Cost | Free | Free |

---

## Tech Stack

Python · Click · Rich · Jinja2 · Regex · Shannon Entropy · GitHub Actions

---

## Installation (from source)

```powershell
git clone https://github.com/tanikush/vibescan.git
cd vibescan
pip install -r requirements.txt
pip install -e .
```

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

1. Fork it
2. Create your feature branch (`git checkout -b feature/my-change`)
3. Commit your changes (`git commit -m 'Add: my new feature'`)
4. Push the branch (`git push origin feature/my-change`)
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details. Free forever. No license fees. No cloud lock-in.
