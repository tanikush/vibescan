import os
import requests
from typing import List
from .fixer import get_fix


def get_headers():
    token = os.getenv('GITHUB_TOKEN')
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }


def build_comment(findings, files_scanned: int) -> str:
    critical = [f for f in findings if f.risk_level == 'CRITICAL']
    high = [f for f in findings if f.risk_level == 'HIGH']
    medium = [f for f in findings if f.risk_level == 'MEDIUM']

    lines = [
        '## 🔍 VibeScan Security Report',
        '',
        f'Scanned **{files_scanned}** files — **{len(findings)}** issues found',
        '',
        '| Critical | High | Medium |',
        '|---------:|-----:|-------:|',
        f'| {len(critical)} | {len(high)} | {len(medium)} |',
        ''
    ]

    if critical:
        lines.append('### 🚨 Critical — Fix Immediately')
        for f in critical[:5]:
            lines.append(f'- **{f.pattern_name}** in `{f.file_path}` line `{f.line_no}`')
            fix = get_fix(f.pattern_name)
            if fix:
                lines.append(f'  - {fix[0]}')
        lines.append('')

    if high:
        lines.append('### ⚠️ High Risk')
        for f in high[:5]:
            lines.append(f'- **{f.pattern_name}** in `{f.file_path}`')
        lines.append('')

    lines.append('---')
    lines.append('*Powered by [VibeScan](https://github.com/tanikush/vibescan)*')
    return '\n'.join(lines)


def post_pr_comment(repo: str, pr_number: int, comment: str) -> bool:
    url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'
    r = requests.post(url, headers=get_headers(), json={'body': comment})
    return r.status_code == 201


def create_issue(repo: str, findings) -> bool:
    critical = [f for f in findings if f.risk_level == 'CRITICAL']
    if not critical:
        return False
    url = f'https://api.github.com/repos/{repo}/issues'
    data = {
        'title': f'[VibeScan] {len(critical)} Critical Security Issues',
        'body': build_comment(findings, 0),
        'labels': ['security', 'vibescan', 'critical']
    }
    r = requests.post(url, headers=get_headers(), json=data)
    return r.status_code == 201