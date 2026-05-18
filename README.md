# VibeScan

> **Security scanner for AI-generated (vibe-coded) code**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](python.org)

VibeScan detects security vulnerabilities specifically introduced by AI coding tools (Cursor, Claude, Copilot) — patterns that GitLeaks and TruffleHog miss.

---

## Problem

45% of AI-generated code contains security vulnerabilities (Veracode 2025). Existing tools scan for secrets but miss AI-specific patterns. VibeScan fills that gap.

---

## Quick Start

```powershell
pip install vibescan
vibescan scan .
```

Output: colorful table with `File | Line | Issue | Risk | Match`. Critical = fix now, High = fix soon.

---

## Features

| Feature | VibeScan |
|---------|----------|
| 300+ secret patterns | ✅ |
| Shannon entropy detection | ✅ |
| AI-specific vulnerabilities | ✅ |
| Live secret validation | ✅ |
| Auto-fix suggestions | ✅ |
| Git hooks | ✅ |
| GitHub Actions PR bot | ✅ |
| HTML report + Security dashboard | ✅ |
| Config file (.vibescan.yml) | ✅ |
| Free · Offline · MIT | ✅ |

---

## Demo

[VibeScan v1 Demo](https://youtu.be/us6Efr1zF1U) | [VibeScan v2 Demo](https://youtu.be/yc_Ud2gm5Zs)

---

## Usage

```powershell
# Scan
vibescan scan .

# HTML report
vibescan scan . -o report.html

# Dashboard
vibescan scan . -d dashboard.html

# JSON
vibescan scan . -j results.json

# Only secrets (fast)
vibescan scan . --no-vibe

# Fail on critical (CI/CD)
vibescan scan . --fail-on-critical
```

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
| Cost | Free | Free |

---

## Tech Stack

Python · Click · Rich · Jinja2 · Regex · Shannon Entropy · GitHub Actions

---

## License

MIT — free forever.
