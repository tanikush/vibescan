from pathlib import Path
from vibescan.scanner import VibeScan

s = VibeScan('tests/fixtures/vulnerable_app.py')
findings = s.scan()
summary = s.risk_summary
print(f'VibeScan -- AI Code Security Scanner')
print(f'Scanning: tests/fixtures/vulnerable_app.py')
print(f'Files scanned: {s.files_scanned}')
print(f'Critical: {summary["CRITICAL"]}  High: {summary["HIGH"]}  Medium: {summary["MEDIUM"]}')
for f in findings:
    print(f'  [{f.risk_level}] {f.pattern_name:<35} line {f.line_no:<3} | {f.matched_text[:50]}')
