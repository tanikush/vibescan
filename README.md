# VibeScan

> **AI-generated code auditor — catches what traditional scanners miss**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/tanikush/vibescan/scan.yml)](.github/workflows/scan.yml)

---

## The Problems

AI coding tools (Cursor, Claude, Copilot) generate code fast — but **45% of it has security vulnerabilities** ([Veracode 2025 GenAI Code Security Report](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/)). Traditional secret scanners like GitLeaks and TruffleHog focus on credential leaks. VibeScan is built specifically to detect insecure coding patterns commonly introduced by AI coding tools.

---

## Architecture

<img width="1536" height="1024" alt="Structure" src="https://github.com/user-attachments/assets/aac838a9-ea18-4ade-81a0-ee3984858b7a" />

---

## How It Works

<img width="1190" height="1322" alt="image" src="https://github.com/user-attachments/assets/11e6db24-4ea8-455c-9ded-6ff4e1171a7c" />


1. **Pattern matching** — 14 secret regex rules + 22 AI-specific vulnerability rules run against every code file
2. **Entropy analysis** — Shannon entropy on every line flags high-entropy strings that look like secrets but don't match any known pattern
3. **Context filtering** — comment lines are skipped (no false positives on `# eval()` documentation), allowlist respected
4. **Risk scoring** — each finding is classified CRITICAL / HIGH / MEDIUM and aggregated into a 0–100 security score with an A–F grade
5. **Output** — Rich terminal table, HTML report, JSON for CI/CD, or interactive dashboard

---

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
pip install vibescan-ai

# Scan any project
vibescan scan .

# Save HTML report
vibescan scan . -o report.html
```

**Output:** `File | Line | Issue | Risk | Match` in a colorful Rich table.

---

## 📸 Screenshots

| Feature | Image |
|--------|-------|
| Terminal Output | <img src="screenshots/terminal_output.png" width="400"/> |
| HTML Report | <img src="screenshots/html_report.png" width="400"/> |
| Security Dashboard | <img src="screenshots/dashboard.png" width="400"/> |



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

## How VibeScan Compares to Traditional Scanners

| Feature | GitLeaks / TruffleHog | VibeScan |
|---------|----------------------|----------|
| Secret / credential leak detection | ✅ | ✅ |
| Shannon entropy analysis | ❌ | ✅ |
| AI-specific vulnerability patterns | ❌ | ✅ |
| Missing authentication detection | ❌ | ✅ |
| SQL injection check | ❌ | ✅ |
| Auto-fix suggestions | ❌ | ✅ |
| GitHub Actions / PR bot | ❌ | ✅ |
| Security dashboard (0–100 score) | ❌ | ✅ |
| Cost | Free | Free |

Traditional tools were built for human-authored code and primarily surface credential leaks. VibeScan focuses on a different class of problems — the insecure coding patterns that AI assistants (Cursor, Claude, Copilot) commonly introduce: missing auth checks, unsafe `eval()`, shell injection via `shell=True`, and debug mode left enabled in production. These patterns aren't secrets, but they're still critical vulnerabilities that general-purpose scanners don't look for.

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
