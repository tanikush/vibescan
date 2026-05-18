from jinja2 import Template
from datetime import datetime
from pathlib import Path


DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VibeScan Dashboard</title>
    <style>
        body { background:#0d1117; color:#f0f6fc; font-family:monospace; padding:2rem; }
        h1 { color:#39d353; }
        .score { width:140px; height:140px; border-radius:50%; display:flex;
                  align-items:center; justify-content:center; font-size:3rem;
                  font-weight:bold; margin:1.5rem auto; border:5px solid {{ grade_color }};
                  color:{{ grade_color }}; }
        .grade-label { color:{{ grade_color }}; font-size:1.5rem; font-weight:bold; }
        .cards { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin:1.5rem 0; }
        .card { background:#161b22; padding:1.5rem; border-radius:10px; text-align:center; }
        .card .num { font-size:2.5rem; font-weight:bold; }
        .critical { color:#ff6b6b; }
        .high     { color:#f0c040; }
        .medium   { color:#f0c040; }
        .cyan     { color:#58a6ff; }
        .exec { background:#161b22; padding:1.5rem; border-radius:8px; border-left:5px solid #39d353; margin:1rem 0; }
        table { width:100%; border-collapse:collapse; margin-top:1rem; }
        th { background:#161b22; color:#58a6ff; padding:10px; text-align:left; }
        td { padding:10px; border-bottom:1px solid #30363d; }
        .badge { padding:3px 10px; border-radius:5px; font-size:.8rem; font-weight:bold; }
        .badge-critical { background:#3d1515; color:#ff6b6b; }
        .badge-high     { background:#3d3015; color:#f0c040; }
        .badge-medium   { background:#2a2a10; color:#f0c040; }
    </style>
</head>
<body>
    <h1>🔍 VibeScan Security Dashboard</h1>
    <p>{{ scan_path }} | {{ timestamp }}</p>

    <div style="text-align:center">
        <div class="score">{{ score }}</div>
        <div class="grade-label">Grade {{ grade }} — {{ grade_label }}</div>
    </div>

    <div class="cards">
        <div class="card">
            <div class="num cyan">{{ files_scanned }}</div>
            <div>Files Scanned</div>
        </div>
        <div class="card">
            <div class="num critical">{{ critical }}</div>
            <div>Critical</div>
        </div>
        <div class="card">
            <div class="num high">{{ high }}</div>
            <div>High</div>
        </div>
        <div class="card">
            <div class="num medium">{{ medium }}</div>
            <div>Medium</div>
        </div>
    </div>

    <div class="exec">
        <h3>📋 Executive Summary</h3>
        <p>{{ exec_summary }}</p>
    </div>

    <h2>All Findings</h2>
    <table>
        <tr>
            <th>File</th>
            <th>Line</th>
            <th>Issue</th>
            <th>Risk</th>
        </tr>
        {% for f in findings %}
        <tr>
            <td><code>{{ f.file_path }}</code></td>
            <td>{{ f.line_no }}</td>
            <td>{{ f.pattern_name }}</td>
            <td>
                <span class="badge badge-{{ f.risk_level.lower() }}">
                    {{ f.risk_level }}
                </span>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''


def calculate_score(findings) -> int:
    score = 100
    for f in findings:
        if f.risk_level == 'CRITICAL':
            score -= 20
        elif f.risk_level == 'HIGH':
            score -= 10
        elif f.risk_level == 'MEDIUM':
            score -= 3
    return max(0, score)


def get_grade(score):
    if score >= 90:
        return ('A', '#39D353', 'Excellent')
    if score >= 75:
        return ('B', '#58A6FF', 'Good')
    if score >= 60:
        return ('C', '#F0C040', 'Fair')
    if score >= 40:
        return ('D', '#F78166', 'Poor')
    return ('F', '#FF6B6B', 'Critical — Do Not Deploy')


def get_exec_summary(score, summary):
    if score >= 90:
        return 'Codebase is in excellent security shape. No immediate action needed.'
    if score >= 75:
        return (f'Minor issues detected. Address {summary["HIGH"]} high-risk finding(s) '
                f'before next release.')
    if score >= 60:
        return (f'{summary["CRITICAL"]} critical and {summary["HIGH"]} high issues need '
                f'attention. Recommend a security review before deploying.')
    return (f'URGENT: {summary["CRITICAL"]} critical vulnerabilities found. '
            f'Do NOT deploy until resolved.')


def generate_dashboard(findings, scanner, output='dashboard.html'):
    score = calculate_score(findings)
    grade, grade_color, grade_label = get_grade(score)
    summary = scanner.risk_summary

    template = Template(DASHBOARD_TEMPLATE)
    html = template.render(
        scan_path=str(scanner.path),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'),
        files_scanned=scanner.files_scanned,
        critical=summary['CRITICAL'],
        high=summary['HIGH'],
        medium=summary['MEDIUM'],
        score=score,
        grade=grade,
        grade_color=grade_color,
        grade_label=grade_label,
        exec_summary=get_exec_summary(score, summary),
        findings=findings,
    )

    Path(output).write_text(html, encoding='utf-8')
    return score
