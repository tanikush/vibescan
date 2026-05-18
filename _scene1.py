import sys
from pathlib import Path
from vibescan.scanner import VibeScan
from vibescan.reporter import generate_html_report

s = VibeScan('demo_project')
findings = s.scan()
summary = s.risk_summary

print(f'VibeScan -- AI Code Security Scanner')
print(f'Scanning: demo_project')
print(f'Files scanned: {s.files_scanned}')
print(f'Critical: {summary["CRITICAL"]}  High: {summary["HIGH"]}  Medium: {summary["MEDIUM"]}')
for f in findings:
    text = f.matched_text[:60] if len(f.matched_text) > 60 else f.matched_text
    print(f'  [{f.risk_level}] {f.pattern_name} | line {f.line_no} | {text}')

generate_html_report(findings, s, 'report.html')
print(f'\nReport saved to report.html')
print(f'Total: {s.files_scanned} files | {len(findings)} findings')
