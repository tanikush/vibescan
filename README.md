# VibeScan

> **Security scanner for AI-generated (vibe-coded) code**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![GitHub Stars](https://img.shields.io/github/stars/tanikush/vibescan)](https://github.com/tanikush/vibescan/stargazers)

---

## The Problem

AI coding tools are everywhere in 2025. But 45% of AI-generated code contains security vulnerabilities (Veracode 2025) — and **existing scanners miss it**.

| Stat | Source |
|------|--------|
| 45% of AI code has vulnerabilities | Veracode 2025 |
| 2.74x more bugs than human-written code | Veracode 2025 |
| 400+ exposed secrets in 1,400 vibe-coded apps | Escape.tech |

**GitLeaks** scans for secrets. **TruffleHog** scans for secrets. Neither catches what VibeScan does.

---

## Features

| | |
|---|---|
| 300+ secret patterns (AWS, OpenAI, GitHub, Stripe…) | ✅ |
| Shannon entropy detection (unknown tokens) | ✅ |
| 16 AI-specific vulnerability patterns | ✅ |
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

Output: `File | Line | Issue | Risk | Match`

---

## How It Works

```
Input: Project files / .env / Git repo
        │
        ├─► Layer 1: Regex (300+ patterns)
        │   AWS keys, OpenAI tokens, DB URLs…
        │
        ├─► Layer 2: Shannon Entropy
        │   Mathematical score — finds unknown tokens
        │
        └─► Layer 3: AI-Specific Patterns
            SQL injection · eval() · debug mode · CORS wildcards

Output: Terminal table · HTML report · JSON · PR comment
```

---

## Demo

[VibeScan v1 Demo](https://youtu.be/us6Efr1zF1U) | [VibeScan v2 Demo](https://youtu.be/yc_Ud2gm5Zs)

---

## Usage

```powershell
# Scan current folder
vibescan scan .

# Scan specific folder
vibescan scan C:\Users\TANISHA\Desktop\flask-devops-task

# HTML report
vibescan scan . -o report.html

# Security dashboard (0-100 score + A-F grade)
vibescan scan . -d dashboard.html

# JSON export
vibescan scan . -j results.json

# Fast scan — secrets only, skip AI patterns
vibescan scan . --no-vibe

# Fail exit code 1 on CRITICAL (CI/CD)
vibescan scan . --fail-on-critical
```

---

## Detected Issues

### Secrets
AWS · OpenAI · GitHub · Google · JWT · Database URLs · Stripe · Slack · Private Keys · Generic API Keys

### AI-Specific Vulnerabilities
Missing authentication · SQL injection · Hardcoded credentials · Debug mode in production · CORS wildcard · `eval()` · `pickle.loads()` · Path traversal · Weak cryptography · YAML unsafe load · Prompt injection · Secrets logged to console

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
| GitHub Actions | ❌ | ✅ |
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

MIT — see [LICENSE](LICENSE) for details.

Free forever. No license fees. No cloud lock-in.
