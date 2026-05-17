from jinja2 import Template
from datetime import datetime
from pathlib import Path

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VibeScan Security Report</title>
    <style>
        body { background:#0d1117; color:#f0f6fc; font-family: monospace; padding:2rem; }
        h1 { color:#39d353; }
        .critical { color:#ff6b6b; font-weight:bold; }
        .high { color:#f0c040; font-weight:bold; }
        .medium { color:#f0c040; }
        table { width:100%; border-collapse:collapse; margin-top:1rem; }
        th { background:#161b22; color:#58a6ff; padding:8px; text-align:left; }
        td { padding:8px; border-bottom:1px solid #30363d; }
        .summary-box { display:flex; gap:1rem; margin:1rem 0; }
        .stat { background:#161b22; padding:1rem 2rem; border-radius:8px; text-align:center; }
        .stat .num { font-size:2rem; font-weight:bold; }
    </style>
</head>
<body>
    <h1>🔍 VibeScan Security Report</h1>
    <p>Scanned: {{ scan_path }} | {{ timestamp }}</p>
    <p>Files: {{ files_scanned }} | Issues: {{ total }}</p>
    
    <div class='summary-box'>
        <div class='stat'>
            <div class='num critical'>{{ critical }}</div>
            <div>CRITICAL</div>
        </div>
        <div class='stat'>
            <div class='num high'>{{ high }}</div>
            <div>HIGH</div>
        </div>
        <div class='stat'>
            <div class='num medium'>{{ medium }}</div>
            <div>MEDIUM</div>
        </div>
    </div>
    
    {% if findings %}
    <table>
        <tr><th>File</th><th>Line</th><th>Issue</th><th>Risk</th><th>Match</th></tr>
        {% for f in findings %}
        <tr>
            <td>{{ f.file }}</td>
            <td>{{ f.line }}</td>
            <td>{{ f.pattern }}</td>
            <td class='{{ f.risk.lower() }}'>{{ f.risk }}</td>
            <td><code>{{ f.match }}</code></td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p style='color:#39d353'>✓ No issues found!</p>
    {% endif %}
</body>
</html>
'''

def generate_html_report(findings, scanner, output_path):
    summary = scanner.risk_summary
    template = Template(HTML_TEMPLATE)
    html = template.render(
        scan_path=str(scanner.path),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'),
        files_scanned=scanner.files_scanned,
        total=len(findings),
        critical=summary['CRITICAL'],
        high=summary['HIGH'],
        medium=summary['MEDIUM'],
        findings=[f.to_dict() for f in findings]
    )
    Path(output_path).write_text(
        html,
        encoding="utf-8"
    )
