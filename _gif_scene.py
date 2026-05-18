"""Scene 1 - Run VibeScan on demo_project"""
from pathlib import Path
from vibescan.scanner import VibeScan
from vibescan.reporter import generate_html_report
from vibescan.team_report import generate_dashboard

import sys
sys.argv = ['vibescan', 'scan', 'demo_project', '--output', 'report.html']

s = VibeScan('demo_project')
findings = s.scan()
summary = s.risk_summary
print(f'VibeScan -- AI Code Security Scanner')
print(f'Scanning: demo_project')
print(f'Files scanned: {s.files_scanned}')
print(f'Critical: {summary["CRITICAL"]}  High: {summary["HIGH"]}  Medium: {summary["MEDIUM"]}')
for f in findings:
    print(f'  [{f.risk_level}] {f.pattern_name} | line {f.line_no} | {f.matched_text[:50]}')

generate_html_report(findings, s, 'report.html')
generate_dashboard(findings, s, 'dashboard.html')
print('\nHTML report saved: report.html')
print('Dashboard saved: dashboard.html')
